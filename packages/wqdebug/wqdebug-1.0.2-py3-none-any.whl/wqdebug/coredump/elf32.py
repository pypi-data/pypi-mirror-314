import io
import struct

from ctypes import *

def dump_struct(struct: Structure):
    info = {}
    for k, v in struct._fields_:
        av = getattr(struct, k)
        if type(v) == type(Structure):
            av = dump_struct(av)
        elif type(v) == type(Array):
            av = cast(av, c_char_p).value.decode()
        else:
            pass
        info[k] = av
    return info


class ElfNote(object):
    NT_VERSION = 0x1
    NT_PRSTATUS = 0x1
    NT_FPREGSET = 0x2
    NT_PRPSINFO = 0x3
    NT_PRXREG = 0x4
    NT_TASKSTRUCT = 0x4
    NT_PLATFORM = 0x5

    NT_RISCV_CSR = 0x900
    NT_RISCV_VECTOR = 0x901

    # private define
    NT_WQDUMP_VRE = 0x57714470

    def __init__(self, name, type, desc):
        self.name = bytearray(name, encoding="ascii") + b"\0"
        self.type = type
        self.desc = desc

    def dump(self):
        hdr = struct.pack("<LLL", len(self.name), len(self.desc), self.type)
        # pad for 4 byte alignment
        name = self.name + ((4 - len(self.name)) % 4) * b"\0"
        desc = self.desc + ((4 - len(self.desc)) % 4) * b"\0"
        return hdr + name + desc

class ElfProgram(Structure):
    PT_NULL = 0
    PT_LOAD = 1
    PT_DYNAMIC = 2
    PT_INTERP = 3
    PT_NOTE = 4
    PT_SHLIB = 5
    PT_PHDR = 6
    PT_TLS = 7

    PF_X = 1
    PF_W = 2
    PF_R = 4

    _pack_ = 4
    _fields_ = [
        ("p_type", c_uint32),
        ("p_offset", c_uint32),
        ("p_vaddr", c_uint32),
        ("p_paddr", c_uint32),
        ("p_filesz", c_uint32),
        ("p_memsz", c_uint32),
        ("p_flags", c_uint32),
        ("p_align", c_uint32),
    ]


class ElfHeader(Structure):
    E_IDNET = b"\x7fELF\1\1\1"

    # e_type in the ELF header
    ET_NONE = 0
    ET_REL = 1
    ET_EXEC = 2
    ET_DYN = 3
    ET_CORE = 4
    ET_LOPROC = 0xFF00
    ET_HIPROC = 0xFFFF

    # e_machine in the ELF header
    EM_NONE = 0  # No machine
    EM_XTENSA = 94  # Tensilica Xtensa Architecture
    EM_RISCV = 243  # RISC-V

    _pack_ = 4
    _fields_ = [
        ("e_ident", c_char * 16),
        ("e_type", c_uint16),
        ("e_machine", c_uint16),
        ("e_version", c_uint32),
        ("e_entry", c_uint32),
        ("e_phoff", c_uint32),
        ("e_shoff", c_uint32),
        ("e_flags", c_uint32),
        ("e_ehsize", c_uint16),
        ("e_phentsize", c_uint16),
        ("e_phnum", c_uint16),
        ("e_shentsize", c_uint16),
        ("e_shnum", c_uint16),
        ("e_shstrndx", c_uint16),
    ]


class Elf(object):
    def __init__(self):
        self.header = ElfHeader()
        self.header.e_phoff = sizeof(ElfHeader)
        self.header.e_ident = ElfHeader.E_IDNET
        self.header.e_ehsize = sizeof(ElfHeader)

        self.p_seg = []

    def add_program_segment(self, addr, type, flags, data):
        phdr = ElfProgram()
        phdr.p_type = type
        phdr.p_vaddr = addr
        phdr.p_paddr = 0
        phdr.p_filesz = len(data)
        phdr.p_memsz = phdr.p_filesz
        phdr.p_flags = flags
        phdr.p_align = 1
        phdr.data = data

        self.p_seg.append(phdr)

    def dump(self, name):
        self.header.e_phentsize = sizeof(ElfProgram)
        self.header.e_phnum = len(self.p_seg)

        # calc p_offset for all segment
        offset = self.header.e_ehsize + self.header.e_phentsize * self.header.e_phnum
        for phdr in self.p_seg:
            phdr.p_offset = offset
            offset += len(phdr.data)

        with open(name, "wb") as elf:
            elf.write(bytearray(self.header))

            for phdr in self.p_seg:
                elf.write(bytearray(phdr))
            for phdr in self.p_seg:
                elf.write(phdr.data)

    def load(self, name):
        with open(name, "rb") as f:
            self.header = ElfHeader.from_buffer_copy(f.read(sizeof(ElfHeader)))

            for i in range(self.header.e_phnum):
                self.p_seg.append(
                    ElfProgram.from_buffer_copy(f.read(sizeof(ElfProgram)))
                )

            for i in range(self.header.e_phnum):
                data_len = (
                    self.p_seg[i + 1].p_offset - self.p_seg[i].p_offset
                    if i < self.header.e_phnum - 1
                    else 0
                )
                self.p_seg[i].data = f.read() if data_len == 0 else f.read(data_len)


class ElfSiginfo(Structure):
    """
    struct elf_siginfo
    {
        int	si_signo;			/* signal number */
        int	si_code;			/* extra code */
        int	si_errno;			/* errno */
    };
    """

    _pack_ = 4
    _fields_ = [
        ("si_signo", c_int32),
        ("si_code", c_int32),
        ("si_errno", c_int32),
    ]


class ElfPRStatus32(Structure):
    """
    struct elf_prstatus32
    {
        struct elf_siginfo pr_info;		/* Info associated with signal.  */
        short int pr_cursig;			/* Current signal.  */
        unsigned int pr_sigpend;		/* Set of pending signals.  */
        unsigned int pr_sighold;		/* Set of held signals.  */
        pid_t pr_pid;
        pid_t pr_ppid;
        pid_t pr_pgrp;
        pid_t pr_sid;
        struct prstatus32_timeval pr_utime;		/* User time.  */
        struct prstatus32_timeval pr_stime;		/* System time.  */
        struct prstatus32_timeval pr_cutime;	/* Cumulative user time.  */
        struct prstatus32_timeval pr_cstime;	/* Cumulative system time.  */
        elf_gregset32_t pr_reg;		/* GP registers.  */
        int pr_fpvalid;			/* True if math copro being used.  */
    };
    """

    _pack_ = 4
    _fields_ = [
        ("pr_info", ElfSiginfo),
        ("pr_cursig", c_int16),
        ("pr_sigpend", c_uint32),
        ("pr_sighold", c_uint32),
        ("pr_pid", c_uint32),
        ("pr_ppid", c_uint32),
        ("pr_pgrp", c_uint32),
        ("pr_sid", c_uint32),
        ("pr_utime", c_uint64),
        ("pr_stime", c_uint64),
        ("pr_cutime", c_uint64),
        ("pr_cstime", c_uint64),
    ]
