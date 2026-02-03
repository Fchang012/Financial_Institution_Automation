import sys
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from banks.definitions import BankOfAmerica, Chase, Citi, CapitalOne, Vanguard, TRowePrice, ETrade, Fidelity

#Load environment variables immediately
load_dotenv()

def main():
    BASE_DOWNLOAD_DIR = os.getenv("BASE_DOWNLOAD_DIR")

    # TOGGLE: Set to "BANKS" or "BROKERAGES"
    MODE = "BANKS"
    # MODE = "BROKERAGES"

    # Define the sequence of banks to process
    banks_to_process = [
        (Chase(),         f"{BASE_DOWNLOAD_DIR}/Chase",       "(C"),
        (BankOfAmerica(), f"{BASE_DOWNLOAD_DIR}/BOA",         "(BOA)"),
        (Citi(),          f"{BASE_DOWNLOAD_DIR}/Citi_COSTCO", "(Citi_COSTCO)"),
        (Citi(),          f"{BASE_DOWNLOAD_DIR}/Citi_DC",     "(Citi_DC)"),
        (Chase(),         f"{BASE_DOWNLOAD_DIR}/K_Chase",     "(K_C"),
        (CapitalOne(),    f"{BASE_DOWNLOAD_DIR}/K_CapitalOne", "(K_COVX)")
    ]

    # Define the sequence of brokerages to process
    brokerages_to_process = [
        (Vanguard(),      f"{BASE_DOWNLOAD_DIR}/Vanguard",    "(VG)"),
        (TRowePrice(),    f"{BASE_DOWNLOAD_DIR}/TRowePrice",  "(TRP)"),
        (ETrade(),        f"{BASE_DOWNLOAD_DIR}/ETrade",      "(ET)"),
        (Fidelity(),      f"{BASE_DOWNLOAD_DIR}/Fidelity",    "(FID)"),
        (TRowePrice(),    f"{BASE_DOWNLOAD_DIR}/K_TRowePrice",  "(K_TRP)"),
    ]

    items_to_process = banks_to_process if MODE == "BANKS" else brokerages_to_process

    print(f"Starting Automation Script in {MODE} mode...")
    
    with sync_playwright() as p:
        # Launch browser (headless=False so user can see and interact)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        for site, save_path, clipboard_string in items_to_process:
            page = context.new_page()
            try:
                site.process(page, save_path=save_path, clipboard_string=clipboard_string)
            except Exception as e:
                 print(f"Error processing {site.name}: {e}")

        print(f"All {MODE.lower()} processed.")
        input("Press Enter to close the browser and exit...")
        browser.close()
    
    print("Script finished.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting.")
        sys.exit(0)
