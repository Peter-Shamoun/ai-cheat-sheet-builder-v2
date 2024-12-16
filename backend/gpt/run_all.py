import subprocess
import sys
import os
import time

def run_scripts():
    """Runs the three scripts in sequence."""
    print("Running template_focus.py...")
    subprocess.run([sys.executable, "template_focus.py"], check=True)
    
    print("\nRunning latex_to_pdf.py...")
    subprocess.run([sys.executable, "latex_to_pdf.py"], check=True)
    
    print("\nRunning count_pages.py...")
    subprocess.run([sys.executable, "count_pages.py"], check=True)

def main():
    # Change to the directory containing the scripts
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    X = 5  # Adjust this to the number of times you want to run all three scripts.

    total_start_time = time.perf_counter()  # Start total timer

    for i in range(X):
        print(f"\n=== Iteration {i+1} of {X} ===")
        iteration_start_time = time.perf_counter()  # Start iteration timer
        try:
            run_scripts()
        except subprocess.CalledProcessError as e:
            print(f"Error running scripts on iteration {i+1}: {e}")
            sys.exit(1)
        iteration_end_time = time.perf_counter()  # End iteration timer
        iteration_duration = iteration_end_time - iteration_start_time
        print(f"Iteration {i+1} completed in {iteration_duration:.2f} seconds.")

    total_end_time = time.perf_counter()  # End total timer
    total_duration = total_end_time - total_start_time
    print(f"\nAll {X} iterations completed in {total_duration:.2f} seconds.")

if __name__ == "__main__":
    main()