"""Edge Nodes are implemented following the State Design Pattern.
All states are inside this module
"""
import abc
import asyncio
import logging
from asyncio import create_subprocess_shell
from dataclasses import dataclass

from aiospb.nodes.messages import MqttNodeCarrier, NodePayload

from ..data import DataType, Metric
from ..mqtt import MqttError
from .scanning import Scanner
from .stores import HistoricalStore

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class NodeState(abc.ABC):
    """Interface to be followed by any node state"""

    @abc.abstractmethod
    async def establish_session(self):
        """Called by edge node"""

    @abc.abstractmethod
    async def terminate_session(self):
        """Called by edge node"""


@dataclass
class NodeContext:
    """Group all common state variables into one"""

    carrier: MqttNodeCarrier
    scanner: Scanner
    store: HistoricalStore
    primary_hostname: str = ""
    state: NodeState | None = None


class Disconnected(NodeState):
    """Edge is disconnected to MQTT"""

    def __init__(self, context: NodeContext, auto_establish: bool = False):
        self._context = context
        context.state = self
        self._waiting_to_host_reporting = None
        self._saving_changes = asyncio.create_task(self._save_changes())
        logger.info("Edge Node is DISCONNECTED")
        self._establish = None
        if auto_establish:
            self._establish = asyncio.create_task(self.establish_session())

    async def establish_session(self):
        trys = 0
        while True:
            try:
                await self._context.carrier.connect()
                self._waiting_to_host_reporting = asyncio.create_task(
                    self._when_host_is_reporting()
                )
                return
            except MqttError as e:
                trys += 1
                if trys < 7:
                    wait = 10
                elif trys < 12:
                    wait = 60
                else:
                    wait = 300
                logger.warning(f"Not possible to connect, waiting {wait} seconds")
                logger.exception(e)
                await asyncio.sleep(wait)
            except Exception as e:
                logger.error("I have dead and someone should help me...")
                logger.exception(e)

    async def _when_host_is_reporting(self):
        while True:
            try:
                message = await self._context.carrier.deliver_message()
            except MqttError as e:
                logger.error("When recieving messages from host, restablishing session")
                logger.exception(e)
                await self.establish_session()
                return

            if not message.is_a("STATE"):
                continue

            if (
                self._context.primary_hostname
                and message.topic.value
                != f"spBv1.0/STATE/{self._context.primary_hostname}"
            ):
                continue

            if message.payload.to_dict()["online"]:
                self._saving_changes.cancel()
                birth = await self._context.scanner.start()
                logger.debug(f"Found {len(birth)} root metrics in the Edge Node")
                try:
                    await self._context.carrier.send_birth(birth)
                    logger.info("Birth certificate published to MQTT server")
                    self._waiting_to_host_reporting = None
                    Reporting(self._context)
                except MqttError as e:
                    logger.error(
                        "When sending birth certificate, restablishing session"
                    )
                    logger.exception(e)
                    await self.establish_session()
                finally:
                    return

    async def _save_changes(self):
        while True:
            changes = await self._context.scanner.deliver_changes()
            logger.info(f"Saving {len(changes)} changes as history...")

            try:
                await self._context.store.save_dtos(changes)
                logger.info("Saved changes to temporary store")
            except Exception as e:
                logger.warning("Not saved the samples in history!!!")
                logger.exception(e)

    async def terminate_session(self):
        """Close session, stopping scanning"""
        self._cancel_tasks()

        await self._context.scanner.stop()
        if self._context.carrier.is_connected:
            logger.debug("Disconnecting cleanly ...")
            await self._context.carrier.send_death()
            await self._context.carrier.disconnect()
            logger.info("Edge node cleanly disconnected")

    def _cancel_tasks(self):
        if self._waiting_to_host_reporting is not None:
            self._waiting_to_host_reporting.cancel()
        self._saving_changes.cancel()


