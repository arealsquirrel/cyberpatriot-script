
import subprocess

def get_running_services():
    """
    Executes systemctl to fetch all active, running services
    and returns them as a list of dictionaries.
    """
    # Arguments to list active running services with no extra headers/pagers
    args = [
        "systemctl", 
        "list-units", 
        "--type=service",
        "--state=running", 
        "--plain", 
        "--no-legend", 
        "--no-page"
    ]
    
    try:
        # Run the command and capture the string output
        output = subprocess.check_output(args, text=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error executing systemctl: {e}")
        return []

    services = []
    
    # Process line by line
    for line in output.strip().split('\n'):
        if not line.strip():
            continue
        parts = line.split(maxsplit=4)
        
        if len(parts) >= 4:
            service_info = {
                "unit": parts[0],
                "load": parts[1],
                "active": parts[2],
                "sub": parts[3],
                "description": parts[4] if len(parts) > 4 else ""
            }
            services.append(service_info)
            
    return services

if __name__ == "__main__":
    critical_services = []
    with open("script.conf", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("critical_services"):
                critical_services = line.split("=")[1].strip().split(",")
                critical_services = [service.strip() for service in critical_services]
                print(f"Critical services: {critical_services}")
                break

    if len(critical_services) == 0:
        print("No critical services found in script.conf")
        exit(1)

    if "vsftpd" in critical_services:
        subprocess.run(["bash", "linux/service_scripts/linux_vsftpd.sh"], check=True)
    else:
        subprocess.run(['apt-get', 'purge', '-y', "vsftpd"], check=True)

    # services = get_running_services()
    
    if "squid" not in critical_services:
        subprocess.run(['systemctl', 'disable', '--now', "squid"], check=True)

    if "nginx" not in critical_services:
        subprocess.run(['systemctl', 'disable', '--now', "nginx"], check=True)

    if "cups" not in critical_services:
        subprocess.run(['systemctl', 'disable', '--now', "cups"], check=True)

    if "ssh" not in critical_services:
        subprocess.run(['systemctl', 'disable', '--now', "ssh"], check=True)

