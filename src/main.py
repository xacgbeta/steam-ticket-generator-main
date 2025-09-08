import os
import sys
import time
import base64
import ctypes
from ctypes import c_bool, c_uint32, c_uint64, c_void_p, byref

class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print(f"{Style.BRIGHT_BLACK}--- Steam Encrypted App Ticket Generator ---{Style.RESET}\n")

def print_error(message: str):
    print(f"\n{Style.RED}{Style.BOLD}Error:{Style.RESET}{Style.RED} {message}{Style.RESET}")

def print_success(message: str):
    print(f"{Style.GREEN}✓ {message}{Style.RESET}")

def prompt_input(message: str) -> str:
    return input(f"{Style.CYAN}› {message}:{Style.RESET} ")

def generate_ticket(app_id: int) -> bool:
    os.environ["SteamAppId"] = str(app_id)
    os.environ["SteamGameId"] = str(app_id)
    try:
        dll_path = os.path.join(os.path.dirname(__file__), "steam_api64.dll")
        steam = ctypes.cdll.LoadLibrary(dll_path)
    except OSError:
        print_error("steam_api64.dll not found. Place it in the same directory as the script.")
        return False
    
    steam.SteamAPI_InitFlat.restype = ctypes.c_int
    steam.SteamAPI_SteamUser_v023.restype = c_void_p
    steam.SteamAPI_ISteamUser_RequestEncryptedAppTicket.argtypes = [c_void_p, c_void_p, c_uint32]
    steam.SteamAPI_ISteamUser_GetEncryptedAppTicket.argtypes = [c_void_p, c_void_p, c_uint32, ctypes.POINTER(c_uint32)]
    steam.SteamAPI_ISteamUser_GetEncryptedAppTicket.restype = c_bool
    steam.SteamAPI_ISteamUser_GetSteamID.argtypes = [c_void_p]
    steam.SteamAPI_ISteamUser_GetSteamID.restype = c_uint64

    if steam.SteamAPI_InitFlat(None) != 0:
        print_error("Steam API initialization failed.")
        print(f"{Style.YELLOW}  Make sure Steam is running, you are logged in, and the App ID is correct.{Style.RESET}")
        return False
        
    user = steam.SteamAPI_SteamUser_v023()
    if not user:
        print_error("Failed to get Steam user interface.")
        return False

    print(f"\n{Style.BRIGHT_BLACK}Requesting ticket from Steam...{Style.RESET}")
    steam.SteamAPI_ISteamUser_RequestEncryptedAppTicket(user, None, 0)
    time.sleep(1.5)
    ticket_buf = (ctypes.c_ubyte * 2048)()
    ticket_len = c_uint32(0)

    if not steam.SteamAPI_ISteamUser_GetEncryptedAppTicket(user, ticket_buf, 2048, byref(ticket_len)):
        print_error("Failed to get encrypted app ticket.")
        print(f"{Style.YELLOW}  This usually means the logged-in Steam account does not own the game (App ID: {app_id}).{Style.RESET}")
        return False

    ticket_bytes = bytes(ticket_buf[:ticket_len.value])
    ticket_b64 = base64.b64encode(ticket_bytes).decode("utf-8")
    steamid = steam.SteamAPI_ISteamUser_GetSteamID(user)

    print(f"\n{Style.GREEN}{Style.BOLD}Ticket generated successfully!{Style.RESET}")
    print(f"  {Style.BRIGHT_BLACK}Steam ID:           {Style.RESET}{Style.BRIGHT_WHITE}{steamid}{Style.RESET}")
    print(f"  {Style.BRIGHT_BLACK}Encrypted Ticket:   {Style.RESET}{Style.BRIGHT_WHITE}{ticket_b64[:70]}...{Style.RESET}")
    
    create_cfg = prompt_input("\nCreate configs.user.ini? (y/n)").strip().lower()
    if create_cfg in ["", "y", "yes"]:
        create_config(steamid, ticket_b64)

    return True

def create_config(steamid: int, ticket: str):
    try:
        with open("configs.user.ini", "w", encoding="utf-8") as f:
            f.write("[user::general]\n")
            f.write(f"account_steamid={steamid}\n")
            f.write(f"ticket={ticket}\n")
        print_success("configs.user.ini created.")
    except IOError as e:
        print_error(f"Could not write to configs.user.ini: {e}")

def main_loop():
    while True:
        clear_screen()
        print_header()
        
        try:
            app_id_str = prompt_input("Enter the App ID")
            if not app_id_str.isdigit():
                print_error("Invalid App ID. Please enter numbers only.")
            else:
                app_id = int(app_id_str)
                generate_ticket(app_id)

        except KeyboardInterrupt:
            print(f"\n\n{Style.YELLOW}Operation cancelled by user.{Style.RESET}")

        choice = input(f"\n{Style.BRIGHT_BLACK}Run again? (y/n): {Style.RESET}").strip().lower()
        if choice in ["n", "no"]:
            break

if __name__ == "__main__":
    main_loop()
