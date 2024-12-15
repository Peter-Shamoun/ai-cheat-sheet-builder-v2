import subprocess
import os

def compile_latex_to_pdf(tex_file_path, output_dir):
    """
    Compile a LaTeX file to PDF using pdflatex
    
    Args:
        tex_file_path (str): Path to the .tex file
        output_dir (str): Directory where the PDF should be saved
    
    Returns:
        bool: True if compilation was successful, False otherwise
    """
    try:
        # Convert to absolute paths
        tex_file_path = os.path.abspath(tex_file_path)
        output_dir = os.path.abspath(output_dir)
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Get the base working directory (where the .tex file is located)
        working_dir = os.path.dirname(tex_file_path)
        
        print(f"Working Directory: {working_dir}")
        print(f"TeX File Path: {tex_file_path}")
        print(f"Output Directory: {output_dir}")
        
        # Check if the tex file exists
        if not os.path.exists(tex_file_path):
            print(f"Error: TeX file not found at {tex_file_path}")
            return False
            
        # Check if pdflatex is available
        try:
            subprocess.run(['pdflatex', '--version'], capture_output=True, text=True)
        except FileNotFoundError:
            print("Error: pdflatex not found. Please ensure LaTeX is installed and in your PATH")
            return False
            
        # Run pdflatex twice to ensure proper rendering of all elements
        for i in range(2):
            print(f"\nRunning pdflatex (pass {i+1})...")
            
            cmd = [
                'pdflatex',
                '-interaction=nonstopmode',
                f'-output-directory={output_dir}',
                tex_file_path
            ]
            print(f"Running command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                cwd=working_dir,
                capture_output=True,
                text=True,
                shell=True  # Add shell=True for Windows
            )
            
            # Print full output for debugging
            print("\nCommand Output:")
            print(result.stdout)
            
            if result.stderr:
                print("\nErrors:")
                print(result.stderr)
            
            if result.returncode != 0:
                print(f"\nPdflatex failed with return code: {result.returncode}")
                return False
                
        return True
        
    except Exception as e:
        print(f"Error compiling LaTeX: {str(e)}")
        print(f"Exception type: {type(e)}")
        import traceback
        traceback.print_exc()
        return False

# After generating output.tex
tex_file_path = 'output.tex'
output_dir = 'pdf'

print("Starting PDF generation...")
success = compile_latex_to_pdf(tex_file_path, output_dir)
if success:
    print("PDF generated successfully")
    pdf_path = os.path.join(output_dir, 'output.pdf')
    if os.path.exists(pdf_path):
        print(f"PDF file created at: {pdf_path}")
    else:
        print("Warning: PDF file not found in output directory")
else:
    print("Failed to generate PDF")