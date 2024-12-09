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

def install_binary():
    """Install the binary from package resources."""
    try:
        binary_name = get_binary_name()
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        if system == "darwin":
            resource_path = f"binaries/darwin_{machine}/lm"
        elif system == "linux":
            resource_path = f"binaries/linux_{machine}/lm"
        elif system == "windows":
            resource_path = "binaries/windows_amd64/lm.exe"
        else:
            raise RuntimeError(f"Unsupported platform: {system}")
            
        try:
            binary_path = pkg_resources.resource_filename("lmprep", resource_path)
        except Exception as e:
            raise RuntimeError(f"Binary not found in package: {e}")
            
        if system == "windows":
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
        shutil.copy2(binary_path, target_path)
        if system != "windows":
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
