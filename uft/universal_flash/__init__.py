"""For parsing argument"""

import argparse
import wget
from urllib.parse import urlparse

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

    print(target)
