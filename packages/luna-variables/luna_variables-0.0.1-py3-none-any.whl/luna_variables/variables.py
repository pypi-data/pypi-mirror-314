# luna_variables/variables.py

# Color Variables
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"
BRIGHT = '\033[1m'
# Main
error = f"{BRIGHT}{WHITE}[{RED}!{WHITE}] {RED}LunaError: {YELLOW}"
solution = f"{WHITE}[{GREEN}✔{WHITE}] {GREEN}LunaSolution: {WHITE}"
search = f"{BRIGHT}{WHITE}[{BLUE}🔍{WHITE}]{BLUE} LunaSearch: {WHITE}"
msg = f"{BRIGHT}{WHITE}[{RED}☾{WHITE}] {RED}LunaTools:{WHITE}"