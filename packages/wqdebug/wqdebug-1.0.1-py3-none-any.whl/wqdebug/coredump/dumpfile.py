import sys
import io
import struct
import base64
from .elf32 import *


def b64_decode(b64file) -> io.BytesIO:
    data = io.BytesIO()
    with open(b64file, "rb") as f:
        for line in f:
            try:
                d = base64.standard_b64decode(line.rstrip(b"\r\n"))
                data.write(d)
            except Exception as e:
                print(f"base64 decode fail at line {line.index}, {e}")
                data.write(b"\0" * 48)
    data.seek(0)
    return data


def alignup(x, align):
    return (x + (align - 1)) // align * align


class BinStruct(object):
    def __init__(self, buf=None):
        """Base constructor for binary structure objects"""
        if buf is None:
            buf = b"\0" * self.sizeof()
        fields = struct.unpack(self.__class__.format, buf[: self.sizeof()])
        self.__dict__.update(zip(self.__class__.fields, fields))

    @classmethod
    def sizeof(cls):
        """Returns the size of the structure represented by specific subclass"""
        return struct.calcsize(cls.format)

    def dump(self):
        """Returns binary representation of structure"""
        keys = self.__class__.fields
        return struct.pack(self.__class__.format, *(self.__dict__[k] for k in keys))

    def info(self):
        return ", ".join([f"{k}:0x{self.__dict__[k]:x}" for k in self.__class__.fields])


class DumpHeader(BinStruct):
    """Common dump header"""

    fields = ("data_len", "version", "tasks_num", "tcb_sz")
    format = "<4L"

    def __init__(self, buf=None):
        super(__class__, self).__init__(buf)


class DumpTask(BinStruct):
    """task dump header"""

    fields = ("tcb", "id", "stack_start", "stack_end")
    format = "<4L"

    def __init__(self, buf=None):
        super(__class__, self).__init__(buf)


class DumpSegment(BinStruct):
    """Segment dump header"""

    fields = ("flag", "id", "start", "end")
    format = "<4L"

    def __init__(self, buf=None):
        super(__class__, self).__init__(buf)


class DumpFileV1(object):
    def __init__(self, data: io.BytesIO, header: DumpHeader):
        self.tasks = []
        self.segments = []
        self.version = 1

        tcbsz = header.tcb_sz
        while data.tell() < header.data_len:
            task = DumpTask(data.read(DumpTask.sizeof()))
            task.tcb_data = data.read(tcbsz)
            task.stack = data.read(alignup(task.stack_end - task.stack_start, 4))
            self.tasks.append(task)

        # read segment
        d = data.read(DumpSegment.sizeof())
        while d:
            seg = DumpSegment(d)
            seg.data = data.read(seg.end - seg.start)
            self.segments.append(seg)

            d = data.read(DumpSegment.sizeof())

    def info(self):
        for t in self.tasks:
            print(f"task: {t.info()}")
        for s in self.segments:
            print(f"segment: {s.info()}")


class DumpFileV2(object):
    def __init__(self, data: io.BytesIO, header: DumpHeader):
        self.tasks = []
        self.segments = []
        self.version = 2

        tcbsz = header.tcb_sz
        if header.data_len > DumpHeader.sizeof():
            for i in range(header.tasks_num):
                task = DumpTask(data.read(DumpTask.sizeof()))
                task.stack = data.read(alignup(task.stack_end - task.stack_start, 4))
                self.tasks.append(task)

        # read segment
        d = data.read(DumpSegment.sizeof())
        while d:
            seg = DumpSegment(d)
            seg.data = data.read(seg.end - seg.start)
            self.segments.append(seg)

            d = data.read(DumpSegment.sizeof())

    def info(self):
        for t in self.tasks:
            print(f"task: {t.info()}")
        for s in self.segments:
            print(f"segment {s.info()}")


class DumpFile(object):
    def __init__(self, dump):
        self.data = b64_decode(dump)
        self.header = DumpHeader(self.data.read(DumpHeader.sizeof()))
        self.version = self.header.version

    def load(self):
        _ = [0, DumpFileV1, DumpFileV2]
        if self.version >= len(_):
            print(f"Core dump version {self.version} is not supported")
        return _[self.version](self.data, self.header)


if __name__ == "__main__":
    df = DumpFile(sys.argv[1])
    df.load().info()
