import subprocess as sp
import platform
import os
from pathlib import Path, PurePosixPath
import installer
import install_markdowner

class CustomError(Exception):
    pass

def startOfProgram(sourceFile, prettiefy=True):
    templateFile = (installer.getInstallPath('markdowner') / Path('misc') / Path('eisvogel.tex')).absolute()
    teplateFileStr = '/mnt/' + str(PurePosixPath(templateFile))[0].lower() + str(PurePosixPath(templateFile))[3:]

    wslType = install_markdowner.checkWslStatus()
    if wslType == 'UBUNTU':
        prefix = 'wsl -d ubuntu'
    elif wslType == 'DEBIAN':
        prefix = 'wsl -d debian'
    else:
        return 1
    
    if prettiefy:
        cmd = f'{prefix} bash -c "npx prettier --write --prose-wrap always --print-width 72 {str(Path(sourceFile))}"'
        sp.check_call(cmd, shell=True)
    cmd = f'{prefix} bash -c "pandoc --listings --template \'{teplateFileStr}\' -V titlepage=true {str(Path(sourceFile))} -o {str(Path(sourceFile))[0:-3]}.pdf"'
    sp.check_call(cmd, shell=True)

def main():
    if installer.isAlreadyInstalled('markdowner') == False:
        input('Not installed correctly, please run installer. Press ENTER to exit program.')
    else:
        import argparse

        parser = argparse.ArgumentParser(description=
            """Markdowner is a cross platform Markdown to PDF converter.
            It uses pandoc, latex and prettier internally.""")
        parser.add_argument("sourceFile", help = "path to markdown source file")
        parser.add_argument('-np', '--do-not-prettiefy', action='store_true',
            help="this will make the program not use the prettifier on your source file")
        args = parser.parse_args()

        startOfProgram(args.sourceFile, prettiefy=not args.do_not_prettiefy)

if __name__ == '__main__':
    main()
