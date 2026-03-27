# ATM Management System

A comprehensive ATM system built with Python that manages bank operations, user accounts, and ATM transactions with robust security features.

## Features

- **User Management**
  - Create new user accounts with Aadhar, PAN validation
  - First-time PIN change requirement for security
  - User authentication with card number and PIN
  - Balance checking and transaction history

- **ATM Operations**
  - Deposit money into accounts
  - Withdraw money with daily limits
  - Change PIN with PIN validation for each transaction
  - Check account balance
  - Cross-bank transaction support with fees

- **Bank Management**
  - Create and manage multiple banks
  - Set up ATM locations for banks
  - Manage bank vault transactions

- **Security**
  - PIN validation required for every transaction
  - 3 attempt limit per transaction
  - First-time PIN change enforcement
  - Secure password hashing
  - Per-transaction authentication

## System Requirements

- Python 3.x
- No external dependencies (uses only Python standard library)

## Project Structure

```
Project_ATM/
├── main.py                 # Main entry point
├── constant.py             # System constants and configurations
├── data.py                 # User, bank, and ATM data storage
├── README.md               # Project documentation
├── atm/
│   ├── __init__.py
│   └── atm_system.py       # ATM operations and user transactions
├── bank/
│   ├── __init__.py
│   └── bank.py             # Bank and user management
└── admin/
    ├── __init__.py
    └── admin.py            # Admin operations and monitoring
```

## Getting Started

### Installation

1. Clone or download the project
2. Navigate to the project directory:
```bash
cd Project_ATM
```

3. Run the application:
```bash
python3 main.py
```

## 🔐 Login Credentials

### Admin Access
- **Admin ID:** `admin`
- **Admin Password:** `Admin@123`

### Bank Access
- **State Bank (BNK001)** - Navrangpura Branch
  - Password: `Sbi@123`

- **HDFC Bank (BNK002)** - Satellite Branch
  - Password: `Hdfc@123`

### Pre-registered Users

| User ID | Name | Card Number | PIN | Balance | Bank |
|---------|------|-------------|-----|---------|------|
| USR001 | Het | 2145156787311234 | 1234 | ₹15,000 | State Bank |
| USR002 | Raj | 6145156257313234 | 5678 | ₹8,000 | State Bank |
| USR003 | Amit | 2149156787371630 | 1111 | ₹20,000 | HDFC Bank |
| USR004 | Neha | 9142159784317264 | 2222 | ₹12,000 | HDFC Bank |

**⚠️ Important:** On first login, users are required to change their PIN for security purposes.

## How to Use

### 1. User - ATM Operations

Select **Option 1** from the main menu:

1. **Select ATM Branch** - Choose an available ATM location
2. **Enter Card Number** - 16-digit card number
3. **Enter PIN** - 4-digit PIN (initial or changed PIN)
4. **Mandatory PIN Change (First Login)** - Change your PIN for security
5. **Select Transaction:**
   - **Deposit** - Deposit money (minimum ₹100, must be multiple of 100)
   - **Withdraw** - Withdraw money (daily limit: ₹50,000, per transaction: ₹20,000)
   - **Change PIN** - Update your PIN (requires PIN validation)
   - **Check Balance** - View current balance (requires PIN validation)
   - **Back to Main Menu** - Return to main menu

### 2. Admin - System Management

Select **Option 2** from the main menu:

1. **Enter Admin ID:** `admin`
2. **Enter Admin Password:** `Admin@123`
3. **Available Options:**
   - View all users and their details
   - View all banks and branches
   - View all ATMs and availability
   - Access reports and statistics

### 3. Bank - Account Management

Select **Option 3** from the main menu:

1. **Select a Bank** - Choose from available banks
2. **Enter Bank Password** - Use credentials provided above
3. **Available Options:**
   - **Create New User Account** - Add new customer with validation
   - **Create New ATM** - Set up ATM at new location
   - **View Users** - List all users in the bank
   - **View ATMs** - List all ATMs in the bank

## Transaction Limits

### Daily Limits (Per User)
- **Maximum Daily Withdrawal:** ₹50,000
- **Maximum Daily Deposit:** ₹100,000
- **Maximum Transactions Per Day:** 4

