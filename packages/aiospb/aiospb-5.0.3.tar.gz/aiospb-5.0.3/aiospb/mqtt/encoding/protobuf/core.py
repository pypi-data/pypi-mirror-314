from typing import Any

from aiospb.data import DataType, ValueType
from aiospb.nodes.messages import NodePayload

from ... import MessageEncoder
from . import sparkplug_pb2 as pb2


class EncodingError(Exception):
    pass


class _ValueConversor:
    _VALUES = {
        "String": "string_value",
        "Float": "float_value",
        "Double": "double_value",
        "Boolean": "boolean_value",
        "Bytes": "bytes_value",
    }

    def save_value(
        self,
        message: pb2.Payload.Metric | pb2.Payload.PropertyValue,
        type_str: str,
        value: ValueType,
    ):
        if value is None:
            setattr(message, "is_null", True)
        elif type_str == "Int64" and type(value) is int:
            setattr(message, "long_value", value & 0xFFFFFFFFFFFFFFFF)
        elif type_str.startswith("Int") and type(value) is int:
            setattr(message, "int_value", value & 0xFFFFFFFF)
        else:
            setattr(message, self._VALUES[type_str], value)

    def load_value(self, message, type_str: str) -> ValueType:
        if message.HasField("is_null"):
            return
        if type_str == "Int64":
            value = getattr(message, "long_value")
            return value - 0x10000000000000000 if value > 0x7FFFFFFFFFFFFFFF else value
        elif type_str.startswith("Int"):
            value = getattr(message, "int_value")
            return value - 0x100000000 if value > 0x7FFFFFFF else value
        else:
            return getattr(message, self._VALUES[type_str])


class ProtobufEncoder(MessageEncoder):
    def __init__(self):
        self._conversor = _ValueConversor()

    def encode(self, payload: NodePayload) -> bytes:
        """Convert a message to a payload"""
        pb_payload = pb2.Payload()

        try:
            pb_payload.timestamp = payload.timestamp
            if payload.seq is not None:
                pb_payload.seq = payload.seq
            for metric in payload.metrics:
                pb_metric = pb_payload.metrics.add()
                pb_metric.datatype = metric.datatype.value
                pb_metric.timestamp = metric.timestamp
                self._conversor.save_value(
                    pb_metric, metric.datatype.name, metric.value
                )
                if metric.name:
                    pb_metric.name = metric.name
                if metric.alias:
                    pb_metric.alias = metric.alias
                if metric.is_historical:
                    pb_metric.is_historical = True
                if metric.is_transient:
                    pb_metric.is_transient = True
                if metric.properties:
                    values = []
                    for prop in metric.properties.values:
                        if prop.value is None:
                            value = pb2.Payload.PropertyValue(
                                type=prop.data_type.value, is_null=True
                            )
                        else:
                            value = pb2.Payload.PropertyValue(type=prop.data_type.value)
                            self._conversor.save_value(
                                value, prop.data_type.name, prop.value
                            )
                        values.append(value)

                    pb_metric.properties.CopyFrom(
                        pb2.Payload.PropertySet(
                            keys=metric.properties.keys, values=values
                        )
                    )

            return pb_payload.SerializeToString()
        except Exception as e:
            raise EncodingError("Error when encoding") from e

    def _decode_metric(self, spb_metric: pb2.Payload.Metric) -> dict[str, Any]:
        dump = {
            "timestamp": spb_metric.timestamp,
            "dataType": DataType(spb_metric.datatype).name,
        }
        if spb_metric.HasField("is_null"):
            value = None
        else:
            value = self._conversor.load_value(
                spb_metric, DataType(spb_metric.datatype).name
            )
        dump["value"] = value

        if spb_metric.HasField("name"):
            dump["name"] = spb_metric.name
        if spb_metric.HasField("alias"):
            dump["alias"] = spb_metric.alias
        if spb_metric.HasField("is_historical"):
            dump["is_historical"] = spb_metric.is_historical
        if spb_metric.HasField("is_transient"):
            dump["is_transient"] = spb_metric.is_transient
        if spb_metric.HasField("properties"):
            properties = spb_metric.properties
            dump["properties"] = {
                key: {
                    "dataType": DataType(prop.type),
                    "value": self._conversor.load_value(prop, DataType(prop.type).name),
                }
                for key, prop in zip(properties.keys, properties.values)
            }
        return dump

    def decode(self, payload: bytes) -> NodePayload:
        """Convert payload to a message object"""
        try:
            pb_payload = pb2.Payload.FromString(payload)
        except Exception as e:
            raise EncodingError("Error when decoding") from e

        dict_payload = {"timestamp": pb_payload.timestamp, "metrics": []}
        if pb_payload.HasField("seq"):
            dict_payload["seq"] = pb_payload.seq
        for spb_metric in pb_payload.metrics:
            dict_payload["metrics"].append(self._decode_metric(spb_metric))

        return NodePayload.from_dict(dict_payload)
