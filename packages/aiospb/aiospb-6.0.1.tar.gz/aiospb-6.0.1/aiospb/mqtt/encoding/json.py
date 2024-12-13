import json

from .. import HostPayload, MessageEncoder, NodePayload, Payload


class JsonEncoder(MessageEncoder):
    """Encoder of messages for testing purposes"""

    def encode(self, payload: Payload) -> bytes:
        """Convert a payload dict to a string for publishing"""

        return json.dumps(payload.to_dict(), sort_keys=True).encode("utf-8")

    def decode(self, payload: bytes) -> Payload:
        """Convert payload to a payload dict"""
        payload_map = json.loads(payload.decode("utf-8"))
        if "online" in payload_map:
            return HostPayload.from_dict(payload_map)
        else:
            return NodePayload.from_dict(payload_map)
