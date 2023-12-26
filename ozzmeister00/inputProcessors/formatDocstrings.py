"""
Helper utility for word-wrapping the docstrings for each Day solver file
Since the texted pasted-in from the web doesn't have any line breaks
"""
import argparse
import os
import sys
import textwrap


def formatDocstring(filePath):
    """
    Given an input python file path, load it up and format the triple-double-quoted docstring at the top
    of the file

    :param str filePath: Path to the file
    :return str: failure reason
    """
    with open(filePath, 'r') as fh:
        contents = fh.read()

    with open(filePath, 'w') as fh:
        docStringStart = False
        for graf in contents.splitlines():
            if graf.strip():
                if '"""' in graf:
                    docStringStart = not docStringStart
                if docStringStart:
                    for line in textwrap.wrap(graf, width=80, replace_whitespace=False, drop_whitespace=False):
                        fh.write(line)
                        fh.write('\n')
                else:
                    fh.write(graf)
                    fh.write('\n')
            else:
                fh.write('\n')


def formatDocStrings(dirPath):
    """
    Given an input directory path, recursively load all the .py files in that directory and format
     the triple-double-quoted docstring at the top of the file

    :param str dirPath: Directory path to files to recursively process
    :return str: failure reason
    """
    exitCode = None
    for dirPath, dirNames, files in os.walk(dirPath):
        for filePath in [os.path.join(dirPath, fileName) for fileName in files if fileName.endswith('.py')]:
            exitCode = formatDocstring(filePath)

    return exitCode


def main():
    """
    Main function for calling via commandline

    :return str: exit reason
    """
    parser = argparse.ArgumentParser(prog="FormatDocstrings",
                                     description="""Helper utility for word-wrapping the docstrings for each Day solver file
Since the texted pasted-in from the web doesn't have any line breaks""")

    parser.add_argument('-f', '--file')
    parser.add_argument('-d', '--dir')

    args = parser.parse_args()

    if args.file:
        if os.path.exists(args.file):
            return formatDocstring(args.file)
    elif args.dir:
        if os.path.exists(args.dir):
            return formatDocStrings(args.dir)

    raise IOError("No arguments provided")


if __name__ == '__main__':
    sys.exit(main())
