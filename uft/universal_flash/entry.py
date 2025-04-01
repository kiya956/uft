import subprocess
import sys

def main():
    result = subprocess.run("lsusb", capture_output=True, text=True, shell=True)
    if "NXP Semiconductors SE Blank 865" in result.stdout:
        print("NXP uuu device is found")
        flashing = subprocess.Popen("uuu uc.lst", text=True, shell=True)

    # Wait for the process to finish
    flashing.wait()
