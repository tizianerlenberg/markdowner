import subprocess as sp
import platform
import installer
import sys
import os
import shutil
from pathlib import Path

class globVars():
    pass

class CustomError(Exception):
    pass

def checkWslStatus():
    cmd = "wsl -d ubuntu echo WSL INSTALLED"
    sess = sp.Popen(cmd,
                    shell=True,
                    stdout=sp.PIPE,
                    stderr=sp.PIPE)
    rc = sess.wait()
    out,err=sess.communicate()
    cmd = "wsl -d debian echo WSL INSTALLED"
    sess = sp.Popen(cmd,
                    shell=True,
                    stdout=sp.PIPE,
                    stderr=sp.PIPE)
    rc = sess.wait()
    out2,err2=sess.communicate()

    if out.decode().startswith('WSL INSTALLED'):
        return 'UBUNTU'
    elif out2.decode().startswith('WSL INSTALLED'):
        return 'DEBIAN'
    
    return 'NOT DEFINED'

def checkAdminStatus():
    cmd = "net session"
    sess = sp.Popen(cmd,
                    shell=True,
                    stdout=sp.PIPE,
                    stderr=sp.PIPE)
    rc = sess.wait()
    out,err=sess.communicate()

    if err.decode().startswith('System error 5 has occurred.'):
        return False
    elif out.decode().startswith('There are no entries in the list.'):
        return True
    else:
        raise Exception("Can't determine administrator status") 

def installWsl():
    if checkWslStatus() == 'NOT DEFINED':
        message = ('The System detected that you are running a Windows machine. '+
                   'It will try to install the Windows Subsystem for Linux.')
        if not installer.continueYesNo(message):
            print("Aborting installation")
            sys.exit(1)
        if not checkAdminStatus():
            input('To install the Windows Subsystem for Linux the installer needs admin privileges.' + 
                'Please run the program with administrator privileges.' + 
                'To exit press ENTER: ')
            sys.exit(1)
        
        input('The Program will now install WSL for you.'+
            'This may take a while.\n\n'+
            '============== IMPORTANT ==============\n' +
            'After the install of Windows Subsystem for Linux you may have to restart the computer.' + 
            'You will be asked to enter a UNIX username and password after the reboot' +
            'After that happened, open this installer again.\n\n' +
            'To continue press ENTER: ')
        cmd = "wsl --install -d ubuntu"
        sp.check_call(cmd, shell=True)
        input('\nWindows Subsystem for Linux successfully installed.\n\n' +
            'PLEASE RESTART THE COMPUTER NOW' +
            'To continue press ENTER: ')
        sys.exit(0)
    else:
        return 0

def installWslTools():
    prefix = ''
    wslType = checkWslStatus()
    if wslType == 'UBUNTU':
        prefix = 'wsl -d ubuntu'
    elif wslType == 'DEBIAN':
        prefix = 'wsl -d debian'
    else:
        raise Exception('WSL not installed')
    
    input('The program will install the required tools now. '+
          'This may take a while.\n'+
          'To continue please press ENTER: ')
    
    password = input('Please enter the password you use for the WSL, '+
                     'so this program can install the necessary tools: ')
    
    cmd = f'{prefix} bash -c "echo {password} | sudo -S apt install pandoc npm texlive-full"'
    sp.check_call(cmd, shell=True)

    os.mkdir('.tmpInstall')
    cmd = f'{prefix} bash -c "cd .tmpInstall; npm install --save-dev --save-exact prettier"'
    sp.check_call(cmd, shell=True)
    shutil.rmtree('.tmpInstall')

def installAll():
    if platform.system() == "Windows":
        def beforeInstall():
            retVal = installWsl()
            if retVal == 0:
                installWslTools()
            else:
                raise Exception('Something went wrong during the installation of the WSL')
    else:
        def beforeInstall():
            pass
            #TODO
    
    installer.interactiveInstall('markdowner', beforeInstall=beforeInstall, addToPathVar=True)

def uninstallAll():
    if platform.system() == "Windows":
        def beforeUninstall():
            pass
            #TODO
    else:
        def beforeUninstall():
            pass
            #TODO
    
    installer.interactiveUninstall('markdowner', beforeUninstall=beforeUninstall)

def main():
    installAll()

if __name__ == '__main__':
    main()
