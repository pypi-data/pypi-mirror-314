# Optional: Add version or metadata
__version__ = "0.1.0"
import pyfiglet
import time
from termcolor import colored
import sys
isprinted=False
# Function to print the designed text with animation
def print_svnm_intro():
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
# Call the function to execute
if not isprinted:
    print_svnm_intro()
else:
    sys.stdout.write(colored_art = colored("~svnm", 'green'))
