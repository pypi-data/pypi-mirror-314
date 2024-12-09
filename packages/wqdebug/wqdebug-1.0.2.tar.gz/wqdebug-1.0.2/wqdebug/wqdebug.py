from wqdebug._version import __version__

import os
import sys
import re
import shutil
import argparse
import traceback
import tarfile
import glob
import platform
import requests
import zipfile
import json
#import wq_coredump
from wqdebug.coredump.elf32 import *
from wqdebug.coredump.corefile import *

class WqDebug:
    def __init__(self, log: str = "", wpk: str = "", elf: str = ""):
        self.log = log
        self.wpk = wpk
        self.elf = elf
        self.dumps = {}
        self.dumps_index = 0
        if self.log == "":
            self.log = os.path.realpath("test/test.log")

    def start(self):
        if self.select_log_file():
            if self.find_coredump():
                self.select_coredump()

    def select_log_file(self):
        user_input = input(
            f"log:\n{self.log}\n请拖入LOG文件或输入文件路径, 输入回车Enter使用推荐文件:\n"
        )
        if user_input:
            self.log = user_input
            while not os.path.isfile(self.log):
                print("文件路径不存在，请重新输入。")
                self.select_log_file()
        return True

    @staticmethod
    def serach_elf_file(core: str, log_path: str, wpk_path: str):
        print(f"serach_elf_file {core} {log_path} {wpk_path}")
        core_name_mapping = {"acore": "core0", "bcore": "core1", "dcore": "core4"}
        core_name = core_name_mapping.get(core, "core0")
        
        # 规范化路径
        log_path = os.path.normpath(log_path)
        wpk_path = os.path.normpath(wpk_path)
        
        # 构建搜索路径列表
        file_paths = [
            os.path.join(os.path.dirname(log_path), f"*_{core.lower()}.elf"),  # opencore
            os.path.join(os.path.dirname(log_path), f"*_{core_name.lower()}.elf"),  # ADK
            os.path.join(os.path.dirname(wpk_path), f"*_{core_name.lower()}.elf"),  # ADK
            os.path.join(os.path.dirname(wpk_path), f"*_{core.lower()}.elf"),  # opencore
            os.path.join(os.path.dirname(wpk_path), core_name, f"*_{core_name.lower()}.elf"),  # ADK
            os.path.join(
                os.path.dirname(wpk_path).replace("package", "bin"),
                "tws_2_0",
                core.lower(),
                f"*_{core.lower()}.elf",
            ),  # opencore
        ]
        
        # 遍历所有可能的路径
        for file_path in file_paths:
            # 转换为系统适用的路径格式
            file_path = os.path.normpath(file_path)
            print(f"Searching in: {file_path}")
            
            # 使用glob搜索文件
            matches = glob.glob(file_path, recursive=True)
            print(f"Found matches: {matches}")
            
            # 返回第一个有效的文件
            for match in matches:
                if os.path.isfile(match):
                    return match
        
        print("No matching ELF file found")
        return None

    def select_elf_file(self, core="core0"):
        # print(f"select_elf_file {core}")
        if not os.path.isfile(self.elf):
            self.elf = self.serach_elf_file(core, self.log, self.wpk)
        user_input = input(
            f"elf:\n{self.elf}\n请拖入ELF文件或输入文件路径, 输入回车Enter使用推荐文件:\n"
        )

        if user_input:
            self.elf = user_input
            while not os.path.isfile(self.elf) or not self.elf.split(".")[-1] == "elf":
                print("无效的ELF文件，请重新输入。")
                self.select_elf_file("")
        return self.elf

    def find_coredump(self):
        rc_mcause_coredump_old = re.compile(
            r"[\[|【].*?([m|c]cause: .*?)\n[\s\S]*?"
            r"================= CORE DUMP START =================([\s\S]*?)"
            r"================= CORE DUMP END ================="
        )
        rc_mcause_coredump = re.compile(
            r"[\[|【]([A|B|D]).*?([m|c]cause: .*?)\n[\s\S]*?"
            r"================= CORE\d? DUMP START =================([\s\S]*?)"
            r"================= CORE\d? DUMP END ================="
        )
        rc_time_coredump = re.compile(r".*?>")
        rc_time_coredump_old = re.compile(r".*?\] ")
        with open(self.log, "r", encoding="utf-8", errors="ignore") as f:
            log_data_all = f.read()
            print(f"正在查找LOG文件中的coredump信息...")
            log_data_list = log_data_all.split("Core dump has written to uart")
            found_coredump = False
            index = 0
            for log_data in log_data_list:
                # print("log_data=", log_data[0:128])
                match_list = rc_mcause_coredump.finditer(log_data)
                for m in match_list:
                    reason = f"{index}. {m.group(1)}core {m.group(2)}"
                    print(reason)
                    self.dumps[reason] = re.sub(
                        rc_time_coredump_old,
                        "",
                        re.sub(rc_time_coredump, "", m.group(3)),
                    )
                    found_coredump = True
                    index += 1
                    if index >= 2:
                        break
            if not found_coredump:
                print(f"正在查找rc_mcause_coredump_old...")
                for log_data in log_data_list:
                    # print("log_data=", log_data[0:128])
                    match_list = rc_mcause_coredump_old.finditer(log_data)
                    for m in match_list:
                        reason = f"{index}. {m.group(1)}"
                        print(reason)
                        self.dumps[reason] = re.sub(
                            rc_time_coredump_old,
                            "",
                            re.sub(rc_time_coredump, "", m.group(2)),
                        )
                    found_coredump = True
                    index += 1
                    if index >= 2:
                        break

            if not found_coredump:
                print(f"{self.log} LOG 文件无效，未找到有效的coredump信息。")
            else:
                print(f"找到 {len(self.dumps)} 个coredump信息")
                return True

    def get_core_name(self, dump):
        rc_core_name = re.compile(r"([A|B|D])core")
        # print(rc_core_name, dump)
        core_name = re.search(rc_core_name, dump)
        if core_name:
            return core_name.group()
        return "acore"
    
    @staticmethod
    def get_machine(program):
        with open(program, "rb") as f:
            eh = ElfHeader.from_buffer_copy(f.read(sizeof(ElfHeader)))
            if eh.e_machine == ElfHeader.EM_XTENSA:
                return "xtensa"
            else:
                return "riscv"

    def select_coredump(self):
        user_input = input(f"\n请输入 coredump 编号, 输入回车Enter使用默认0\n:")
        if not user_input:
            self.dumps_index = 0
            print(f"{list(self.dumps.keys())[self.dumps_index]}")
        elif user_input.isdigit() and 0 <= int(user_input) < len(self.dumps):
            self.dumps_index = int(user_input)
            print(f"{list(self.dumps.keys())[self.dumps_index]}")
        else:
            print(f"请输入是介于 0 到 {len(self.dumps) - 1} 之间的数字")
            self.select_coredump()

        core_name = self.get_core_name(list(self.dumps.keys())[self.dumps_index])
        elf = self.select_elf_file(core_name)
        if not os.path.exists("temp"):
            os.makedirs("temp")
        shutil.copy(elf, f"temp/coredump_{core_name}.elf")

        reason = list(self.dumps.keys())[self.dumps_index]
        with open(os.path.join(f"temp/coredump_{core_name}.b64"), "w") as f:
            f.write(self.dumps[reason].strip())

        coredump_elf = f"temp/coredump_{core_name}.elf"
        coredump_bin = f"temp/coredump_{core_name}.bin"
        machine = self.get_machine(coredump_elf)
        cf = CoreFile(machine=machine)
        cf.load(dumpfile=f"temp/coredump_{core_name}.b64")
        cf.save(coredump_bin)

        
        gdbinit = "gdbinit.py"
       
        if platform.system() == "Windows":
            gdb = "tools/riscv/windows/riscv32-esp-elf-gdb/bin/riscv32-esp-elf-gdb.exe"
            if not os.path.isfile(gdb):
                self.download_gdb()
            cmd = (
                f"start powershell echo '\033[91m {reason} \033[0m';"
                f"{gdb} --command=gdbinit.py -core='{coredump_bin}' {coredump_elf}"
            )
        else:
            gdb = "tools/riscv/linux/riscv32-esp-elf-gdb/bin/riscv32-esp-elf-gdb"
            if not os.path.isfile(gdb):
                self.download_gdb()
            cmd = (f"echo '\033[91m {reason} \033[0m';" 
                   f"{gdb} --command=gdbinit.py -core={coredump_bin} {coredump_elf}")
        print(cmd)
        os.system(cmd)
        sys.exit(0)

    @staticmethod
    def download_gdb():
        print(f"download gdb {platform.system()} {platform.machine()}")
        this_dir = os.path.dirname(__file__)
        
        # 读取tools.json配置
        with open(os.path.join(this_dir, "tools.json"), "r") as f:
            tools_config = json.loads(f.read())
        
        # 获取RISC-V GDB配置
        riscv_gdb = next(tool for tool in tools_config["tools"] if "RISC-V" in tool["description"])
        
        # 根据系统选择下载URL
        if platform.system() == "Windows":
            if platform.machine().endswith('64'):
                platform_key = "win64"
            else:
                platform_key = "win32"
            local_gdb = os.path.join(this_dir,"tools", "riscv", "windows")
        else:
            if platform.machine() == "x86_64":
                platform_key = "linux-amd64"
            else:
                platform_key = "linux-i686"
            local_gdb = os.path.join(this_dir,"tools", "riscv", "linux")
        
        version = riscv_gdb["versions"][0]
        gdb_info = version[platform_key]
        gdb_path = gdb_info["url"]
        
        if not os.path.exists(local_gdb):
            print("未找到GDB，开始下载...")
            os.makedirs(local_gdb, exist_ok=True)
            
            # 使用requests下载文件并显示进度
            response = requests.get(gdb_path, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 KB
            downloaded = 0
            
            local_file = os.path.join(this_dir, os.path.basename(gdb_path))
            
            with open(local_file, 'wb') as f:
                for data in response.iter_content(block_size):
                    downloaded += len(data)
                    f.write(data)
                    
                    # 计算下载进度百分比
                    if total_size > 0:
                        percent = int(downloaded * 100 / total_size)
                        bar_length = 50
                        filled_length = int(bar_length * percent / 100)
                        bar = '=' * filled_length + '-' * (bar_length - filled_length)
                        
                        # 计算下载速度和已下载大小
                        downloaded_mb = downloaded / (1024 * 1024)
                        total_mb = total_size / (1024 * 1024)
                        
                        print(f'\r下载进度: [{bar}] {percent}% {downloaded_mb:.1f}MB/{total_mb:.1f}MB', end='')
            
            print("\n下载完成，正在解压...")
            if local_file.endswith(".zip"):
                with zipfile.ZipFile(local_file, 'r') as zip_ref:
                    zip_ref.extractall(local_gdb)
            else:
                with tarfile.open(local_file, 'r:gz') as tar:
                    tar.extractall(local_gdb)
            
            os.remove(local_file)
            print("GDB安装完成")

def main():
    print(f"wq debug v:{__version__}")
    os.chdir(os.path.dirname(__file__))
    print(sys.argv)
    try:
        parser = argparse.ArgumentParser(description=f"wq debug v:{__version__}")
        parser.add_argument(
            "-l",
            "--log",
            help="log file path",
            nargs="?",
            const="",
            type=str,
            default="",
        )
        parser.add_argument("-e", "--elf", help="elf file path", type=str, default="")
        parser.add_argument(
            "-w",
            "--wpk",
            help="wpk file path, infer the elf file path from the wpk file path",
            nargs="?",
            const="",
            type=str,
            default="",
        )
        args = parser.parse_args()
        # print(args.log, args.wpk, args.elf)
        wq_debug = WqDebug(args.log, args.wpk, args.elf)
        wq_debug.start()
    except Exception as e:
        print(e)
        traceback.print_exc()
        input("请按下回车键退出...")

if __name__ == "__main__":
    main()