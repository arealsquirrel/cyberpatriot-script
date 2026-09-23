
import subprocess

def run_command(command):
    with open("log.txt", "a") as file:
        result = subprocess.run(command, stdout=file, stderr=file, text=True)
        if result.returncode != 0:
            file.write(f"[!] Command failed with return code {result.returncode}\n")
            print(f"[!] Command failed with return code {result.returncode}")
        print(result.stdout)
        file.flush()