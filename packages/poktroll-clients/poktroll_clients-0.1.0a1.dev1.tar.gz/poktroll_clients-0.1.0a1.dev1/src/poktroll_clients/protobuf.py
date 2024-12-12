from dataclasses import dataclass
from typing import List

from poktroll_clients.ffi import ffi


@dataclass
class SerializedProto:
    """
    Represents a serialized protobuf message with its type URL and binary data.
    Handles conversion to C structures while ensuring proper memory management.
    """
    type_url: str
    data: bytes

    def to_c_struct(self) -> ffi.CData:
        """
        Converts the Python protobuf data to a C struct while preserving the underlying memory.
        Returns a C serialized_proto struct pointer.
        """
        serialized_proto = ffi.new("serialized_proto *")

        # Create buffers and store them as instance attributes to prevent GC
        self._type_url_bytes = self.type_url.encode('utf-8')
        self._type_url_buffer = ffi.new("uint8_t[]", self._type_url_bytes)
        self._data_buffer = ffi.new("uint8_t[]", self.data)

        # Assign the buffers to the C struct
        serialized_proto.type_url = self._type_url_buffer
        serialized_proto.type_url_length = len(self._type_url_bytes)
        serialized_proto.data = self._data_buffer
        serialized_proto.data_length = len(self.data)

        return serialized_proto


@dataclass
class ProtoMessageArray:
    """
    Represents an array of serialized protobuf messages.
    Handles conversion to C structures while ensuring proper memory management.
    """
    messages: List[SerializedProto]

    def to_c_struct(self) -> ffi.CData:
        """
        Converts the Python protobuf message array to a C struct while preserving the underlying memory.
        Returns a C proto_message_array struct pointer.
        """
        # Create the array structure
        proto_message_array = ffi.new("proto_message_array *")
        proto_message_array.num_messages = len(self.messages)

        # Allocate the array of message structures
        proto_message_array.messages = ffi.new("serialized_proto[]", len(self.messages))

        # Convert each message and store C structs as instance attributes
        self._message_structs = []
        for i, msg in enumerate(self.messages):
            # Create and store the C struct for this message
            c_msg = msg.to_c_struct()
            self._message_structs.append(c_msg)

            # Copy the data to the array
            proto_message_array.messages[i].type_url = c_msg.type_url
            proto_message_array.messages[i].type_url_length = c_msg.type_url_length
            proto_message_array.messages[i].data = c_msg.data
            proto_message_array.messages[i].data_length = c_msg.data_length

        return proto_message_array
