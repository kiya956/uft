import subprocess
import sys

def main():
    flashing = None
    result = subprocess.run("lsusb", capture_output=True, text=True, shell=True)
    if "NXP Semiconductors SE Blank 865" in result.stdout:
        print("NXP uuu device is found")
        if len(sys.argv) > 1:
            cmd = "uuu " + (' '.join(sys.argv[1:]))
        else:
            cmd = "uuu uc.lst"
        flashing = subprocess.Popen(cmd, text=True, shell=True)

    # Wait for the process to finish
    if flashing is not None:
        flashing.wait()
