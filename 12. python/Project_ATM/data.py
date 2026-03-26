banks = {
    "BNK001": {
        "name": "State Bank",
        "branch": "Navrangpura",
        "vault": 50000000
    },
    "BNK002": {
        "name": "National Bank",
        "branch": "Satellite",
        "vault": 50000000
    }
}

users = {
    "USR001": {
        "name": "Het",
        "dob": "15/06/2001",
        "phone": "9876543210",
        "aadhar": "123456789012",
        "pan": "ABCDE1234A",
        "balance": 15000,
        "card_no": 2145156787311234,
        "pin": 1234,
        "bank_id": "BNK001",
        "daily_withdrawn": 0,
        "daily_withdrawal_count": 0,
        "daily_deposited": 0,
        "daily_deposit_count": 0,
        "login_attempt": 0
    },
    "USR002": {
        "name": "Raj",
        "dob": "20/03/2002",
        "phone": "9876543211",
        "aadhar": "123456789013",
        "pan": "BCDEF2345B",
        "balance": 8000,
        "card_no": 6145156257313234,
        "pin": 5678,
        "bank_id": "BNK001",
        "daily_withdrawn": 0,
        "daily_withdrawal_count": 0,
        "daily_deposited": 0,
        "daily_deposit_count": 0,
        "login_attempt": 0
    },
    "USR003": {
        "name": "Amit",
        "dob": "10/08/2000",
        "phone": "9876543212",
        "aadhar": "123456789014",
        "pan": "CDEFG3456C",
        "balance": 20000,
        "card_no": 2149156787371630,
        "pin": 1111,
        "bank_id": "BNK002",
        "daily_withdrawn": 0,
        "daily_withdrawal_count": 0,
        "daily_deposited": 0,
        "daily_deposit_count": 0,
        "login_attempt": 0
    },
    "USR004": {
        "name": "Neha",
        "dob": "05/12/1999",
        "phone": "9876543213",
        "aadhar": "123456789015",
        "pan": "DEFGH4567D",
        "balance": 12000,
        "card_no": 9142159784317264,
        "pin": 2222,
        "bank_id": "BNK002",
        "daily_withdrawn": 0,
        "daily_withdrawal_count": 0,
        "daily_deposited": 0,
        "daily_deposit_count": 0,
        "login_attempt": 0
    }
}


atms = {
    "ATM001": {
        "bank_id": "BNK001",
        "location": "Navrangpura",
        "available_atm_balance": 500000
    },
    "ATM002": {
        "bank_id": "BNK002",
        "location": "Satellite",
        "available_atm_balance": 300000
    },
    "ATM003": {
        "bank_id": "BNK001",
        "location": "Vasna",
        "available_atm_balance": 900000
    }
}