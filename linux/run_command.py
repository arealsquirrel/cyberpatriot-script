
import sys
import subprocess

def run_command(command):
    with open("log.txt", "a") as file:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=file, text=True)
        for line in process.stdout:
            file.write(line + "\n")
            sys.stdout.write(line)
        process.wait()

        if process.returncode != 0:
            file.write(f"[!] Command failed with return code {process.returncode}\n")
            print(f"[!] Command failed with return code {process.returncode}")