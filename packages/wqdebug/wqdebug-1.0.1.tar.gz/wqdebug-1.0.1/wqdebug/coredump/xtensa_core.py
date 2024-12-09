import sys
from ctypes import *
from .elf32 import *

from .dumpfile import DumpFile


class XtensaFrame(Structure):
    _pack_ = 4
    _fields_ = [
        ("version", c_uint32),
        ("pc", c_uint32),
        ("ar0", c_uint32),
        ("ar1", c_uint32),
        ("ar2", c_uint32),
        ("ar3", c_uint32),
        ("ar4", c_uint32),
        ("ar5", c_uint32),
        ("ar6", c_uint32),
        ("ar7", c_uint32),
        ("ar8", c_uint32),
        ("ar9", c_uint32),
        ("ar10", c_uint32),
        ("ar11", c_uint32),
        ("ar12", c_uint32),
        ("ar13", c_uint32),
        ("ar14", c_uint32),
        ("ar15", c_uint32),
        ("ar16", c_uint32),
        ("ar17", c_uint32),
        ("ar18", c_uint32),
        ("ar19", c_uint32),
        ("ar20", c_uint32),
        ("ar21", c_uint32),
        ("ar22", c_uint32),
        ("ar23", c_uint32),
        ("ar24", c_uint32),
        ("ar25", c_uint32),
        ("ar26", c_uint32),
        ("ar27", c_uint32),
        ("ar28", c_uint32),
        ("ar29", c_uint32),
        ("ar30", c_uint32),
        ("ar31", c_uint32),
        ("lbeg", c_uint32),
        ("lend", c_uint32),
        ("lcount", c_uint32),
        ("sar", c_uint32),
        ("windowbase", c_uint32),
        ("windowstart", c_uint32),
        ("configid0", c_uint32),
        ("configid1", c_uint32),
        ("ps", c_uint32),
        ("br", c_uint32),
        ("ae_ovf_sar", c_uint32),
        ("ae_bithead", c_uint32),
        ("ae_ts_fts_bu_bp", c_uint32),
        ("ae_cw_sd_no", c_uint32),
        ("ae_cbegin0", c_uint32),
        ("ae_cend0", c_uint32),
        ("ae_cbegin1", c_uint32),
        ("ae_cend1", c_uint32),
        ("ae_cbegin2", c_uint32),
        ("ae_cend2", c_uint32),
        ("aed0", c_uint64),
        ("aed1", c_uint64),
        ("aed2", c_uint64),
        ("aed3", c_uint64),
        ("aed4", c_uint64),
        ("aed5", c_uint64),
        ("aed6", c_uint64),
        ("aed7", c_uint64),
        ("aed8", c_uint64),
        ("aed9", c_uint64),
        ("aed10", c_uint64),
        ("aed11", c_uint64),
        ("aed12", c_uint64),
        ("aed13", c_uint64),
        ("aed14", c_uint64),
        ("aed15", c_uint64),
        ("aed16", c_uint64),
        ("aed17", c_uint64),
        ("aed18", c_uint64),
        ("aed19", c_uint64),
        ("aed20", c_uint64),
        ("aed21", c_uint64),
        ("aed22", c_uint64),
        ("aed23", c_uint64),
        ("aed24", c_uint64),
        ("aed25", c_uint64),
        ("aed26", c_uint64),
        ("aed27", c_uint64),
        ("aed28", c_uint64),
        ("aed29", c_uint64),
        ("aed30", c_uint64),
        ("aed31", c_uint64),
        ("u0", c_uint32 * 4),
        ("u1", c_uint32 * 4),
        ("u2", c_uint32 * 4),
        ("u3", c_uint32 * 4),
        ("aep0", c_uint8),
        ("aep1", c_uint8),
        ("aep2", c_uint8),
        ("aep3", c_uint8),
        ("ae_zbiasv8c", c_uint32),
        ("fcr_fsr", c_uint32),
        ("ibreakenable", c_uint32),
        ("memctl", c_uint32),
        ("ddr", c_uint32),
        ("ibreaka0", c_uint32),
        ("ibreaka1", c_uint32),
        ("dbreaka0", c_uint32),
        ("dbreaka1", c_uint32),
        ("dbreakc0", c_uint32),
        ("dbreakc1", c_uint32),
        ("epc1", c_uint32),
        ("epc2", c_uint32),
        ("epc3", c_uint32),
        ("epc4", c_uint32),
        ("depc", c_uint32),
        ("eps2", c_uint32),
        ("eps3", c_uint32),
        ("eps4", c_uint32),
        ("excsave1", c_uint32),
        ("excsave2", c_uint32),
        ("excsave3", c_uint32),
        ("excsave4", c_uint32),
        ("cpenable", c_uint32),
        ("interrupt", c_uint32),
        ("intset", c_uint32),
        ("intclear", c_uint32),
        ("intenable", c_uint32),
        ("vecbase", c_uint32),
        ("exccause", c_uint32),
        ("debugcause", c_uint32),
        ("ccount", c_uint32),
        ("prid", c_uint32),
        ("icount", c_uint32),
        ("icountlevel", c_uint32),
        ("excvaddr", c_uint32),
        ("ccompare0", c_uint32),
        ("ccompare1", c_uint32),
    ]


