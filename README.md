# Disclaimer
This project is not a modification of the original Rust implementation.
It is simply a Python reimplementation of the same logic, created for convenience and ease of use by non-developers.

# Steam Ticket Generator

This project provides an implementation of a encrypted app ticket generator for Steam. The generated ticket can then be used to run games that require a valid ticket to check for game ownership (ex. Denuvo protected games).

**Note for Denuvo games:**
 - Denuvo protected games will also require to have the correct steam account id in the steam emulator settings.
 - Each Steam account can achieve at most 5 activations a day.
 - An EncryptedAppTicket expires after 20 minutes and can be used multiple times in that time span, using the same ticket won't bypass the 5 daily activations limit.

## Requirements
- Steam client running and logged in
- The account must own the game (App ID) for ticket generation to succeed
- Python 3.8+ (for running directly without .exe)

## Usage

1. **Build the project:**

    ```sh
    pip install pyinstaller
    pyinstaller --onefile main.py --add-binary "steam_api64.dll;."
    pyinstaller main.spec
    ```

    The resulting binary will be located in `/dist/main.exe`.

2. **Provide the steam_api64.dll file:**

    Place the `steam_api64.dll` file in the same directory as the main.py before compiling. This file is required to comunicate with the local Steam client.

3. **Run the generator:**

    Open steam on your computer, log in with the account you wish to use for the generation then run the program.
    Input the game's AppID when prompted. The program will use the currently logged in account to generate the ticket.
    It will output both the user's SteamID and the generated ticket in base64 format.

4. **Use the generated ticket:**
    It is possible to use the generated ticket with [GBE]([https://github.com/GittyGittyKit/gbe_fork/releases](https://gitlab.com/Mr_Goldberg/goldberg_emulator)) (that recently [merged](https://github.com/Detanup01/gbe_fork/pull/274) into the Detanup's fork 🎉).
    Copy the generated SteamID and ticket to `configs.user.ini` in the `account_steamid` and `ticket` fields respectively.
    ```ini
    [user::general]
    account_steamid=YOUR_STEAM_ID
    ticket=BASE64_ENCODED_TICKET
    ```

## Builds

Builds are available in the [releases](https://github.com/xacgbeta/steam-ticket-python-version/releases/tag/1.1.2) section of the repository.

The builds in the releases section will also include the `steam_api64.dll` file required to run the program. Otherwise you can download it from the [Steamworks SDK](https://partner.steamgames.com/doc/sdk). The minimum required version is 1.62.

## Disclaimer

This project is for educational and research purposes only. Use responsibly and respect software licenses.
