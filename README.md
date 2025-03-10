# (Work In Progress) W-2G Input Automation for H&R Block and TurboTax

Welcome to **W-2G Input Automation**! Tired of manually entering handpay data every tax season? This project automates W-2G form submission for tax platforms using Python and Playwright. Simply keep a log of every casino handpay you recieve soon after you recieve it and at the beginning of the next year you won't have to sit there and maually type in every single handpay you got for the entire year.

## Repository Structure
```bash
w2g_input/
├── H&R Block/
│   ├── w2g_input_hrblock.py      # H&R Block automation script
│   ├── w-2g_all_template.csv     # CSV file with your data (ensure correct column headers)
│   ├── README.md                 # H&R Block-specific instructions & walkthrough
│   └── images/                   # 12 screenshots for the H&R Block playthrough
├── TurboTax/
│   ├── w2g_input_turbotax.py     # TurboTax automation script (planned/in development)
│   └── README.md                 # Instructions for TurboTax (coming soon)
├── .gitignore                    # Ignores checkpoint.json and other temporary files
└── LICENSE                       # MIT License
```

## Overview

- **Two Platform Support:** Automates form entry for H&R Block (and soon TurboTax separately).
- **Secure & Automated:** Uses your browser’s persistent profile—no hardcoded credentials.
- **Checkpointing:** Resumes automatically if interrupted.
- **CSV-Driven:** Reads W-2G data from a CSV file (follow the provided CSV template with correct headers).

In the future I plan on making an executable that will provide you with the options of TurboTax or H&R Block, allow you to upload your .csv file and a simple start that will do all the manual work for you, providing an opportunity at the end to uninstall...

Happy automating—say goodbye to tedious data entry and hello to a smarter tax season!
