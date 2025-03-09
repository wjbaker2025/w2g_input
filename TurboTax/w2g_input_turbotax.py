import os
import json
import pandas as pd
from playwright.sync_api import sync_playwright

# --- CONFIGURATION ---
# Set USE_PERSISTENT_PROFILE to True so that the browser launches using your saved credentials.
USE_PERSISTENT_PROFILE = True
# Provide the path to your Edge/Chromium user data directory (the profile that holds your saved logins).
PROFILE_PATH = "path/to/your/edge/profile"  # <-- Update this with your actual profile path

CHECKPOINT_FILE = "checkpoint.json"

def load_checkpoint():
    """Load the last completed row index from a JSON file."""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            data = json.load(f)
            return data.get("last_completed_index", -1)
    return -1

def save_checkpoint(index):
    """Save the last completed row index to a JSON file."""
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump({"last_completed_index": index}, f)

def main():
    # Read CSV (assumes data is already clean)
    df = pd.read_csv("W-2G_All.csv")
    df.fillna("", inplace=True)

    # Determine the starting row from checkpointing.
    start_index = load_checkpoint()
    print(f"Starting from row index {start_index + 1}.")

    with sync_playwright() as pw:
        # Launch a persistent browser context so that your saved credentials are used.
        if USE_PERSISTENT_PROFILE:
            context = pw.chromium.launch_persistent_context(
                user_data_dir=PROFILE_PATH,
                channel='msedge',
                headless=False
            )
            page = context.pages[0] if context.pages else context.new_page()
        else:
            # Fallback (should not be used as no credentials are hardcoded)
            browser = pw.chromium.launch(channel='msedge', headless=False)
            context = browser.new_context()
            page = context.new_page()

        # 1. Navigate to the H&R Block account login page.
        page.goto("https://account.hrblock.com/")
        page.wait_for_load_state("networkidle")
        # At this point, your browser will prompt you to authenticate (using your saved passwords and preferred method).

        # 2. After login, navigate to the My Taxes page.
        page.wait_for_load_state("networkidle", timeout=30000)
        page.goto("https://mytaxes.hrblock.com/")
        page.wait_for_load_state("networkidle", timeout=30000)
        page.wait_for_selector("button:has-text('Add')", timeout=30000)

        # 3. Process each W-2G form from the CSV.
        for index, row in df.iterrows():
            # Skip rows that were already processed
            if index <= start_index:
                continue

            print(f"Filling W-2G #{index + 1}: {row['payers_name']}")
            add_buttons = page.query_selector_all("button:has-text('Add')")
            if index < len(add_buttons):
                add_buttons[index].click()
            else:
                print(f"No more 'Add' buttons at entry {index + 1}. Check the number of entries.")
                break

            # Nonstandard W-2G question: Always select "No" then click Next.
            page.wait_for_selector("input[type='radio'][value='No']", timeout=10000)
            page.click("input[type='radio'][value='No']")
            page.click("text='Next'")

            # Payer Information: fill in payer name, zip (which auto-populates city/state), address, federal ID, and phone.
            page.wait_for_selector("input[name='payer_name']", timeout=10000)
            page.fill("input[name='payer_name']", row["payers_name"])
            page.fill("input[name='zip']", str(row["zip"]))
            page.press("input[name='zip']", "Tab")
            page.wait_for_timeout(1000)  # Allow auto-population of city/state
            page.fill("input[name='address']", row["address"])
            page.fill("input[name='federal_id_number']", row["federal_id_number"])
            page.fill("input[name='phone']", row.get("phone", ""))
            page.click("text='Next'")

            # Double-check your name and address.
            page.wait_for_selector("text='Double-check your name and address.'", timeout=10000)
            page.click("text='Next'")

            # Fill in Boxes 1-18.
            page.wait_for_selector("input[name='amount_won']", timeout=10000)
            page.fill("input[name='amount_won']", str(row["1_gross_winnings"]))
            page.fill("input[name='date_won']", row["2_date_won"])
            page.fill("input[name='type_of_wager']", row["3_type_of_wager"])
            page.fill("input[name='federal_tax_withheld']", str(row["4_federal_tax_withheld"]))
            page.fill("input[name='transaction']", row["5_transaction"])
            page.fill("input[name='race']", row.get("6_race", ""))
            page.fill("input[name='identical_wagers']", row.get("7_identical_wagers", ""))
            page.fill("input[name='cashier']", row.get("8_cashier", ""))
            page.fill("input[name='first_id']", row["11_first_id"])

            # If state info is provided, fill in state-specific fields.
            if row.get("13_state"):
                page.select_option("select[name='state']", row["13_state"])
                page.fill("input[name='payers_state_id']", row["payers_state_id"])
                page.fill("input[name='state_tax_withheld']", str(row["15_state_income_tax_withheld"]))

            page.click("text='Next'")
            page.wait_for_timeout(2000)  # Short pause between entries

            # Update checkpoint so that this row is marked as completed.
            save_checkpoint(index)

        print("All W-2G forms submitted—fuck yes!")
        context.close()

if __name__ == "__main__":
    main()
