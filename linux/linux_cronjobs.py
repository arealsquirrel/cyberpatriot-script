    
import subprocess

if __name__ == "__main__":
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    lines = result.stdout.splitlines() if result.returncode == 0 else []

    jobs = {i: line for i, line in enumerate(lines, 1) if line.strip() and not line.strip().startswith("#")}

    if not jobs:
        print("No cron jobs found.")
        raise SystemExit

    for i, line in jobs.items():
        print(f"{i}: {line}")
    print()

    choice = input("Line number to delete (Enter to quit): ").strip()
    if not choice:
        raise SystemExit

    if not choice.isdigit() or int(choice) not in jobs:
        print("Invalid line number.")
        raise SystemExit(1)

    n = int(choice)
    if input(f"Delete '{jobs[n]}'? (y/n): ").strip().lower() == "y":
        del lines[n - 1]
        new_crontab = "\n".join(lines) + "\n" if lines else ""
        subprocess.run(["crontab", "-"], input=new_crontab, text=True)
        print("Deleted.")
