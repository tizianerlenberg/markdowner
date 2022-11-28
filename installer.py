from pathlib import Path
from zipfile import ZipFile
import os, sys, platform, shutil

def getInternalFilePath(nameOfZip):
    try:
        wd = sys._MEIPASS
    except AttributeError:
        wd = os.getcwd()
    return os.path.join(wd, nameOfZip)

def getInstallPath(nameOfProgram):
    if platform.system() == "Windows":
        return Path(os.path.expanduser('~')) / Path('AppData/Roaming' / Path(nameOfProgram))
    else:
        return Path(os.path.expanduser('~')) / Path("." + nameOfProgram)

def extractBlob(name, dest):
    with ZipFile(getInternalFilePath(name)) as zObject:
        zObject.extractall(path=dest)

def addToPath(name):
    import subprocess as sp
    if platform.system() == "Windows":
        #powershell -Command "[Environment]::SetEnvironmentVariable('PATH', \"$([Environment]::GetEnvironmentVariable('PATH', 'User'));C:\Users\Tizian Erlenberg\AppData\Roaming\markdowner\",'User')"
        cmd =   ("powershell -Command \"" +
                    "[Environment]::SetEnvironmentVariable(" +
                        "'PATH', \\\"" + 
                            "$([Environment]::GetEnvironmentVariable(" +
                                "'PATH', 'User'" +
                            "))" +
                            ";" +
                            str(getInstallPath(name)) +
                        "\\\"" +
                        ", " +
                        "'User'" +
                    ")" +
                "\"")
        sp.check_call(cmd, shell=True)
    else:
        pass
        #TODO

def setDoneFlag(nameOfProgram):
    with open(getInstallPath(nameOfProgram) / Path('installerHasRun'), 'w') as fp:
        pass

def unsetDoneFlag(nameOfProgram):
    os.remove(getInstallPath(nameOfProgram) / Path('installerHasRun'))

def isAlreadyInstalled(nameOfProgram):
    if os.path.exists(getInstallPath(nameOfProgram) / Path('installerHasRun')):
        return True
    else:
        return False

def install(nameOfProgram, addToPathVar=False, setFlag=True):
    if isAlreadyInstalled(nameOfProgram):
        return 1

    extractBlob("package.zip", getInstallPath(nameOfProgram))
    if addToPathVar:
        addToPath(nameOfProgram)
    if setFlag:
        setDoneFlag(nameOfProgram)
    return 0

def uninstall(nameOfProgram):
    import subprocess as sp
    if platform.system() == "Windows":
        cmd = "powershell -Command \"[Environment]::GetEnvironmentVariable('PATH', 'User')\""
        sess = sp.Popen(cmd,
                    shell=True,
                    stdout=sp.PIPE,
                    stderr=sp.PIPE)
        rc = sess.wait()
        out,err=sess.communicate()
        listOfEntrys = out.decode().split(';')
        newListOfEntrys = listOfEntrys.copy()
        
        for item in listOfEntrys:
            if str(getInstallPath(nameOfProgram)) in item:
                newListOfEntrys.remove(item)

        newPath = ';'.join(newListOfEntrys)
        cmd =   ("powershell -Command \"" +
                    "[Environment]::SetEnvironmentVariable(" +
                        "'PATH', \\\"" + 
                            newPath +
                        "\\\"" +
                        ", " +
                        "'User'" +
                    ")" +
                "\"")
        sp.check_call(cmd, shell=True)

        shutil.rmtree(getInstallPath(nameOfProgram))
    else:
        pass
        #TODO

def continueYesNo(message):
    user_input = input(f"{message}\n" + 
                        "Do you want to continue? (y / n): ")

    if user_input == 'y' or user_input == 'Y':
        return True
    else:
        return False

def interactiveUninstall(nameOfProgram, beforeUninstall=None, afterUninstall=None):
    message = ('============= UNISNTALLER =============\n' +
               f'Do you REALLY want to uninstall \"{nameOfProgram}\" from your system?')
    if continueYesNo(message):
        if beforeUninstall:
            beforeUninstall()
        uninstall(nameOfProgram)
        if afterUninstall:
            afterUninstall()
    input("Program successfully uninstalled. To exit press ENTER: ")
    sys.exit(1)

def interactiveInstall(nameOfProgram, addToPathVar=False, beforeInstall=None, afterInstall=None, beforeUninstall=None, afterUninstall=None):
    if isAlreadyInstalled(nameOfProgram):
        print('Program is already installed on your computer.\n' +
              'Therefore the uninstaller is beeing started.\n\n')
        interactiveUninstall(nameOfProgram, beforeUninstall=beforeUninstall, afterUninstall=afterUninstall)

    message = (f"This is an installer for {nameOfProgram}. " + 
               "It will install the Program on your computer.")
    if not continueYesNo(message):
        print("Aborting installation")
        return 1

    if beforeInstall:
        beforeInstall()
    
    install(nameOfProgram, addToPathVar=addToPathVar, setFlag=False)

    if afterInstall:
        afterInstall()
    
    setDoneFlag(nameOfProgram)
    input("Program successfully installed. To exit press ENTER: ")
    return 0

def main():
    pass
    #interactiveInstall('testProgram')
    uninstall('markdowner')

if __name__ == '__main__':
    main()

