from abc import ABC, abstractmethod
from playwright.sync_api import Page

class BankSite(ABC):
    """Abstract base class for a bank website."""

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

    def process(self, page: Page):
        """
        Navigates to the bank's URL and pauses for manual interaction.
        Subclasses can override this to add specific automation steps.
        """
        print(f"--- Processing {self.name} ---")
        print(f"Navigating to {self.url}...")
        try:
            page.goto(self.url)
            # Wait for reasonable load (domcontentloaded is faster than load, 
            # usually sufficient for user to start seeing things)
            page.wait_for_load_state("domcontentloaded") 
        except Exception as e:
            print(f"Error navigating to {self.name}: {e}")
            return

        print(f"Opened {self.name}. Perform your manual actions.")
        self.manual_intervention_hook(page)
        print(f"Finished processing {self.name}.\n")

    def manual_intervention_hook(self, page: Page):
        """
        Hook for manual intervention. 
        In the future, automated steps can be added here or before/after this call.
        """
        input(f"Pres 'Enter' to continue to the next site (or exit if last)...")
