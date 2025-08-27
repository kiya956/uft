"""For parsing argument"""

import argparse
import wget
import tarfile
import os
import shutil
import time
import lzma
from urllib.parse import urlparse
from unified_flash.parser import DescriptorParser
from unified_flash.wspace import temp_local_directory
from unified_flash.provision_handler import provision_handler

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

        os.chdir(target_dir)

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

def is_valid_url(url):
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])
	
def main():
    target = ""
    parser = argparse.ArgumentParser(
        description="Example program showing how to use argparse."
    )


    parser.add_argument(
        "-m", "--meta",
        help="meta file indicate where to download images, how to provision. If meta is provided, url and local file would be ignored",
    )

    parser.add_argument(
        "-u", "--url",
        help="The url of target file"
    )

    parser.add_argument(
        "-f", "--file",
        help="local target file, if url is provided. This argument would be ignored",
    )


    # Parse arguments
    args = parser.parse_args()
    current_dir = os.getcwd()
    with temp_local_directory():
        # For meta
        if args.meta:
            target_dir = "temp"
            try:
                desc_parser = DescriptorParser(f"{current_dir}/{args.meta}")
            except ValueError as e:
                print(e)
                return
                
            urls = desc_parser.data["items"]
            os.mkdir(target_dir)
            for item in urls:
                try:
                    target = wget.download(item["url"])
                except Exception as e:
                    print("Download Target failed")
                    return

                fmt = is_compressed(target)
                if not fmt:
                    dest_file = os.path.join(target_dir, target)
                    shutil.copy2(target, dest_file)

                elif  fmt == "xz":
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

                else:
                    untar_copy(target, target_dir)

                if "sha" in item:
                    pass

        elif args.url or args.file: # for single image
            if args.url and is_valid_url(args.url):
                try:
                    target = wget.download(args.url)
                except Exception as e:
                    print("Download Target failed")
                    return

                if untar_chdir(target):
                    print("decompress tarball failed")
                    return

            elif args.file:
                target = args.file

                if os.path.isdir(target):
                    pass
                else:
                    shutil.copy2(f"{current_dir}/{target}", target)
                    if untar_chdir(target):
                        print("decompress tarball failed")
                        return

            try:
                desc_parser = DescriptorParser("config.yaml")
            except ValueError as e:
                print(e)
                return
        else:
            parser.print_help()
            return 

        if not desc_parser.data:
            return

        provision_handler(desc_parser.data)
