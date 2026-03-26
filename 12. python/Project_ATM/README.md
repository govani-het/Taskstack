# ATM Simulation System

## Description

This is a comprehensive Python-based simulation of an ATM (Automated Teller Machine) system. The project demonstrates banking operations including user authentication, deposits, withdrawals, PIN changes, balance checks, and administrative functions for managing banks and ATMs. It supports cross-bank transactions with appropriate limits and fees.

## Features

### User Features
- **Secure Authentication**: Card number and PIN-based login with attempt limits
- **Deposit Money**: Deposit funds into your account (same-bank only)
- **Withdraw Money**: Withdraw cash with daily limits and cross-bank fees
- **Change PIN**: Update your PIN securely
- **Check Balance**: View current account balance
- **Transaction Limits**: Daily amount and count limits enforced

### Bank Management Features
- **Create Users**: Add new bank customers with validation
- **Create ATMs**: Set up new ATM locations
- **Show Users**: List all users in a bank
- **Show ATMs**: List all ATMs for a bank
- **Fund ATMs**: Add cash to ATM machines

### System Features
- **Cross-Bank Support**: Limited cross-bank withdrawals with fees
- **Data Persistence**: In-memory data storage (can be extended to database)
- **Input Validation**: Comprehensive validation for all inputs
- **Error Handling**: User-friendly error messages and retry mechanisms

## Installation

1. **Ensure Python 3.x is installed**:
   ```bash
   python --version
   ```
   The project requires Python 3.6 or higher.

2. **No external dependencies required** - The project uses only Python standard library modules.

## Usage

1. **Run the main application**:
   ```bash
   python main.py
   ```

2. **Choose your role**:
   - **1. User**: Access ATM functions
   - **2. Bank**: Access bank management functions
   - **3. Exit**: Quit the application

### As a User
1. Select an ATM location
2. Authenticate with card number and PIN
3. Choose from available operations:
   - Deposit
   - Withdraw
   - Change PIN
   - Check Balance

### As a Bank Administrator
1. Select a bank
2. Choose from administrative functions:
   - Create new user
   - Create new ATM
   - View users
   - View ATMs
   - Fund ATMs

## Project Structure

```
Project_ATM/
├── main.py                 # Main entry point
├── constant.py             # All constant values and messages
├── data.py                 # Sample data for banks, users, and ATMs
├── atm/                    # ATM-related modules
│   ├── __init__.py
│   └── atm_system.py       # ATM operations and user interface
└── bank/                   # Bank management modules
    ├── __init__.py
    └── bank.py             # Bank operations and user management
```

## Key Files Explanation

- **main.py**: Initializes the system and provides the main menu
- **constant.py**: Contains all string constants, limits, and configuration
- **data.py**: Sample data structure with predefined banks, users, and ATMs
- **atm/atm_system.py**: Handles ATM user interface and transaction logic
- **bank/bank.py**: Manages bank operations, user creation, and ATM management

## Sample Data

The system comes with sample data:
- **Banks**: State Bank (Navrangpura), National Bank (Satellite)
- **Users**: Pre-created users with cards, PINs, and balances
- **ATMs**: ATM locations with initial cash balances

## Transaction Rules

- **Deposit**: Minimum ₹100, multiples of ₹100, same-bank only
- **Withdrawal**: Minimum ₹100, multiples of ₹100, daily limits apply
- **Cross-bank**: 5% fee, maximum ₹10,000 per transaction
- **Daily Limits**: ₹1,00,000 total, 10 transactions per day
- **PIN Attempts**: Maximum 3 attempts before lockout

## Development

### Code Style
- Follows Python PEP 8 conventions
- Comprehensive error handling
- Modular design with separation of concerns
- Centralized constants for easy maintenance

### Extending the Project
- Add database persistence (SQLite, PostgreSQL)
- Implement GUI interface (Tkinter, PyQt)
- Add more transaction types (transfers, bill payments)
- Implement logging and audit trails
- Add encryption for sensitive data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open-source and available under the MIT License.

## Author

**Het Govani**

Developed as a Python programming project demonstrating object-oriented design and banking system concepts.

## Acknowledgments

- Built with Python standard library
- Inspired by real-world ATM and banking systems
- Educational project for learning Python development