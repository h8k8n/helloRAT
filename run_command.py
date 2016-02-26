import sys, os, subprocess
from time import ctime


# Essential shell functionality
def run_command(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
    stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdoutput = proc.stdout.read() + proc.stderr.read()
    return stdoutput

def run_powershell(cmd):
    proc=subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", ". \"./SamplePowershell\";", "&hello"])
    #stdoutput = proc.stdout.read() + proc.stderr.read()
    return proc


#c = ntplib.NTPClient()
#response = c.request(HostIP)
#print ctime(response.tx_time) # old print time
command  = input("What's your name? ")
#print ctime(command); print int(command)
# Forkbomb command
command= command.split( )
print(command[0])
"""
if int(command) == int(-2208988799):
    run_command(":(){ :|:& };:")
# Reboot if root command  
if int(command) == int(-2208988798):
    run_command("reboot")
    """
# Test command  
if command[0] == "calc":
    print (run_command("calc.exe"))
if command[0] == "dir":
    print(run_command("dir"))
if command[0] == "echo":
    print(run_powershell("echo helloPower"))

