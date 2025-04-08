import subprocess
import sys
import time

uuu = [
    "NXP Semiconductors SE Blank 865",
    "Freescale Semiconductor, Inc. SE Blank PELE",
    "Freescale Semiconductor, Inc. i.MX 6Dual/6Quad SystemOnChip in RecoveryMode"
]

imx6_flashing = [
    "Freescale Semiconductor, Inc. i.MX 6ULL SystemOnChip in RecoveryMode"
]

qdl = [
    "Qualcomm, Inc. Gobi Wireless Modem (QDL mode)"
]

def main():
    flashing = None
    print("Waiting for target device....")
    while True:
        result = subprocess.run("lsusb", capture_output=True, text=True, shell=True)
        if any(device in result.stdout for device in uuu):
            print("NXP uuu device found")
            if len(sys.argv) > 1:
                cmd = "uuu " + (' '.join(sys.argv[1:]))
            else:
                cmd = "uuu uc.lst"
            flashing = subprocess.Popen(cmd, text=True, shell=True)
            break
        elif any(device in result.stdout for device in imx6_flashing):
            print("imx6 flashing tool TBD")
            break
        elif any(device in result.stdout for device in qdl):
            print("Qualcomm device found")
            if len(sys.argv) > 1:
                cmd = "qdl " + (' '.join(sys.argv[1:]))
            else:
                cmd = "qdl"
            flashing = subprocess.Popen(cmd, text=True, shell=True)
            break
        time.sleep(3)

    # Wait for the process to finish
    if flashing is not None:
        flashing.wait()
