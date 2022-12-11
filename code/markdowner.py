import subprocess as sp
import platform
import os
from pathlib import Path, PurePosixPath
import sys

def createPsCommand(commandString):
    pre = 'powershell -Command "'
    end = '"'
    convString = ''
    
    for ch in commandString:
        if ch == '"':
            convString = convString + '\\"'
        else:
            convString = convString + ch
            
    return pre + convString + end

def startOfProgram(sourceFile, prettiefy=True):
    sourceFilePath = Path(sourceFile).absolute()

    installPath = Path(os.path.realpath(__file__)).parent
    pandocPath = (installPath / 'misc' / 'pandoc' / 'pandoc.exe').absolute()
    miktexPath = (installPath / 'misc' / 'miktex' / 'bin' / 'x64' / 'pdflatex.exe').absolute()
    nodePath = (installPath / 'misc' / 'node' / 'node.exe').absolute()
    prettierPath = (installPath / 'misc' / 'prettier' / 'bin-prettier.js').absolute()
    templatePath = (installPath / 'misc' / 'eisvogel.tex').absolute()
    
    if prettiefy:
        cmd = (f'& "{nodePath}" "{prettierPath}" ' + 
               f'--write --prose-wrap always --print-width 72 ' + 
               f'"{sourceFilePath}"')
        sp.check_call(createPsCommand(cmd), shell=True)

    cmd = (f'& "{pandocPath}" --pdf-engine "{miktexPath}" ' + 
           f'--listings --template "{templatePath}" ' + 
           f'-V titlepage=true "{sourceFilePath}" ' + 
           f'-o "{sourceFilePath.parent / sourceFilePath.stem}.pdf"')
    sp.check_call(createPsCommand(cmd), shell=True)
        

def main():
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
