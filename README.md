# W-2G Automatic Input for H&R Block and TurboTax

Welcome to **W-2G Automation for Tax Platforms**! Tired of manually entering handpay data every tax season? This project automates W-2G form submission for tax platforms using Python and Playwright. I keep a log every time I get a casino handpay so you never have to retype the same damn data again.

## Repository Structure
,,, 
w2g_input/
├── H&R Block/
│   ├── w2g_input_hrblock.py      # H&R Block automation script
│   ├── W-2G_All.csv              # CSV file with your data (ensure correct column headers)
│   ├── README.md                 # H&R Block-specific instructions & walkthrough
│   └── images/                   # 12 screenshots for the H&R Block playthrough
├── TurboTax/
│   ├── w2g_input_turbotax.py     # TurboTax automation script (planned/in development)
│   └── README.md                 # Instructions for TurboTax (coming soon)
├── .gitignore                    # Ignores checkpoint.json and other temporary files
└── LICENSE                       # MIT License
,,, 

## Overview

- **Dual Platform Support:** Automates form entry for H&R Block (and soon TurboTax).
- **Secure & Automated:** Uses your browser’s persistent profile—no hardcoded credentials.
- **Checkpointing:** Resumes automatically if interrupted.
- **CSV-Driven:** Reads W-2G data from a CSV file (follow the provided CSV template with correct headers).

Happy automating—say goodbye to tedious data entry and hello to a smarter tax season!
