import os

def Alert(title, msg):
    power_shell_command = f'PowerShell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show(\'{msg}\', \'{title}\')"'
    os.system(power_shell_command)
