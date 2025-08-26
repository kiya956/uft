import os
import re

from unified_flash.command import syscmd
from unified_flash.err import FAILED, SUCCESS

def notify_and_wait():
    print("\n" + "="*50)
    print(" Notice: Please put your device into download mode")
    print("="*50)
    input("Press Enter to continue...\n")

def provision_handler(data):

    notify_and_wait()
    match data["provision"]:
        case "uuu":
            try:
                lst_file = next(
                    f for f in os.listdir("./")
                    if re.search(r".*\.lst$", f)
                )
            except StopIteration:
                print("uuu lst file not found")
                return FAILED
            flash_cmd = f"sudo uuu {lst_file}"
            syscmd(flash_cmd)

        case "qdl":
            syscmd("sudo qdl ./prog_firehose_ddr.elf rawprogram*.xml")
        case "genio_flash":
            flash_cmd = "$(which genio-flash)"
            if data["extra_args"]:
                flash_cmd += data["extra_args"]
            syscmd(flash_cmd)
        case _:
            print("unknow provision method")
