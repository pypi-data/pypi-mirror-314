import subprocess
import sys
from pathlib import Path

def build_executable(platform):
    """Build the phrasec executable using PyInstaller"""
    phrasec_path = Path(__file__).parent.joinpath("phrasec.py")
    wordlist_path = Path(__file__).parent.joinpath("eef_wordlist.txt")
    # Set the PyInstaller command for your platform
    pyinstaller_cmd = [
        'pyinstaller',
        #'--onefile',  # Single file output
        '--strip',
        '--name', 'phrasec',  # Name of the output executable
        '--add-data', f"{wordlist_path}:.",
        f"{phrasec_path}",  # Path to the main script
    ]

    if platform == 'windows':
        print("Building for Windows...")
    elif platform == 'linux':
        # Handle Linux-specific paths
        print("Building for Linux...")
    
    try:
        subprocess.run(pyinstaller_cmd, check=True)
        print(f"Build for {platform} completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during build for {platform}: {e}")
        sys.exit(1)

def main():
    """Main function to handle the build process"""
    platform = sys.platform

    # Check if the platform is Windows or Linux and build accordingly
    if platform.startswith('win'):
        build_executable('windows')
    elif platform.startswith('linux'):
        build_executable('linux')
    else:
        print(f"Unsupported platform: {platform}")
        sys.exit(1)

if __name__ == '__main__':
    main()
