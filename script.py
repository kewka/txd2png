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
            List of png file names.
    '''
    output = subprocess.check_output([config.TXD2PNG, os.path.abspath(filepath)],
                                     cwd=output_dir)
    lines = output.decode().splitlines()
    return [line.split()[1] for line in lines]


if __name__ == "__main__":
    args = sys.argv

    if (len(args) < 2):
        print('Usage: %s texture.txd' % args[0])
        exit(1)

    print(convert(args[1], config.TEMP_DIR))