class XtensaStack(Structure):
    _pack_ = 4
    _fields_ = [
        ("exit", c_uint32),
        ("pc", c_uint32),
        ("ps", c_uint32),
        ("ar0", c_uint32),
        ("ar1", c_uint32),
        ("ar2", c_uint32),
        ("ar3", c_uint32),
        ("ar4", c_uint32),
        ("ar5", c_uint32),
        ("ar6", c_uint32),
        ("ar7", c_uint32),
        ("ar8", c_uint32),
        ("ar9", c_uint32),
        ("ar10", c_uint32),
        ("ar11", c_uint32),
        ("ar12", c_uint32),
        ("ar13", c_uint32),
        ("ar14", c_uint32),
        ("ar15", c_uint32),
        ("sar", c_uint32),
        ("exccause", c_uint32),
        ("excvaddr", c_uint32),
        ("lbeg", c_uint32),
        ("lend", c_uint32),
        ("lcount", c_uint32),
        ("tmp0", c_uint32),
        ("tmp1", c_uint32),
        ("tmp2", c_uint32),
        ("pad", c_uint32 * 4),
        ("extra", c_uint32 * 8),
    ]


class XtensaCoreFile(Elf):
    def __init__(self):
        super().__init__()
        self.header.e_type = ElfHeader.ET_CORE
        self.header.e_machine = ElfHeader.EM_XTENSA
        self.core = None
        self.gdb = "xt-gdb"

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

    def _save_v1(self, name):
        pass

    def _save_v2(self, name):
        """First program segment is 'note0' with main frame
        other program are data
        """
        self.header.e_version = 1
        note = io.BytesIO()

        # WQ dump version note
        note.write(
            ElfNote(
                "WQDUMP", ElfNote.NT_WQDUMP_VRE, bytearray(c_int32(self.version))
            ).dump()
        )

        if self.df.tasks:
            stack_data = self.frame_data(self.df.tasks[0].stack)
            # note.write(ElfNote("note0", ElfNote.NT_FPREGSET, stack_data).dump())
            note.write(ElfNote("note0", 3, stack_data).dump())

            note.seek(0)
            self.add_program_segment(
                0, ElfProgram.PT_NOTE, ElfProgram.PF_R, note.read()
            )

        for seg in self.df.segments:
            self.add_program_segment(
                seg.start,
                ElfProgram.PT_LOAD,
                ElfProgram.PF_R | ElfProgram.PF_W | ElfProgram.PF_X,
                seg.data,
            )
        self.dump(name)

    def frame_data(self, stack):
        xs = XtensaStack.from_buffer_copy(stack)
        xf = XtensaFrame()
        for f in xs._fields_:
            if f in xf._fields_:
                xf.__setattr__(f[0], getattr(xs, f[0]))

        # crashed and some running tasks (e.g. prvIdleTask) have EXCM bit set
        # and GDB can not unwind callstack properly (it implies not windowed call0)
        if xf.ps & (1 << 5):
            xf.ps &= ~(1 << 4)

        xf.version = 1
        return bytearray(xf)

    def save(self, name):
        if self.version == 1:
            return self._save_v1(name)
        return self._save_v2(name)

    @property
    def gdb_arg(self):
        arg = [
            self.gdb,
        ]

        if self.version == 1:
            return arg
        elif self.version == 2:
            arg.append('--init-eval-command=py import thread_aware_rtos')
            return arg
