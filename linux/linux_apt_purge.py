
import subprocess

def get_installed_packages():
    try:
        result = subprocess.run(
            ['apt', 'list', '--installed'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=True
        )
        
        packages = []
        lines = result.stdout.splitlines()
        
        for line in lines:
            if line.startswith('Listing...') or not line:
                continue
            parts = line.split('/')
            if parts:
                package_name = parts[0].strip()
                packages.append(package_name)
                
        return packages

    except subprocess.CalledProcessError as e:
        print(f"Error executing apt command: {e}")
        return []
    except FileNotFoundError:
        print("The 'apt' command is not available on this system.")
        return []


if __name__ == "__main__":
    installed_pkgs = get_installed_packages()
    print(f"Total packages installed: {len(installed_pkgs)}")

    with open("linux/templates/apt_blacklist", "r", encoding="utf-8") as file:
        blacklist = [line.strip() for line in file if line.strip()]
        for pkg in blacklist:
            print(pkg)
            if pkg in installed_pkgs:
                print(f"Package '{pkg}' is installed and will be purged.")
                subprocess.run(['apt-get', 'purge', '-y', pkg])
            else:
                print(f"Package '{pkg}' is not installed.")

