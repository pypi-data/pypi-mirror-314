import sys
import io
import shutil

from ctypes import *
from .elf32 import *

from .dumpfile import DumpFile


def alignup(x, align):
    return (x + (align - 1)) // align * align


class RiscvUserRegStruct(Structure):
    _pack_ = 4
    _fields_ = [
        ("pc", c_uint32),
        ("ra", c_uint32),
        ("sp", c_uint32),
        ("gp", c_uint32),
        ("tp", c_uint32),
        ("t0", c_uint32),
        ("t1", c_uint32),
        ("t2", c_uint32),
        ("s0", c_uint32),
        ("s1", c_uint32),
        ("a0", c_uint32),
        ("a1", c_uint32),
        ("a2", c_uint32),
        ("a3", c_uint32),
        ("a4", c_uint32),
        ("a5", c_uint32),
        ("a6", c_uint32),
        ("a7", c_uint32),
        ("s2", c_uint32),
        ("s3", c_uint32),
        ("s4", c_uint32),
        ("s5", c_uint32),
        ("s6", c_uint32),
        ("s7", c_uint32),
        ("s8", c_uint32),
        ("s9", c_uint32),
        ("u10", c_uint32),
        ("u11", c_uint32),
        ("t3", c_uint32),
        ("t4", c_uint32),
        ("t5", c_uint32),
        ("t6", c_uint32),
    ]


class RiscvStack(Structure):
    """
    reference from exception.h
    typedef struct trap_stack_registers {
        uint32_t mepc;
        uint32_t flr[32];
        uint32_t ra;
        uint32_t sp;
        uint32_t gp;
        uint32_t tp;
        uint32_t t0_2[3];
        uint32_t fp;
        uint32_t s1;
        uint32_t a0_7[8];
        uint32_t s2_11[10];
        uint32_t t3_6[4];
        uint32_t mstatus;
    } trap_stack_registers_t;
    """

    _pack_ = 4
    _fields_ = [
        ("pc", c_uint32),
        ("flr", c_uint32 * 32),
        ("ra", c_uint32),
        ("sp", c_uint32),
        ("gp", c_uint32),
        ("tp", c_uint32),
        ("t0", c_uint32),
        ("t1", c_uint32),
        ("t2", c_uint32),
        ("s0", c_uint32),
        ("s1", c_uint32),
        ("a0", c_uint32),
        ("a1", c_uint32),
        ("a2", c_uint32),
        ("a3", c_uint32),
        ("a4", c_uint32),
        ("a5", c_uint32),
        ("a6", c_uint32),
        ("a7", c_uint32),
        ("s2", c_uint32),
        ("s3", c_uint32),
        ("s4", c_uint32),
        ("s5", c_uint32),
        ("s6", c_uint32),
        ("s7", c_uint32),
        ("s8", c_uint32),
        ("s9", c_uint32),
        ("u10", c_uint32),
        ("u11", c_uint32),
        ("t3", c_uint32),
        ("t4", c_uint32),
        ("t5", c_uint32),
        ("t6", c_uint32),
        ("mstatus", c_uint32),
    ]

class RiscvStack2(Structure):
    """
    reference from exception.h
    typedef struct trap_stack_registers {
        uint32_t mepc;
        uint32_t flr[32];
        uint32_t ra;
        uint32_t t0_2[3];
        uint32_t fp;
        uint32_t s1;
        uint32_t a0_7[8];
        uint32_t s2_11[10];
        uint32_t t3_6[4];
        uint32_t mstatus;
    } trap_stack_registers_t;
    """

    _pack_ = 4
    _fields_ = [
        ("pc", c_uint32),
        ("flr", c_uint32 * 32),
        ("ra", c_uint32),
        ("t0", c_uint32),
        ("t1", c_uint32),
        ("t2", c_uint32),
        ("s0", c_uint32),
        ("s1", c_uint32),
        ("a0", c_uint32),
        ("a1", c_uint32),
        ("a2", c_uint32),
        ("a3", c_uint32),
        ("a4", c_uint32),
        ("a5", c_uint32),
        ("a6", c_uint32),
        ("a7", c_uint32),
        ("s2", c_uint32),
        ("s3", c_uint32),
        ("s4", c_uint32),
        ("s5", c_uint32),
        ("s6", c_uint32),
        ("s7", c_uint32),
        ("s8", c_uint32),
        ("s9", c_uint32),
        ("u10", c_uint32),
        ("u11", c_uint32),
        ("t3", c_uint32),
        ("t4", c_uint32),
        ("t5", c_uint32),
        ("t6", c_uint32),
        ("mstatus", c_uint32),
    ]


