
def log(category, text):
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    colors = {
        "ERROR": "\033[91m",      
        "WARNING": "\033[93m",
        "INITIALIZATION": "\033[94m",
        "SYNCHRONIZATION": "\033[96m",
        "ENDC": "\033[0m"
    }
    color = colors.get(category, "")
    endc = colors["ENDC"]
    print(f'{color}[{timestamp}] [{category}] {text}{endc}')
