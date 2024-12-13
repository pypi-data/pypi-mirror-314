from huggingface_hub import hf_hub_download
def download_model(repo_id,filename):
    # Download the file
    model_path = hf_hub_download(repo_id=repo_id, filename=filename)
    print("Model downloaded to:", model_path)
    return model_path
import pyfiglet
import time
from termcolor import colored
import sys
isprinted=False
# Function to print the designed text with animation
def print_svnm_intro():
    global isprinted
    if isprinted:
        colored_art = colored("svnm", 'green')
        sys.stdout.write(colored_art)
        return
    # ASCII Art for 'SVNM'
    ascii_art = pyfiglet.figlet_format("S V N M")
    colored_art = colored(ascii_art, 'green')

    # Short, neat summary text
    summary = '''
    SVNM Package:
    - Easy-to-use models for everyone
    - Developed by: svn.murali
    - Simplifying model usage for you
    '''
    colored_text=colored(summary, 'cyan')
    # Animation Effect for ASCII Art
    sys.stdout.write(colored_art)
    sys.stdout.flush()
    sys.stdout.write(colored_text)
    isprinted=True


    