class Reporting(NodeState):
    """Gateway is connected to MQTT Server and Primary Host is Reporting"""

    def __init__(self, context: NodeContext):
        self._context = context
        context.state = self
        self._sending = asyncio.create_task(self._send_node_changes())
        self._recieving = asyncio.create_task(self._recieve_host_messages())
        logger.info("Edge Node is REPORTING")

    async def establish_session(self):
        """Not allowed, only when is disconnected to Mqtt Broker"""
        raise RuntimeError(
            f'State "REPORTING" can not establish session, terminate_session before'
        )

    async def terminate_session(self):
        """Terminate cleanly the session"""
        logger.info(f"Terminating session REPORTING")
        self._cancel_tasks()
        await Disconnected(self._context).terminate_session()

    def _cancel_tasks(self):
        """Stops tasks, cancel incomming, wait messages to be sent."""
        self._sending.cancel()
        self._recieving.cancel()

    async def _send_node_changes(self):
        while True:
            try:
                changes = await self._context.scanner.deliver_changes()
                logger.info(f"Detected {len(changes)} changes from the scanner")

                if changes:
                    history = []
                    try:
                        if self._context.store.has_dtos():
                            history = await self._context.store.load_all_dtos()
                            logger.info(f"Loaded {len(history)} historical changes")
                    except Exception as e:
                        logger.error("Not possible to load history of changes")
                        logger.exception(e)

                    try:
                        await self._context.carrier.send_data_changes(history + changes)
                        logger.info("Sent changes to the MQTT Server")
                    except MqttError as e:
                        logger.error("MQTT error when sending changes")
                        try:
                            await self._context.store.save_dtos(changes)
                        except Exception as e:
                            logger.error("Not possible to save changes")
                            logger.exception(e)
                        self._cancel_tasks()
                        Disconnected(self._context, auto_establish=True)
                        return

                try:
                    if self._context.store.has_dtos():
                        await self._context.store.clear()
                except Exception as e:
                    logger.error("Not possible to clean scan changes from store")
                    logger.exception(e)
            except Exception as e:
                logger.error("It has broken sending data changes loop!!!")
                logger.exception(e)
                raise e

    async def _recieve_host_messages(self):
        while True:
            try:
                message = await self._context.carrier.deliver_message()
            except MqttError as e:
                logger.error(f"Error when recieving host messages")
                logger.exception(e)
                self._cancel_tasks()
                Disconnected(self._context, auto_establish=True)
                return

            if message.is_a("NCMD"):
                if type(message.payload) is NodePayload:
                    await self._process_commands(message.payload)
                continue

            if (
                self._context.primary_hostname
                and message.topic.value
                != f"spBv1.0/STATE/{self._context.primary_hostname}"
            ):
                continue

            if not message.payload.to_dict()["online"]:
                logger.info(f"Detected host is disconnected, stopped data sending")
                self._cancel_tasks()
                Connected(self._context)
                return

    async def _process_commands(self, payload: NodePayload):
        commands = payload.metrics
        confirmations = []
        for index, command in enumerate(commands):
            if command.name == "Node Control/Reboot":
                confirmations.append(
                    Metric(0, True, DataType.Boolean, name="Node Control/Reboot")
                )
                if index + 1 < len(commands):
                    logger.warning(
                        f"The commands {commands[index+1:]} will not applied after reboot"
                    )
                await self._context.carrier.confirm_commands(confirmations)
                await self._reboot()
                return

            elif command.name == "Node Control/Rebirth":
                logger.debug("Recieved rebirth command from host application")
                try:
                    await self._rebirth()
                except MqttError as e:
                    logger.error("MQTT connection error when rebirth")
                    logger.exception(e)
                    self._cancel_tasks()
                    Disconnected(self._context, auto_establish=True)

                confirmations.append(
                    Metric(0, True, DataType.Boolean, name="Node Control/Rebirth")
                )
            else:
                description = command.name + ":" + str(command.alias)
                logger.info(f"Writing to metric '{description}'")

                confirmations.append(
                    await self._context.scanner.execute_command(command)
                )

        if confirmations:
            await self._context.carrier.confirm_commands(confirmations)
            logger.info(f"Sent confirmations of {len(confirmations)} changes")

    async def _reboot(self):
        await self.terminate_session()
        process = await create_subprocess_shell(
            "reboot", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        # Wait for the command to complete
        await process.communicate()

    async def _rebirth(self):
        await self._context.scanner.stop()
        birth = await self._context.scanner.start()
        logger.info(f"Found {len(birth)} root metrics for birth certificate")
        await self._context.carrier.send_birth(birth)
        logger.info(f"Resent birth certificate to MQTT server")


class Connected(NodeState):
    """Gateway connected to MQTT Server, but primary host is connected"""

    def __init__(self, context: NodeContext):
        self._context = context
        context.state = self
        self._recieving_messages = asyncio.create_task(self._recieve_host_messages())
        self._saving_changes = asyncio.create_task(self._save_changes())
        logger.info("Edge Node is CONNECTED")

    async def establish_session(self):
        """Not allowed, only when is disconnected to Mqtt Broker"""

        raise RuntimeError(
            f'State "connected" can not establish session, terminate_session before'
        )

    async def terminate_session(self):
        """Close session of node cleanly"""
        logger.info(f"Terminating session from CONNECTED state")
        self._cancel_tasks()
        await Disconnected(self._context).terminate_session()

    def _cancel_tasks(self):
        self._recieving_messages.cancel()
        self._saving_changes.cancel()

    async def _save_changes(self):
        while True:
            changes = await self._context.scanner.deliver_changes()
            logger.info(f"Saving {len(changes)} changes as history...")

            try:
                await self._context.store.save_dtos(changes)
                logger.info("Saved changes to temporary store")
            except Exception as e:
                logger.warning("Not saved the samples in history!!!")
                logger.exception(e)

    async def _recieve_host_messages(self):
        while True:
            try:
                message = await self._context.carrier.deliver_message()
            except MqttError as e:
                logger.error("Lost MQTT connection when recieving host messages")
                logger.exception(e)
                self._cancel_tasks()
                Disconnected(self._context, auto_establish=True)
                return

            if not message.is_a("STATE"):
                continue

            if (
                self._context.primary_hostname
                and message.topic.value
                != f"spBv1.0/STATE/{self._context.primary_hostname}"
            ):
                continue

            if message.payload.to_dict()["online"]:
                logger.info("The host application is ONLINE!!")
                await self._context.scanner.stop()
                birth = await self._context.scanner.start()
                try:
                    await self._context.carrier.send_birth(birth)
                    logger.info("Birth certificate is sent")
                except MqttError:
                    Disconnected(self._context, auto_establish=True)

                self._cancel_tasks()
                Reporting(self._context)
                return
