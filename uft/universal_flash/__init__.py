"""For parsing argument"""

import argparse
import wget
import tarfile
import os
from urllib.parse import urlparse

def untar_chdir(
    tarball,
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

    # Positional argument
    parser.add_argument(
        "-u", "--url",
        help="The url of target file"
    )

    # Optional argument with a value
    parser.add_argument(
        "-f", "--file",
        help="local target file, if url is provided. This argument would be ignored",
    )

    # Parse arguments
    args = parser.parse_args()

    if args.url and is_valid_url(args.url):
        try:
            target = wget.download(args.url)
        except Exception as e:
            print("Download Target failed")

    else:
        target = args.file

    if not target:
        print("please provide valid url or file name")
        return

    if untar_chdir(target):
        print("decompress tarball failed")
        return