### Per Transaction Limits
- **Minimum Withdrawal:** ₹100
- **Maximum Withdrawal (Own Bank):** ₹20,000
- **Maximum Withdrawal (Cross Bank):** ₹10,000
- **Minimum Deposit:** ₹100
- **Maximum Deposit:** ₹50,000

### Transaction Fees
- **Own Bank Transactions:** No fee
- **Cross Bank Transactions:** 2.5% fee

## Data Validation Requirements

### User Information
- **Name:** 3-60 characters, letters and spaces only
- **Date of Birth (DOB):** DD/MM/YYYY format, user must be 16+ years old
- **Phone:** Exactly 10 digits
- **Aadhar:** 12 digits, cannot start with 01 or 10, must be unique per bank
- **PAN:** 10 characters (format: ABCDE1234A), must be unique per bank
- **Initial Balance:** ₹1,000 - ₹50,000

### PIN Requirements
- **Format:** Exactly 4 digits
- **Cannot be same** as previous PIN
- **First-time change** is mandatory on first login
- **Per-transaction validation** required for all ATM operations

## Security Features

### 1. PIN Validation System
- Every transaction requires PIN entry and validation
- 3 attempt limit per transaction
- Incorrect attempts lock the transaction
- User returned to ATM menu after failed attempts

### 2. First-Time PIN Change
- New users must change default PIN on first login
- Prevents unauthorized access with system-generated PIN
- `pin_changed` flag tracks PIN change status

### 3. Account Protection
- Daily withdrawal and deposit limits
- Transaction count limits per day
- Cross-bank transaction restrictions
- Unique Aadhar and PAN per bank

### 4. Data Security
- PIN stored as integer for basic security
- Password hashing using SHA256 for admin/bank credentials
- In-memory data storage (can be extended to database)

## Error Handling

The system includes comprehensive error handling for:
- Invalid card numbers (format and length validation)
- Incorrect PINs (3 attempt limit per transaction)
- Insufficient balance
- Daily limit violations
- Invalid amount entry
- Duplicate Aadhar/PAN registrations per bank
- Cross-bank transaction restrictions
- Invalid bank selection
- User input validation across all operations

## Troubleshooting

### "Card Not Found"
- Verify the 16-digit card number is correct
- Check if the user exists in the system
- Contact bank to verify card number

### "Incorrect PIN"
- You have 3 attempts per transaction
- If all attempts fail, you're returned to ATM menu
- Contact bank to reset PIN if forgotten

### "Daily Limit Exceeded"
- Check remaining daily limit (shown after each transaction)
- Try again the next day or reduce transaction amount
- Different limits for withdrawal and deposit

### "Insufficient Balance"
- Check current balance (select "Check Balance")
- Deposit money first if needed
- Check available ATM balance for withdrawals

### "Aadhar Card Already Exists"
- Aadhar card is unique per bank
- Cannot register same Aadhar in same bank
- Use different Aadhar for new registration

## Transaction Rules

- **Deposit**: Minimum ₹100, multiples of ₹100, same-bank only
- **Withdrawal**: Minimum ₹100, multiples of ₹100, daily limits apply
- **Cross-bank**: 2.5% fee, maximum ₹10,000 per transaction
- **Daily Limits**: ₹50,000 withdrawal, ₹100,000 deposit, 4 transactions per day
- **PIN Attempts**: Maximum 3 attempts per transaction

## Development

### Code Style
- Follows Python PEP 8 conventions
- Comprehensive error handling
- Modular design with separation of concerns
- Centralized constants for easy maintenance
- Object-oriented design with clear responsibilities

### Testing
- Input validation across all user interactions
- Transaction limit enforcement
- Cross-bank transaction fee calculations
- PIN validation and attempt tracking

## License

This project is open-source and available for educational and development purposes.

## Author

**Het Govani**

Developed as a Python programming project demonstrating object-oriented design and banking system concepts.

## Acknowledgments

- Built with Python standard library
- Inspired by real-world ATM and banking systems
- Educational project for learning Python development
- Enhanced with comprehensive security features and transaction validation

---

**Last Updated:** March 27, 2026
**Version:** 1.0