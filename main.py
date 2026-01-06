import sys
from playwright.sync_api import sync_playwright
from banks.definitions import BankOfAmerica, Chase, Citi, CapitalOne

def main():
    BASE_DOWNLOAD_DIR = "/home/USER/CUSTOM_PATH"

    # Define the sequence of banks to process and their specific download paths.
    # Each entry is a tuple: (BankInstance, "Path/To/Copy")
    # This ensures that even for duplicate banks (like Citi), you can set different paths.
    banks_to_process = [
        (BankOfAmerica(), f"{BASE_DOWNLOAD_DIR}/BOA"),
        (Chase(),         f"{BASE_DOWNLOAD_DIR}/Chase"),
        (Citi(),          f"{BASE_DOWNLOAD_DIR}/Citi_Personal"),
        (Citi(),          f"{BASE_DOWNLOAD_DIR}/Citi_Business"),
        (CapitalOne(),    f"{BASE_DOWNLOAD_DIR}/CapitalOne")
    ]

    print("Starting Bank Automation Script...")
    
    with sync_playwright() as p:
        # Launch browser (headless=False so user can see and interact)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        for bank, save_path in banks_to_process:
            page = context.new_page()
            bank.process(page, save_path=save_path)

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
