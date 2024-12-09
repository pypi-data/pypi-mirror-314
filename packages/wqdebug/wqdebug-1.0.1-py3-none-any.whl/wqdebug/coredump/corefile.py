import os
import sys
import tempfile
import subprocess

from .xtensa_core import XtensaCoreFile
from .riscv_core import RiscvCoreFile


class CoreFile(object):
    def __init__(self, machine):
        self.machine = machine
        _ = {"riscv": RiscvCoreFile, "xtensa": XtensaCoreFile}
        self.cf = _[self.machine]()

    def load(self, **kwarg):
        self.cf.load(**kwarg)

    def save(self, name="core.bin"):
        self.cf.save(name)

    def dbg_start(self, program):
        self.program = program

        tmp = tempfile.mktemp()
        self.cf.save(tmp)

        gdb_args = self.cf.gdb_arg
        gdb_args.extend([
            "-x",
            os.path.join(os.path.dirname(sys.argv[0]), "gdbinit"), # sya.argv[0] is where the wq_debug at.
            f"--core={tmp}",
            program,
        ])

        gdb_env = os.environ.copy()
        gdb_env['WQCOREDUMPPATH'] = os.path.dirname(sys.argv[0])
        gdb_env['XTENSA_CORE'] = 'wq_hifi5_asic'

        p = subprocess.Popen(
            bufsize=0,
            args=gdb_args,
            stdin=None,
            stdout=None,
            stderr=None,
            close_fds=os.name == "nt",
            env=gdb_env,
        )
        p.wait()

        os.unlink(tmp)
