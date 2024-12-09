#!/usr/bin/env python3
import os
import platform
import subprocess
import sys
import shutil
from pathlib import Path
import pkg_resources

def get_binary_name():
    """Get the appropriate binary name for the current platform."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        return "lm.exe"
    return "lm"

def get_binary_path():
    """Get the appropriate binary path for the current platform."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        return "binaries/win_amd64/lm.exe"
    elif system == "linux":
        return "binaries/linux_x86_64/lm"
    elif system == "darwin":
        if machine == "arm64":
            return "binaries/darwin_arm64/lm"
        else:
            return "binaries/darwin_x86_64/lm"
    else:
        raise RuntimeError(f"Unsupported platform: {system} {machine}")

def install_binary():
    """Install the binary from package resources."""
    try:
        binary_name = get_binary_name()
        binary_path = get_binary_path()
        
        try:
            resource_path = pkg_resources.resource_filename("lmprep", binary_path)
        except Exception as e:
            raise RuntimeError(f"Binary not found in package: {e}")
            
        if platform.system().lower() == "windows":
            install_dir = os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "lmprep")
        else:
            if os.access("/usr/local/bin", os.W_OK):
                install_dir = "/usr/local/bin"
            else:
                install_dir = os.path.expanduser("~/.local/bin")
                os.makedirs(install_dir, exist_ok=True)
                
        target_path = os.path.join(install_dir, binary_name)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        print(f"Installing binary to: {target_path}")
        shutil.copy2(resource_path, target_path)
        if platform.system().lower() != "windows":
            os.chmod(target_path, 0o755)
            
        return target_path
            
    except Exception as e:
        raise RuntimeError(f"Failed to install binary: {e}")

def create_config():
    """Create default config file if it doesn't exist."""
    home = Path.home()
    config_file = home / ".lmprep.yml"
    
    if not config_file.exists():
        config_content = """# Default configuration for lmprep
subfolder: "context"
allowed_extensions: []
ignored_directories: [
    "node_modules",
    "venv",
    ".venv",
    "env",
    ".env",
    "target",
    "build",
    "dist",
    "__pycache__",
    ".git",
    ".idea",
    ".vs",
    ".vscode"
]
respect_gitignore: true"""
        
        config_file.write_text(config_content)
        print(f"Created default configuration at {config_file}")

def main():
    """Main entry point for the CLI."""
    try:
        binary_path = install_binary()
        create_config()
          
        try:
            result = subprocess.run(
                [binary_path] + sys.argv[1:],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
                
            sys.exit(result.returncode)
        except subprocess.TimeoutExpired:
            print("\nError: Command timed out after 30 seconds")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
