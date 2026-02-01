import sys
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from banks.definitions import BankOfAmerica, Chase, Citi, CapitalOne

#Load environment variables immediately
load_dotenv()

def main():
    BASE_DOWNLOAD_DIR = os.getenv("BASE_DOWNLOAD_DIR")

    # Define the sequence of banks to process and their specific download paths.
    # Each entry is a tuple: (BankInstance, "Path/To/Copy", "ClipboardString")
    # This ensures that even for duplicate banks (like Citi), you can set different paths.
    banks_to_process = [
        (Chase(),         f"{BASE_DOWNLOAD_DIR}/Chase",       "(C"),
        (BankOfAmerica(), f"{BASE_DOWNLOAD_DIR}/BOA",         "(BOA)"),
        (Citi(),          f"{BASE_DOWNLOAD_DIR}/Citi_COSTCO", "(Citi_COSTCO)"),
        (Citi(),          f"{BASE_DOWNLOAD_DIR}/Citi_DC",     "(Citi_DC)"),
        (Chase(),         f"{BASE_DOWNLOAD_DIR}/K_Chase",     "(K_C"),
        (CapitalOne(),    f"{BASE_DOWNLOAD_DIR}/K_CapitalOne", "(K_COVX)")
    ]

    print("Starting Bank Automation Script...")
    
    with sync_playwright() as p:
        # Launch browser (headless=False so user can see and interact)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        for bank, save_path, clipboard_string in banks_to_process:
            page = context.new_page()
            bank.process(page, save_path=save_path, clipboard_string=clipboard_string)

        print("All banks processed.")
        input("Press Enter to close the browser and exit...")
        browser.close()
    
    print("Script finished.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting.")
        sys.exit(0)
