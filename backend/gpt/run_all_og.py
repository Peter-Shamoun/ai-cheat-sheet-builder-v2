import subprocess
import sys
import os

def run_scripts():
    print("Running template_focus.py...")
    subprocess.run([sys.executable, "template_focus.py"], check=True)
    
    print("\nRunning latex_to_pdf.py...")
    subprocess.run([sys.executable, "latex_to_pdf.py"], check=True)

if __name__ == "__main__":
    # Change to the directory containing the scripts
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    try:
        run_scripts()
    except subprocess.CalledProcessError as e:
        print(f"Error running scripts: {e}")
        sys.exit(1)
