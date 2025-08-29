"""For parsing argument"""

import argparse
import wget
import time
import os
import shutil
from urllib.parse import urlparse
from unified_flash.tarball_handler import is_compressed, file_copy, untar_copy, unxz_copy, untar_chdir
from unified_flash.parser import DescriptorParser
from unified_flash.wspace import temp_local_directory
from unified_flash.provision_handler import provision_handler


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
                
            urls = desc_parser.data["urls"]
            os.mkdir(target_dir)
            for item in urls:
                try:
                    target = wget.download(item["url"])
                except Exception as e:
                    print("Download Target failed")
                    return

                fmt = is_compressed(target)
                if not fmt:
                    file_copy(target, target_dir)

                elif  fmt == "xz":
                    unxz_copy(target, target_dir)

                else:
                    untar_copy(target, target_dir)

                if "sha256sum" in item:
                    pass

            os.chdir(target_dir) 

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
