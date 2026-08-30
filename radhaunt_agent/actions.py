import subprocess

def power_off_server():
    cmd = ["sudo", "/usr/bin/shutdown", "now"]
    subprocess.run(cmd)