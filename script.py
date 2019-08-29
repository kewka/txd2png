import sys
import os
import config
import subprocess
from typing import List


def convert(filepath: str, output_dir: str) -> List[str]:
    '''
        Converts a txd file to png.

        Args:
            filepath: The TXD file path.
            output_dir: The output directory path.
        Returns:
            List of png files.
    '''
    output = subprocess.check_output([config.TXD2PNG, os.path.abspath(filepath)],
                                     cwd=output_dir)
    lines = output.decode().splitlines()
    return [line.split()[1] for line in lines]


if __name__ == "__main__":
    args = sys.argv

    if (len(args) < 2):
        print('Usage: %s [path to txd]' % args[0])
        exit(1)

    filepath = args[1]
    output_dir = os.getcwd()
    png_files = convert(filepath, output_dir)

    for file in png_files:
        print('\033[92m+ %s.png\033[0m' % os.path.join(output_dir, file))
