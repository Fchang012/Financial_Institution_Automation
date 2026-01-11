from abc import ABC, abstractmethod
import pyperclip
import os
import tkinter
from tkinter import filedialog
from playwright.sync_api import Page, Download
import subprocess

class BankSite(ABC):
    """Abstract base class for a bank website."""

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

    def copy_to_clipboard(self, text: str):
        """
        Attempts to copy text to clipboard using pyperclip, falling back to 
        system commands (wl-copy, xclip, etc.) if pyperclip fails.
        """
        try:
            pyperclip.copy(text)
            print(f"  [Clipboard] Copied to clipboard (via pyperclip): '{text}'")
            return
        except Exception as e_pyperclip:
            print(f"  [Warning] Pyperclip failed: {e_pyperclip}. Trying system fallback...")

        # Fallback for Wayland/Linux if pyperclip fails
        try:
            # Try wl-copy (Wayland)
            subprocess.run(["wl-copy"], input=text.encode('utf-8'), check=True)
            print(f"  [Clipboard] Copied to clipboard (via wl-copy): '{text}'")
            return
        except FileNotFoundError:
            pass # wl-copy not found
        except Exception as e:
            print(f"  [Warning] wl-copy failed: {e}")

        # Fallback for X11 (or XWayland if wl-copy fails)
        try:
            # Try xclip
            subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode('utf-8'), check=True)
            print(f"  [Clipboard] Copied to clipboard (via xclip): '{text}'")
            return
        except FileNotFoundError:
            pass # xclip not found
        except Exception as e:
            print(f"  [Warning] xclip failed: {e}")

        try:
            # Try xsel
            subprocess.run(["xsel", "--clipboard", "--input"], input=text.encode('utf-8'), check=True)
            print(f"  [Clipboard] Copied to clipboard (via xsel): '{text}'")
            return
        except FileNotFoundError:
            pass # xsel not found
        except Exception as e:
            print(f"  [Warning] xsel failed: {e}")

        print(f"  [Error] Failed to copy '{text}' to clipboard using all available methods.")

    def process(self, page: Page, save_path: str = None, clipboard_string: str = None):
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

            # Pause for manual login
            print(f"Please log in to {self.name} and perform your downloads.")
            print(f"When you are finished with {self.name}, CLOSE THE BROWSER TAB to proceed to the next bank.")

            # Set up download listener if save_path is provided
            if save_path:
                page.on("download", lambda download: self.handle_download(download, save_path, clipboard_string))
                print(f"  [Auto-Download] Monitoring downloads to save to: {save_path}")
        except Exception as e:
            print(f"Error navigating to {self.name}: {e}")
            return

        if save_path and not clipboard_string:
            # Fallback: copy save_path if no specific clipboard_string is provided
            self.copy_to_clipboard(save_path)

        self.manual_intervention_hook(page)
        print(f"Finished processing {self.name}.\n")

    def handle_download(self, download: Download, save_path: str, clipboard_string: str = None):
        """
        Callback to handle file downloads with a manual 'Save As' dialog.
        """
        try:
            # Create the initial directory if it likely doesn't exist yet, 
            # just so the dialog has somewhere valid to start.
            if save_path:
                os.makedirs(save_path, exist_ok=True)

            print(f"  [Download] File detected: {download.suggested_filename}")
            print(f"  [Action Required] Please select a save location in the popup window...")

            # Initialize Tkinter and hide the main window
            root = tkinter.Tk()
            root.withdraw()
            # Bring dialog to front (may not work on all OS/window managers, but helps)
            root.attributes('-topmost', True)

            # Open Save As dialog
            # initialdir = save_path (the default for this bank)
            # initialfile = the browser's suggested filename
            
            if clipboard_string:
                self.copy_to_clipboard(clipboard_string)

            file_path = filedialog.asksaveasfilename(
                title=f"Save Download from {self.name}",
                initialdir=save_path,
                initialfile=download.suggested_filename,
                confirmoverwrite=True
            )
            
            # Clean up Tkinter
            root.destroy()

            if file_path:
                # User selected a path and clicked Save
                download.save_as(file_path)
                print(f"  [Success] Saved to: {file_path}")
            else:
                # User clicked Cancel
                print("  [Cancelled] User cancelled the save dialog. File not saved.")
                # Optional: download.delete() to clean up temp file immediately, 
                # though Playwright handles this eventually.

        except Exception as e:
            print(f"  [Error] Failed to save file: {e}")

    def manual_intervention_hook(self, page: Page):
        """
        Hook for manual intervention. 
        In the future, automated steps can be added here or before/after this call.
        """
        print(f"Waiting for user to close the {self.name} tab...")
        page.wait_for_event("close", timeout=600000) # 10 minutes
