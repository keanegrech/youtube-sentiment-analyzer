import subprocess
import sys

print(
    """\
##  ##    ## ##     ##     
##  ##   ##   ##     ##    
##  ##   ####      ## ##   
 ## ##    #####    ##  ##  
  ##         ###   ## ###  
  ##     ##   ##   ##  ##  
  ##      ## ##   ###  ##     
                    """
)

print("Welcome to the setup.py file")
print("This file will help you setup the project")
print("Make sure that PIP is installed and working on your system")

choice = input("Do you want to continue? (y/n): ")

if choice.lower() != "y":
    print("Exiting the setup.py file")
    exit()

print("Installing the required packages")


def install(package):
    """
    Installs the given package using pip
    
    Parameters:
    package (str): The package to install
    
    Returns:
    None
    """
    print(f"Installing {package}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


f = open("requirements.txt", "r")
for line in f:
    install(line)

print("All the required packages have been installed")

print("Downloading required NLTK packages")

import nltk

print("Downloading punkt")
nltk.download("punkt")
print("Downloading wordnet")
nltk.download("wordnet")

print("All the required NLTK packages have been installed")

print("Setup is complete")
print("Make sure to fill in the API key in the .env file")
print("Run the application by typing python main.py")
