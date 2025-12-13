"""
FileSense Setup Script
"""
import subprocess
import sys
import os


def install_dependencies():
    """Install required Python packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def check_ollama():
    """Check if OLLAMA is available"""
    print("\nChecking OLLAMA installation...")
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ OLLAMA is installed")
            print("\nAvailable models:")
            print(result.stdout)
            return True
        else:
            print("⚠️ OLLAMA found but not configured properly")
            return False
    except FileNotFoundError:
        print("❌ OLLAMA not found")
        print("   Please install OLLAMA from: https://ollama.ai")
        return False
    except subprocess.TimeoutExpired:
        print("⚠️ OLLAMA command timed out")
        return False


def suggest_model():
    """Suggest installing a model"""
    print("\nTo use AI features, install a model:")
    print("  ollama pull llama2")
    print("  ollama pull mistral")
    print("  ollama pull codellama")


def main():
    """Main setup function"""
    print("=" * 60)
    print("FileSense Setup")
    print("=" * 60)
    print()
    
    # Install dependencies
    if not install_dependencies():
        print("\nSetup failed. Please install dependencies manually:")
        print(f"  {sys.executable} -m pip install -r requirements.txt")
        sys.exit(1)
    
    # Check OLLAMA
    ollama_ok = check_ollama()
    
    if not ollama_ok:
        suggest_model()
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nTo run FileSense:")
    print(f"  {sys.executable} main.py")
    print("\nOr use the provided launch script:")
    if os.name == 'nt':
        print("  run.bat")
    else:
        print("  ./run.sh")
    print()


if __name__ == "__main__":
    main()
