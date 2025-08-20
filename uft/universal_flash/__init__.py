"""For parsing argument"""

import argparse
import wget
import tarfile
import os
import shutil
import time
from urllib.parse import urlparse
from universal_flash.parser import DescriptorParser
from universal_flash.wspace import temp_local_directory
from universal_flash.provision_handler import provision_handler

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
        os.mkdir(target_dir)
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
        help="meta file indicate where to download images, how to provision. If meta us provided, url and local would be ignored",
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
            print(args.meta)
            desc_parser = DescriptorParser(f"{current_dir}/{args.meta}")
            print(desc_parser.data)
            urls = desc_parser.data["urls"]
            for url in urls:
                target = wget.download(url)
                untar_copy(target)

        else: # for single image
            if args.url and is_valid_url(args.url):
                try:
                    target = wget.download(args.url)
                except Exception as e:
                    print("Download Target failed")

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

            else:
                parser.print_help()

            desc_parser = DescriptorParser("config.yaml")

        if not desc_parser.data:
            return

        provision_handler(desc_parser.data)
