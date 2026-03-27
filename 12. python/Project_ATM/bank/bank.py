from data import banks, users, atms
import constant
from datetime import datetime
import random
import re
import hashlib

class Bank:
    """Bank class for managing bank operations like creating users and ATMs."""

    def __init__(self):
        """Initializes the Bank class.
        
        Takes no arguments.
        
        Returns nothing.
        """
        self.selected_bank_id = None

    def _display_banks(self):
        """Displays all banks.
        
        Takes no arguments.
        
        Returns True if banks exist, False otherwise.
        """
        if not banks:
            print(constant.BANK_NOT_FOUND)
            return False
        
        print(constant.AVAILABLE_BANK)
        for bank_data in banks.values():
            print(f"  {bank_data.get('name')} - {bank_data.get('branch')}")
        print()
        return True

    def _select_bank(self):
        """Selects a bank for operations.
        
        Takes no arguments.
        
        Returns True if selected, False otherwise.
        """
        while True:
            if not self._display_banks():
                return False
            
            bank_name = input(constant.BANK_CHOICE_INPUT).strip()
            bank_id = self._fetch_bank(bank_name)
            if not bank_id:
                print(constant.BANK_NOT_FOUND)
                continue

            # Now ask for password up to 3 attempts
            for attempt in range(3):
                password = input(constant.BANK_PASSWORD_INPUT).strip()
                hashed_input = hashlib.sha256(password.encode()).hexdigest()
                if hashed_input == banks[bank_id].get('password'):
                    self.selected_bank_id = bank_id
                    print(f'\nSelected bank: {banks[bank_id]["name"]} - {banks[bank_id]["branch"]}')
                    return True
                else:
                    remaining_attempts = 3 - attempt - 1
                    if remaining_attempts > 0:
                        print(constant.BANK_PASSWORD_ERROR)
                    else:
                        print("\nMaximum password attempts exceeded.")
                        break

    def _display_atms(self):
        """Displays all available ATMs for the selected bank.
        
        Takes no arguments.
        
        Returns True if ATMs exist, False otherwise.
        """
        bank_atms = [atm_data for atm_data in atms.values() if atm_data.get('bank_id') == self.selected_bank_id]
        
        if not bank_atms:
            print(constant.ATM_NOT_FOUND)
            return False
        
        print(f"\nAvailable ATMs for {banks[self.selected_bank_id]['name']} - {banks[self.selected_bank_id]['branch']}:" )
        for atm_data in bank_atms:
            print(f"  {atm_data.get('location')} (Bank: {banks[self.selected_bank_id]['name']})")
        print()
        return True

    def _fetch_bank(self, bank_name):
        """Gets bank ID by bank name.
        
        Takes bank_name (string).
        
        Returns bank_id string or None.
        """
        for bank_id, bank_data in banks.items():
            if bank_data.get('name').lower() == bank_name.lower():
                return bank_id
        return

    def _fetch_atm_by_branch(self, branch_name):
        """Gets ATM ID by branch name for the selected bank.
        
        Takes branch_name (string).
        
        Returns atm_id string or None.
        """
        for atm_id, atm_data in atms.items():
            if (atm_data.get('location').lower() == branch_name.lower() and 
                atm_data.get('bank_id') == self.selected_bank_id):
                return atm_id
        return
        
    def _create_new_user_id(self):
        """Creates a new user ID.
        
        Takes no arguments.
        
        Returns a unique user ID string.
        """
        existing_ids = [int(uid.replace('USR', '')) for uid in users.keys() if uid.startswith('USR')]
        return f"USR{str(max(existing_ids, default=0) + 1).zfill(3)}"

    def _create_new_atm_id(self):
        """Creates a new ATM ID.
        
        Takes no arguments.
        
        Returns a unique ATM ID string.
        """
        existing_ids = [int(atm_id.replace('ATM', '')) for atm_id in atms.keys() if atm_id.startswith('ATM')]
        return f"ATM{str(max(existing_ids, default=0) + 1).zfill(3)}"

    def _create_pin(self):
        """Creates a 4-digit random card PIN number.
        
        Takes no arguments.
        
        Returns a 4-digit string PIN.
        """
        return str(random.randint(1000, 9999))

    def _create_card_number(self):
        """Creates a 16-digit random card number.
        
        Takes no arguments.
        
        Returns a 16-digit string card number.
        """
        return str(random.randint(1000000000000000, 9999999999999999))

    def _validate_phone_number(self, phone):
        """Validates the phone number.
        
        Takes phone (string).
        
        Returns True if valid, False otherwise.
        """

        if not phone.isdigit() or len(phone) != 10:
            print(constant.PHONE_NUMBER_ERROR)
            return False
        
        if not phone.startswith(('6', '7', '8', '9')):
            print(constant.PHONE_NUMBER_START_WITH_ERROR)
            return False
        
        return True

    def _validate_dob(self,dob_str):
        """Validates the date of birth.
        
        Takes dob_str (string in DD/MM/YYYY format).
        
        Returns datetime object if valid, None otherwise.
        """
        try:
            dob = datetime.strptime(dob_str, '%d/%m/%Y')
            today = datetime.now()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            
            if age < 16:
                print(constant.AGE_ERROR)
                return 
            if age > 120:
                print(constant.OVER_AGE_ERROR)
                return 
            
            return dob
        except ValueError:
            print(constant.DOB_FORMAT_ERROR)
            return 

    def _validate_aadhar(self, aadhar, bank_id):
        """Validates the Aadhar card.
        
        Takes aadhar (string), bank_id (string).
        
        Returns True if valid, False otherwise.
        """
        if not aadhar.isdigit() or len(aadhar) != 12:
            print(constant.AADHAR_CARD_ERROR)
            return False
        
        if aadhar.startswith(('01', '10')):
            print(constant.AADHAR_CARD_START_WITH_ERROR)
            return False
        
        for user_data in users.values():
            if user_data.get('bank_id') == bank_id and user_data.get('aadhar') == aadhar:
                print(constant.AADHAR_CARD_ALREADY_EXISTS)
                return False
        
        return True

    def _validate_pan(self, pan, bank_id):
        """Validates the PAN card format.
        
        Takes pan (string), bank_id (string).
        
        Returns True if valid, False otherwise.
        """
        pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
        
        if not re.match(pan_pattern, pan):
            print(constant.PAN_FORMAT_ERROR)
            return False
        
        for user_data in users.values():
            if user_data.get('bank_id') == bank_id and user_data.get('pan') == pan:
                print(constant.PAN_ALREADY_EXISTS_ERROR)
                return False
        
        return True

    def _create_user(self):
        """Creates a user and validates user details.
        
        Takes no arguments.
        
        Returns nothing.
        """
        print()
        
        while True:
            name = input(constant.USER_NAME_INPUT).strip()
            if not name:
                print(constant.NAME_BLANK_ERROR)
                continue
            
            if len(name) < 3 or len(name) > 60:
                print(constant.NAME_LENGTH_ERROR)
                continue

            if not name.replace(' ', '').isalpha():
                print(constant.NAME_FORMAT_ERROR)
                continue
            break

        bank_id = self.selected_bank_id


        while True:
            dob_str = input(constant.ATM_DOB_INPUT).strip()
            dob = self._validate_dob(dob_str)
            if dob:
                break

        while True:
            phone = input(constant.ATM_PHONE_INPUT).strip()
            if self._validate_phone_number(phone):
                break

        while True:
            aadhar = input(constant.ATM_AADHAR_INPUT).strip()
            if self._validate_aadhar(aadhar, bank_id):
                break


        while True:
            pan = input(constant.ATM_PAN_INPUT).strip()
            if self._validate_pan(pan, bank_id):
                break

        while True:
            initial_balance = input(constant.ATM_BALANCE_INPUT).strip()
            if not initial_balance.isdigit():
                print(constant.INVALID_INPUT)
                continue
            
            initial_balance = float(initial_balance)
            if initial_balance < 1000:
                print(constant.INITIAL_BALANCE_MIN_ERROR)
                continue
            if initial_balance > 50000:
                print(constant.INITIAL_BALANCE_MAX_ERROR)
                continue
            break

        pin = self._create_pin()
        card_no = self._create_card_number()

        user_id = self._create_new_user_id()

        users[user_id] = {
            'name': name,
            'dob': dob_str,
            'phone': phone,
            'aadhar': aadhar,
            'pan': pan,
            'balance': initial_balance,
            'card_no': int(card_no),
            'pin': int(pin),
            'bank_id': bank_id,
            'daily_withdrawn': 0,
            'daily_withdrawal_count': 0,
            'daily_deposited': 0,
            'daily_deposit_count': 0,
            'login_attempt': 0,
            'pin_changed': False
        }

        bank_name = banks.get(bank_id, {}).get('name', bank_id)
        print(constant.MSG_USER_ADDED.format(name, card_no, pin, bank_name, initial_balance))

    def create_atm(self):
        """Creates a new ATM for the selected bank.
        
        Takes no arguments.
        
        Returns nothing.
        """
        print()

        bank_id = self.selected_bank_id

        while True:
            location = input(constant.ATM_ATM_ID_INPUT).strip()
            if not location:
                print(constant.ATM_BRANCH_NAME_ERROR)
                continue
            
           
            atm_exists = False
            for existing_atm_data in atms.values():
                if existing_atm_data.get('location').lower() == location.lower() and existing_atm_data.get('bank_id') == bank_id:
                    print(constant.ATM_ALREADY_EXISTS_ERROR)
                    atm_exists = True
                    break
            
            if atm_exists:
                continue
            break

        atm_id = self._create_new_atm_id()

        while True:
            atm_balance = input(constant.ATM_FUND_AMOUNT_INPUT).strip()
            if not atm_balance.isdigit():
                print(constant.ATM_FUND_AMOUNT_ERROR)
                continue
            available_atm_balance = float(atm_balance)
            if available_atm_balance < 100000 and available_atm_balance < banks[bank_id]['vault']:
                print(constant.ATM_MINIMUM_FUNDING_ERROR)
                continue
            break

        atms[atm_id] = {
            'bank_id': bank_id,
            'location': location,
            'available_atm_balance': available_atm_balance
        }

        bank_name = banks.get(bank_id, {}).get('name', bank_id)
        print(constant.MSG_ATM_ADDED.format(atm_id, bank_name, available_atm_balance))

    def show_users(self):
        """Displays users for the selected bank.
        
        Takes no arguments.
        
        Returns nothing.
        """
        print()
        bank_users = {uid: user_data for uid, user_data in users.items() if user_data.get('bank_id') == self.selected_bank_id}
        
        if not bank_users:
            print(constant.USER_NOT_FOUND)
            return

        print(f"Users for {banks[self.selected_bank_id]['name']} - {banks[self.selected_bank_id]['branch']}:")
        for uid, user_data in bank_users.items():
            bank_name = banks.get(user_data.get('bank_id'), {}).get('name', user_data.get('bank_id'))
            print(f"{uid}: {user_data.get('name')} | Balance: INR{user_data.get('balance')} | Bank: {bank_name}")

    def _show_atm(self):
        """Displays ATMs for the selected bank.
        
        Takes no arguments.
        
        Returns nothing.
        """
        print()
        bank_atms = {atm_id: atm_data for atm_id, atm_data in atms.items() if atm_data.get('bank_id') == self.selected_bank_id}
        
        if not bank_atms:
            print(constant.ATM_NOT_FOUND)
            return

        print(f"ATMs for {banks[self.selected_bank_id]['name']} - {banks[self.selected_bank_id]['branch']}:")
        for atm_id, atm_data in bank_atms.items():
            print(f" {atm_id}: {atm_data.get('location')} | Cash: INR{atm_data.get('available_atm_balance'):.2f}")

    def deposit_to_atm(self):
        """Deposits money to an ATM for the selected bank.
        
        Takes no arguments.
        
        Returns nothing.
        """
        print()
        
        if not self._display_atms():
            return
            
        while True:
            branch_name = input(constant.ATM_ATM_ID_INPUT).strip()
            atm_id = self._fetch_atm_by_branch(branch_name)
            if atm_id:
                break
            print(constant.INVALID_BRANCH_NAME)

        atm_data = atms.get(atm_id)

        while True:
            amount_str = input(constant.ATM_FUND_AMOUNT_INPUT).strip()
            if not amount_str.isdigit():
                print(constant.ATM_FUND_AMOUNT_ERROR)
                continue

            amount = float(amount_str)
            if amount <= 0:
                print(constant.AMOUNT_MUST_GREATER_THAN_ZERO)
                continue
            
            # Check if bank vault has sufficient funds
            bank_id = self.selected_bank_id
            if amount > banks[bank_id]['vault']:
                print(f'\nInsufficient bank vault balance. Available: INR{banks[bank_id]["vault"]:,.2f}')
                continue
            break

        atm_data['available_atm_balance'] += amount
        bank_id = self.selected_bank_id
        banks[bank_id]['vault'] -= amount
        
        print(constant.MSG_ATM_FUNDED.format(atm_data['available_atm_balance']))
        print(f"Bank vault updated. New vault balance: INR{banks[bank_id]['vault']:,.2f}")

    def bank_menu(self):
        """Displays and handles the bank menu for operations.
        
        Takes no arguments.
        
        Returns nothing.
        """
        # First select a bank
        if not self._select_bank():
            return
        
        # Then show operations menu for the selected bank
        while True:
            print(f'\nBank Functions for {banks[self.selected_bank_id]["name"]} - {banks[self.selected_bank_id]["branch"]}')
            print('1. Create user')
            print('2. Create ATM')
            print('3. Show users')
            print('4. Show ATMs')
            print('5. Deposit money to ATM')
            print('6. Change bank')
            print('7. Back to main menu')
            print()

            choice = input(constant.ATM_CHOICE_INPUT).strip()
            if not choice.isdigit():
                print(constant.INVALID_MENU_CHOICE)
                continue

            choice_num = int(choice)
            if choice_num == 1:
                self._create_user()
            elif choice_num == 2:
                self.create_atm()
            elif choice_num == 3:
                self.show_users()
            elif choice_num == 4:
                self._show_atm()
            elif choice_num == 5:
                self.deposit_to_atm()
            elif choice_num == 6:

                if not self._select_bank():
                    return
                continue
            elif choice_num == 7:
                print('\nReturning to main menu...')
                break
            else:
                print('\nInvalid choice. Please select from 1 to 7.')

