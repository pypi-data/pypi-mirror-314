import os
import platform
import shutil
import sys
from setuptools import setup

def copy_binary():
    """Copy the pre-built Rust binary to the package directory"""
    print(f"Starting binary copy process... Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Determine binary name and paths
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        binary_name = "lm.exe"
        platform_dir = "windows_amd64"
    elif system == "linux":
        binary_name = "lm"
        platform_dir = "linux_x86_64"
    elif system == "darwin":  # macOS
        binary_name = "lm"
        if machine == "arm64":
            platform_dir = "darwin_arm64"
        else:
            platform_dir = "darwin_x86_64"
    else:
        raise RuntimeError(f"Unsupported platform: {system}")

    binary_path = os.path.join("target", "release", binary_name)
    package_dir = os.path.join("lmprep", "binaries", platform_dir)
    
    print(f"System: {system}, Machine: {machine}")
    print(f"Binary path: {binary_path}")
    print(f"Package dir: {package_dir}")
    
    # Create binaries directory if it doesn't exist
    os.makedirs(package_dir, exist_ok=True)
    print(f"Created directory: {package_dir}")
    
    # Copy binary to package if it exists
    if os.path.exists(binary_path):
        dest_binary = os.path.join(package_dir, binary_name)
        print(f"Copying {binary_path} to {dest_binary}")
        shutil.copy2(binary_path, dest_binary)
        print(f"Binary copied successfully")
        print(f"Destination contents: {os.listdir(package_dir)}")
    else:
        print(f"WARNING: Binary not found at {binary_path}. Skipping copy.")

if __name__ == "__main__":
    copy_binary()
    
    setup(
        package_data={
            "lmprep": ["binaries/**/*"],
        },
        include_package_data=True,
    )
