import subprocess
import sys
import time

uuu = [
    "NXP Semiconductors SE Blank 865",
    "Freescale Semiconductor, Inc. SE Blank PELE",
    "Freescale Semiconductor, Inc. i.MX 6Dual/6Quad SystemOnChip in RecoveryMode"
]

def main():
    flashing = None
    print("Waiting for target device....")
    while True:
        result = subprocess.run("lsusb", capture_output=True, text=True, shell=True)
        if any(device in result.stdout for device in uuu):
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