class ElfPRStatus32Riscv(Structure):
    _pack_ = 4
    _fields_ = [
        ("prstatus_common", ElfPRStatus32),
        ("pr_reg", RiscvUserRegStruct),
        ("pr_fpvalid", c_int),
    ]


class RiscvCoreFile(Elf):
    def __init__(self):
        super().__init__()
        self.header.e_type = ElfHeader.ET_CORE
        self.header.e_machine = ElfHeader.EM_RISCV
        self.core = None
        self.gdb = "riscv64-unknown-elf-gdb"

    def load(self, corefile=None, dumpfile=None):
        if dumpfile is not None:
            self.df = DumpFile(dumpfile).load()
            self.version = self.df.version
            return

        if corefile is not None:
            self.core = corefile

            # read version
            elf = Elf()
            elf.load(corefile)
            note = None
            for p in elf.p_seg:
                if p.p_type == ElfProgram.PT_NOTE:
                    note = p.data

            if not note:
                print("No note section found in core file!")
                sys.exit(-1)

            off = 0
            while off < len(note):
                ns, ds, t = struct.unpack("<LLL", note[off : off + 12])
                off += 12
                name = note[off : off + ns]
                off += alignup(ns, 4)
                desc = note[off : off + ds]
                off += alignup(ds, 4)

                if t == ElfNote.NT_WQDUMP_VRE:
                    self.version = c_int.from_buffer_copy(desc).value
                    break

    def save(self, name):
        if self.core:
            if self.core != name:
                shutil.copyfile(self.core, name)
            return

        self.df.info()

        self.header.e_version = 1
        note = io.BytesIO()

        # WQ dump version note
        note.write(
            ElfNote(
                "WQDUMP", ElfNote.NT_VERSION, bytearray(c_int32(self.version))
            ).dump()
        )

        for i, task in enumerate(self.df.tasks):
            prs = ElfPRStatus32Riscv()
            prs.prstatus_common.pr_cursig = 0
            prs.prstatus_common.pr_pid = task.tcb
            prs.pr_reg = self.prreg_data(task.stack)
            prs.pr_fpvalid = 1

            note.write(ElfNote("CORE", ElfNote.NT_PRSTATUS, bytearray(prs)).dump())

        note.seek(0)
        self.add_program_segment(0, ElfProgram.PT_NOTE, ElfProgram.PF_R, note.read())

        # sys stack data
        t = self.df.tasks[0]
        self.add_program_segment(
            t.stack_start,
            ElfProgram.PT_LOAD,
            ElfProgram.PF_R | ElfProgram.PF_W | ElfProgram.PF_X,
            t.stack,
        )

        for seg in self.df.segments:
            self.add_program_segment(
                seg.start,
                ElfProgram.PT_LOAD,
                ElfProgram.PF_R | ElfProgram.PF_W | ElfProgram.PF_X,
                seg.data,
            )
        self.dump(name)

    def prreg_data(self, stack):
        if self.version == 1:
            rs = RiscvStack.from_buffer_copy(stack)
        else:
            rs = RiscvStack2.from_buffer_copy(stack)

        ru = RiscvUserRegStruct()

        for f in rs._fields_:
            if f in ru._fields_:
                ru.__setattr__(f[0], getattr(rs, f[0]))
        return ru

    @property
    def gdb_arg(self):
        arg = [self.gdb]

        return arg
