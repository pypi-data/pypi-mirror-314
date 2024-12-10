## FamilyMedT - Family Medication Tracking System

Developed by Yuzhou Wang and Yubo Wang.

## Overview
FamilyMedT is a Python-based medication management system designed to help families track and manage medications for multiple family members. It provides features for monitoring medication inventory, setting up reminders for low stock, and managing prescriptions.

## Features
- Multi-user family member management
- Medication inventory tracking
- Prescription medication management
- Automatic low stock alerts
- Stock level monitoring and reporting
- Prescription expiration tracking
- Data persistence using CSV storage

## Project Structure
```
FamilyMedT/
├── __init__.py
│
├── medication_management/
│   ├── __init__.py
│   ├── medication.py        # Base medication class
│   ├── prescription.py      # Prescription medication class
│   └── inventory.py         # Inventory management
│
├── user_management/
│   ├── __init__.py
│   ├── family.py           # Family member management
│   └── reminder.py         # Reminder system
│
│
├── data/                    # Data storage directory
│   └── (CSV files)
│
├── main.py                  # Main application entry
└── README.md
```

## Installation
1. Clone the repository:
```bash
git clone https://github.com/MDS-2024-Labs/project-step-1-wyuzhou6.git
cd FamilyMedT
```

2. Install required dependencies:
```bash
pip install pandas
```

## Usage
Run the main application:
```bash
python main.py
```

### Main Menu Options:
1. Add Family Member
2. Switch to Family Member
3. List Family Members
4. Add Medication for Current Member
5. Update Stock for Current Member
6. Generate Stock Report for Current Member
7. List Reminders for Current Member
8. List Prescription Medications
9. Generate Prescription Report
10. Delete Family Member
11. Delete Medication for Current Member
12. Exit



## Key Components

### Medication Management
- Basic medication tracking
- Prescription medication handling
- Stock level monitoring
- Expiration date tracking

### Inventory Management
- Add/remove medications
- Update stock levels
- Generate inventory reports
- Track low stock alerts

### Family Management
- Multiple family member support
- Individual medication tracking
- Member-specific inventory

### Reminder System
- Automatic low stock alerts
- Custom reminder messages
- Per-member reminder tracking

## Data Storage
- All data is stored in CSV format
- Separate files for each family member's inventory
- Centralized reminder storage
- Automatic data persistence

## Development
- Written in Python 3.6+
- Uses pandas for data management
- Modular design for easy extension
- Comprehensive unit testing

## Future Improvements
- GUI interface
- Database storage option
- Mobile app integration
- Multiple language support
- Email notifications
- Medication interaction checking

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request