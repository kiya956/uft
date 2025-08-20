import os
import re

from universal_flash.command import syscmd
from universal_flash.err import FAILED, SUCCESS
from tkinter import messagebox

def provision_handler(data):

    messagebox.showinfo("Notice", "Please put your device into download mode")
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
