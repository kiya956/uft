import subprocess
import sys
import time

def main():
    flashing = None
    print("Waiting for target device....")
    while True:
        result = subprocess.run("lsusb", capture_output=True, text=True, shell=True)
        if "NXP Semiconductors SE Blank 865" in result.stdout:
            print("NXP uuu device is found")
            if len(sys.argv) > 1:
                cmd = "uuu " + (' '.join(sys.argv[1:]))
            else:
                cmd = "uuu uc.lst"
            flashing = subprocess.Popen(cmd, text=True, shell=True)
            break
        time.sleep(3)

    # Wait for the process to finish
    if flashing is not None:
        flashing.wait()
