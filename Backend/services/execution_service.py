import subprocess
import os

UPLOAD_DIR = "storage/user_files"

def execute_python_code(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        return "File not found!"
    
    try:
        # Execute the python file securely with timeout 
        result = subprocess.run(
            ["python", file_path],
            capture_output= True, text= True, timeout= 5    #prevents infinite loops
        )
        return result.stdout if result.returncode == 0 else result.stderr
    
    except subprocess.TimeoutExpired:
        return "Error: Code execution timed out!"
    
    except Exception as e:
        return f"Execution error: {str(e)}"
    