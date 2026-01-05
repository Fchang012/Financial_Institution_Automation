import sys
from playwright.sync_api import sync_playwright
from banks.definitions import BankOfAmerica, Chase, Citi, CapitalOne

def main():
    # Define the list of banks in the specific order requested
    # Note: Citi is requested twice.
    banks_to_process = [
        BankOfAmerica(),
        Chase(),
        Citi(),
        Citi(),
        CapitalOne()
    ]

    print("Starting Bank Automation Script...")
    
    with sync_playwright() as p:
        # Launch browser (headless=False so user can see and interact)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        for bank in banks_to_process:
            bank.process(page)

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
