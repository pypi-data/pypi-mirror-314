from pathlib import Path
from typing import Type

from rosbags.highlevel import AnyReader

from autonomous_proto import autonomous_proto

def read_msgs(path: Path,
              topics: list[str],
              start: int | None = None,
              stop: int | None = None,
              ):
    with AnyReader([path.expanduser()]) as reader:
        connections = [ x for x in reader.connections if x.topic in topics ]
        for connection, timestamp, rawdata in reader.messages(connections=connections, start=start, stop=stop):
            yield timestamp, reader.deserialize(rawdata, connection.msgtype)

def get_proto(ros_msg,
              proto_type: Type[autonomous_proto],
              ):
    if hasattr(ros_msg, 'data'):
        return proto_type.FromString(bytes(ros_msg.data))
    return proto_type()

def read_protos(path: Path,
                topics: list[str],
                proto_type: Type[autonomous_proto],
                start: int | None = None,
                stop: int | None = None,
                ):
    for timestamp, ros_msg in read_msgs(path, topics, start, stop):
        yield timestamp, get_proto(ros_msg, proto_type)


if __name__ == "__main__":
    pass
