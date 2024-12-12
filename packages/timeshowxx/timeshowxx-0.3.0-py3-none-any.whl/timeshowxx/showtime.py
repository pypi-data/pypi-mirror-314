from colorama import Fore, Style, init

# Initialize Colorama to auto-reset styles after each print
init(autoreset=True)

def show_time():
    """Display credits for the developer."""
    title = f"""
{Fore.GREEN}====================================================
        Telegram Bot https://t.me/smspanelil
{Fore.GREEN}====================================================
"""
    credits = f"""
{Fore.CYAN}Developed by: {Fore.YELLOW}@Justask6
{Fore.CYAN}Telegram: {Fore.YELLOW}https://t.me/smspanelil
{Fore.GREEN}====================================================
"""
    print(title + credits)
