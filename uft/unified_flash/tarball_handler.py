import tarfile
import os
import shutil
import lzma

def is_compressed(filepath):
    with open(filepath, "rb") as f:
        magic = f.read(6)
    if magic.startswith(b"\x1f\x8b"):  # gzip
        return "gzip"
    if magic.startswith(b"PK\x03\x04"):  # zip
        return "zip"
    if magic.startswith(b"BZh"):  # bzip2
        return "bzip2"
    if magic.startswith(b"\xfd7zXZ"):  # xz
        with lzma.open(filepath, "rb") as xf:
            head = xf.read(600)  # read enough for tar header area
            if len(head) >= 262 and head[257:262] == b"ustar":
                return "tar.xz"
            else:
                return "xz"
    if magic.startswith(b"7z\xbc\xaf\x27\x1c"):  # 7z
        return "7z"

    return None

def file_copy(
    target: str,
    target_dir: str = "temp"
):
    dest_file = os.path.join(target_dir, target)
    shutil.copy2(target, dest_file)


def unxz_copy(
    target: str,
    target_dir: str = "temp"
):
    out_image, ext = os.path.splitext(target)
                    # Perform decompression
    with (
        lzma.open(target, "rb") as f_in,
        open(out_image, "wb") as f_out,
    ):
        shutil.copyfileobj(f_in, f_out)
        print(
            f"Decompressed image: {target} -> {out_image}"
        )
    dest_file = os.path.join(target_dir, out_image)
    shutil.copy2(out_image, dest_file)


def untar_copy(
    tarball: str,
    target_dir: str = "temp"
):
    """untar file and copy file to target folder"""
    print("Extracting the image archive...")
    image_dir = ""
    if not tarball:
        return -1

    with tarfile.open(tarball, "r:*") as archive:
        names = archive.getnames()
        # Extract top-level directories
        top_dirs = {name.split("/")[0] for name in names if "/" in name}
        if len(top_dirs) == 1:
            image_dir = top_dirs.pop()

        archive.extractall()

    if image_dir:
        for item in os.listdir(image_dir):
            source_file = os.path.join(image_dir, item)
            dest_file = os.path.join(target_dir, item)

            if os.path.isdir(source_file):
                shutil.copytree(source_file, dest_file)
            else:
                shutil.copy2(source_file, dest_file)

    return 0

def untar_chdir(
    tarball: str,
):
    """untar file and change location to folder"""
    print("Extracting the image archive...")
    image_dir = ""
    if not tarball:
        return -1

    with tarfile.open(tarball, "r:*") as archive:
        names = archive.getnames()
        # Extract top-level directories
        top_dirs = {name.split("/")[0] for name in names if "/" in name}
        if len(top_dirs) == 1:
            image_dir = top_dirs.pop()

        archive.extractall()

    if image_dir:
        os.chdir(image_dir)

    return 0

