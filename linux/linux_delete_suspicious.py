
from pathlib import Path

if __name__ == "__main__":
    print("--------- SEARCHING FOR WEIRD FILES ---------")
    paths = ["/etc", "/lib", "/sys", "/usr", "/var", "/root", "/sbin", "/bin", "/dev", "/home"]
    for path in paths:
        extensions = [".midi", ".mid", ".mod", ".mp3", ".mp2", ".mpa", ".abs", ".mpega", ".au", ".snd", ".wav", ".aiff", ".aif", ".sid", ".flac", ".ogg",".mpeg", ".mpg", ".mpe", ".dl", ".movie", ".movi", ".mv", ".iff", ".anim5", ".anim3", ".anim7", ".avi", ".vfw", ".avx", ".fli", ".flc", ".mov", ".qt", ".spl", ".swf", ".dcr", ".dir", ".dxr", ".rpm", ".rm", ".smi", ".ra", ".ram", ".rv", ".wmv", ".asf", ".asx", ".wma", ".wax", ".wmx", ".3gp", ".mp4", ".flv", ".m4v", ".tiff", ".tif", ".rs", ".im1", ".gif", ".jpeg", ".jpg", ".jpe", ".png", ".rgb", ".xwd", ".xpm", ".ppm", ".pbm", ".pgm", ".pcx", ".ico", ".svg", ".svgz", ".php"]
        for ext in extensions: #input("Extension (e.g. .txt): ").strip()
            if not ext.startswith("."):
                ext = "." + ext
            folder = Path(path)
            for f in list(folder.rglob("*" + ext)):
                if f.is_file() and input(f"Delete {f}? (y/n): ").strip().lower() == "y":
                    f.unlink()
                    print("Deleted.")

