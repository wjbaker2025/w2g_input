# H&R Block Automation Walkthrough

This document details the H&R Block automation script (`w2g_input_hrblock.py`). The script reads W-2G data from a CSV file, auto-fills online forms, and uses checkpointing to resume if interrupted. It leverages your browser’s saved credentials via a persistent profile for secure login (e.g., Windows Hello).

## CSV File Format

**Important:**  
Your CSV must include the required headers exactly as defined in the script:  
`payers_name`, `zip`, `address`, `federal_id_number`, `phone`, `1_gross_winnings`, `2_date_won`, `3_type_of_wager`, `4_federal_tax_withheld`, `5_transaction`, `6_race`, `7_identical_wagers`, `8_cashier`, `11_first_id`, `13_state`, `payers_state_id`, `15_state_income_tax_withheld`.  
Follow the template provided in `w-2g_all_template.csv`.

---

## Code Walkthrough with In-Depth Explanations

### 1. Loading CSV Data & Checkpointing

The script reads your CSV and uses checkpointing to resume where you left off:

```python
# Load CSV data and fill missing values with empty strings
df = pd.read_csv("w-2g_all.csv")
df.fillna("", inplace=True)

# Determine which row to start from based on checkpoint
start_index = load_checkpoint()
print(f"Starting from row index {start_index + 1}.")
```

*Explanation:* This code ensures your data is complete and resumes processing from the last completed row stored in `checkpoint.json`.

---

### 2. Launching with a Persistent Browser Profile

The script uses your browser’s stored credentials for secure login:

```python
context = pw.chromium.launch_persistent_context(
    user_data_dir=PROFILE_PATH,  # Path to your browser's profile directory
    channel='msedge',
    headless=False
)
page = context.pages[0] if context.pages else context.new_page()
```

*Explanation:* A persistent context lets your browser use saved logins (e.g., Windows Hello or face recognition) without hardcoding any credentials.

---

### 3. Form Submission Loop

For each CSV row, the script fills out the form and updates the checkpoint:

```python
for index, row in df.iterrows():
    if index <= start_index:
        continue  # Skip already processed rows

    # Click the "Add" button to start a new form entry
    add_buttons = page.query_selector_all("button:has-text('Add')")
    if index < len(add_buttons):
        add_buttons[index].click()
    else:
        print(f"No more 'Add' buttons at entry {index + 1}.")
        break

    # Answer the nonstandard W-2G question
    page.wait_for_selector("input[type='radio'][value='No']", timeout=10000)
    page.click("input[type='radio'][value='No']")
    page.click("text='Next'")

    # Fill in payer information
    page.wait_for_selector("input[name='payer_name']", timeout=10000)
    page.fill("input[name='payer_name']", row["payers_name"])
    page.fill("input[name='zip']", str(row["zip"]))
    page.press("input[name='zip']", "Tab")
    page.wait_for_timeout(1000)  # Allow auto-population of city/state
    page.fill("input[name='address']", row["address"])
    page.fill("input[name='federal_id_number']", row["federal_id_number"])
    page.fill("input[name='phone']", row.get("phone", ""))
    page.click("text='Next'")

    # Confirm personal info and fill form details
    page.wait_for_selector("text='Double-check your name and address.'", timeout=10000)
    page.click("text='Next'")
    page.wait_for_selector("input[name='amount_won']", timeout=10000)
    # Fill in additional fields here as needed...
    page.click("text='Next'")
    page.wait_for_timeout(2000)  # Short pause between entries

    # Save progress in checkpoint
    save_checkpoint(index)
```

*Explanation:* This loop processes each CSV entry, simulating user interaction (clicks, fills, waits) and saving progress after each successful form submission.

---

## Visual Walkthrough with Screenshots

### 1. Launch & Login  
Your browser launches using your persistent profile and prompts you to log in with your saved credentials.  
![Login Screen](./images/1_login.png)

### 2. Authentication Prompt  
Authenticate using your usual method (e.g., Windows Hello).  
![Auth Prompt](./images/2_auth.png)

### 3. Navigate to "My Taxes"  
After login, the script navigates automatically to the My Taxes page.  
![My Taxes](./images/3_mytaxes.png)

### 4. Nonstandard W-2G Question  
The script reaches the nonstandard W-2G question and auto-selects “No.”  
![Nonstandard W-2G](./images/4_nonstandard.png)

### 5. Confirm Nonstandard Selection  
It confirms the selection by clicking “Next.”  
![Confirm Nonstandard](./images/5_confirm.png)

### 6. Enter Payer Information  
Fills in payer details: name, ZIP (auto-populates city/state), address, federal ID, and phone.  
![Payer Info](./images/6_payer_info.png)

### 7. ZIP Auto-Population  
Waits for the ZIP code to auto-populate the city and state fields.  
![ZIP Auto-Population](./images/7_zip_auto.png)

### 8. Personal Information Display  
Displays your personal info (with SSN greyed out) for review.  
![Personal Info](./images/8_personal_info.png)

### 9. Double-Check Confirmation  
Clicks “Next” on the double-check screen to confirm details.  
![Double-Check](./images/9_double_check.png)

### 10. Begin Form Details (Part 1)  
Starts filling in form details (e.g., gross winnings, date won, wager type).  
![Form Details Part 1](./images/10_form_details1.png)

### 11. Complete Form Details (Part 2)  
Fills in remaining fields, including state-specific data if available.  
![Form Details Part 2](./images/11_form_details2.png)

### 12. Final Submission & Checkpointing  
Submits the form and updates the checkpoint for seamless resumption.  
![Final Submission](./images/12_final.png)

---

## Final Thoughts

This automation script dramatically simplifies the tedious process of submitting W-2G forms on H&R Block’s website. Ensure your CSV file exactly follows the provided template, and enjoy a smoother, more efficient tax season with robust checkpointing and secure login!

Happy automating!
