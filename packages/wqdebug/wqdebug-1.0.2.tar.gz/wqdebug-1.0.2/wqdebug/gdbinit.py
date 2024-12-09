import os
import sys
import gdb


sys.path.append(os.path.dirname(__file__))

# ref https://sourceware.org/gdb/current/onlinedocs/gdb.html/Python-API.html
class Hello(gdb.Command):
    """
    gdb script test.
    """

    def __init__(self):
        super().__init__(self.__class__.__name__, gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        print("Hello, GDB World! \033[0;31;40m WuQi \033[0m")


Hello()

import wqgdb