import subprocess
import os
import shutil

if not os.path.exists("arxml_parsing.exe"):
    parameter = "--onefile arxml_parsing.py"
    command = f"pyinstaller.exe {parameter}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)      

    # Check the result
    if result.returncode == 0:
        print("Application ran successfully!")
        print("Standard Output:")
        print(result.stdout)
    else:
        print("Application encountered an error.")
        print("Error Output:")
        print(result.stderr)   
          
    shutil.copy("dist/arxml_parsing.exe", ".")
    os.remove("arxml_parsing.spec")
    shutil.rmtree("build")
    shutil.rmtree("dist")
        
# subprocess.run("arxml_parsing.exe", shell=True, capture_output=True, text=True)