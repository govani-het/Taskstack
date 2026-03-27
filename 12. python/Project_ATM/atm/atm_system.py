from bank.bank import Bank
from admin.admin import Admin
from data import banks, users, atms
import constant
import hashlib

class ATMSystem:
    def __init__(self):
        """Initializes the ATM system.
        
        Takes no arguments.
        
        Returns nothing.
        """
        self.is_running = True

    def _find_user_by_card(self, card_no):
        """Finds and returns user record matching the given card number.
        
        Takes card_no (string or int): the card number to search for.
        
        Returns a dictionary copy of the user data with user_id added, or None if not found.
        """  
        for user_id, user_data in users.items():
            if str(user_data.get('card_no')) == str(card_no):
                user_data_copy = user_data.copy()
                user_data_copy['user_id'] = user_id
                return user_data_copy
        return

    def _validate_pin_for_transaction(self, user_id):
        """Validates the user's PIN for a transaction with up to 3 attempts.
        
        Takes user_id (string).
        
        Returns True if PIN is correct, False if attempts exhausted.
        """
        user = users.get(user_id)
        if not user:
            print(constant.USER_NOT_FOUND)
            return False

        for attempt in range(3):
            pin = input(constant.ATM_PIN_INPUT).strip()
            remaining_attempts = 2 - attempt
            
            # Check format
            if not pin.isdigit() or len(pin) != 4:
                print(constant.PIN_FORMAT_ERROR)
                if remaining_attempts > 0:
                    print(f"Remaining attempts: {remaining_attempts}")
                else:
                    print(constant.MAX_PIN_ATTEMPTS_EXCEEDED)
                    print("Returning to ATM menu.")
                    return False
                continue

            # Check if PIN is correct
            if str(user.get('pin')) == str(pin):
                return True
            else:
                if remaining_attempts > 0:
                    print(f"\nIncorrect PIN. {remaining_attempts} attempt(s) remaining.")
                else:
                    print(constant.MAX_PIN_ATTEMPTS_EXCEEDED)
                    print("Returning to ATM menu.")
                    return False
        return False

    def _authenticate_user(self):
        """Authenticates a user by card number and PIN with per-user attempt tracking.
        
        Takes no arguments.
        
        Returns a tuple of (user_id, user_data) if authenticated, or None if failed.
        """
        card_no = input(constant.ATM_CARD_INPUT).strip()

        if not card_no.isdigit():
            print(constant.CARD_NUMBER_DIGIT_ERROR)
            return

        if len(card_no) != 16:
            print(constant.CARD_NUMBER_LENGTH_ERROR)
            return

        user = self._find_user_by_card(card_no)
        if not user:
            print(constant.CARD_NOT_FOUND)
            return

        # Now ask for PIN up to 3 attempts
        for attempt in range(constant.MAX_PIN_ATTEMPTS):
            pin = input(constant.ATM_PIN_INPUT).strip()

            if not pin.isdigit() or len(pin) != 4:
                print(constant.PIN_FORMAT_ERROR)
                continue

            if str(user.get('pin')) == str(pin):
                user_id = user['user_id']
                bank_id = user['bank_id']
                user['login_attempt'] = 0  
                bank_name = banks.get(bank_id, {}).get('name', 'Bank')
                print(constant.AUTH_SUCCESS.format(user.get('name'), bank_name))
                return user_id, user
            else:
                remaining_attempts = constant.MAX_PIN_ATTEMPTS - attempt - 1
                if remaining_attempts > 0:
                    print(f"\nIncorrect PIN. {remaining_attempts} attempt(s) remaining.")
                else:
                    print(constant.MAX_PIN_ATTEMPTS_EXCEEDED)
                    print(constant.RETURN_TO_ATM_MENU)
                    return

    def _fetch_atm_by_branch(self, branch_name):
        """Gets ATM data by branch name.
        
        Takes branch_name (string): the branch name to search for.
        
        Returns a tuple of (atm_data, atm_id) if found, or None if not found.
        """
        for atm_id, atm_data in atms.items():
            if atm_data.get('location').lower() == branch_name.lower():
                return atm_data, atm_id
        return

    def _select_atm(self):
        """Allows the user to select an ATM from available options.
        
        Takes no arguments.
        
        Returns nothing.
        """
        if not atms:
            print(constant.ATM_NOT_FOUND)
            return

        while True:
            print(constant.AVAILABLE_ATM)
            print()
            for atm_id, atm_data in atms.items():
                bank_name = banks.get(atm_data.get('bank_id'), {}).get('name', 'Unknown')
                print(f"Branch: {atm_data.get('location')} (Bank: {bank_name})")
            print()
            branch_choice = input(constant.ATM_SELECT_ATM_INPUT).strip()
            atm_data, atm_id = self._fetch_atm_by_branch(branch_choice)

            if atm_data:
                bank_name = banks.get(atm_data.get('bank_id'), {}).get('name', 'Bank')
                print(f"\nSelected ATM: {branch_choice} - {atm_data.get('location')} (Bank: {bank_name})")
                print()
                self._atm_action_menu(atm_id)
                break
            else:
                print(constant.INVALID_BRANCH_SELECTION)

    def _atm_action_menu(self, atm_id):
        """Displays the ATM action menu and handles user operations like deposit, withdraw, and PIN change.
        
        Takes atm_id (string): the ID of the selected ATM.
        
        Returns nothing.
        """
        atm = atms.get(atm_id)

        # Authenticate user first
        auth_result = self._authenticate_user()
        if not auth_result:
            print(constant.TRY_AGAIN)
            return
        
        user_id, user = auth_result

        # Check if PIN needs to be changed (first login)
        if not user.get('pin_changed', False):
            print("\nFor security reasons, you must change your PIN on first login.")
            while True:
                new_pin = input(constant.ATM_NEW_PIN_INPUT).strip()
                if self._change_pin(user_id, new_pin):
                    break
            # After changing PIN, pin_changed is set to True

        while True:

            user = users.get(user_id)  # Refresh user data

            print("1. Deposit")
            print("2. Withdraw")
            print("3. Change PIN")
            print("4. Check Balance")
            print("5. Back to Main Menu")
            print()

            choice = input(constant.ATM_CHOICE_INPUT).strip()
            if choice not in ["1", "2", "3", "4", "5"]:
                print(constant.INVALID_CHOICE_SELECTED)
                continue

            if choice == "5":
                print(constant.RETURN_TO_MAIN_MENU)
                break

            # User is already authenticated, no need to authenticate again
            user = users.get(user_id)  # Refresh user data in case PIN was changed

            if choice == "1":
                if not self._validate_pin_for_transaction(user_id):
                    continue
                while True:
                    amount_str = input(constant.ATM_AMOUNT_INPUT).strip()
                    try:
                        amount = float(amount_str)
                    except ValueError:
                        print(constant.MSG_INVALID_AMOUNT)
                        continue
                    if amount <= 0:
                        print(constant.AMOUNT_MUST_GREATER_THAN_ZERO)
                        continue
                    if user.get('bank_id') != atm.get('bank_id'):
                        print(constant.CROSS_BANK_DEPOSIT_ERROR)
                        break
                    if amount < 100:
                        print(constant.MINIMUM_DEPOSIT_ERROR)
                        continue
                    if amount % 100 != 0:
                        print(constant.DEPOSIT_AMOUNT_ERROR)
                        continue
                    if amount > constant.MAX_DEPOSIT_PER_TXN:
                        print(f"\nAmount exceeds per-transaction limit of ₹{constant.MAX_DEPOSIT_PER_TXN}.")
                        continue
                    daily_deposited = user.get('daily_deposited', 0)
                    if daily_deposited + amount > constant.MAX_DAILY_DEPOSIT_AMOUNT:
                        print(constant.DAILY_DEPOSIT_LIMIT_ERROR)
                        continue
                    self._deposit_money(user_id, atm_id, amount)
                    break

            elif choice == "2":
                if not self._validate_pin_for_transaction(user_id):
                    continue
                while True:
                    amount_str = input(constant.ATM_AMOUNT_INPUT).strip()
                    try:
                        amount = float(amount_str)
                    except ValueError:
                        print(constant.MSG_INVALID_AMOUNT)
                        continue
                    if amount <= 0:
                        print(constant.AMOUNT_MUST_GREATER_THAN_ZERO)
                        continue
                    if amount < 100:
                        print(constant.MINIMUM_WITHDRAW_ERROR)
                        continue
                    if amount % 100 != 0:
                        print(constant.MULTIPLE_OF_100_ERROR)
                        continue
                    if amount > user.get('balance'):
                        print(constant.MSG_INSUFFICIENT_BALANCE)
                        continue
                    if amount > atm.get('available_atm_balance'):
                        print(constant.MSG_INSUFFICIENT_ATM_BALANCE)
                        continue
                    daily_amount = user.get('daily_withdrawn', 0)
                    daily_count = user.get('daily_withdrawal_count', 0)
                    if daily_count >= constant.MAX_DAILY_TXN_COUNT:
                        print(constant.MSG_DAILY_COUNT_LIMIT.format(constant.MAX_DAILY_TXN_COUNT))
                        continue
                    if daily_amount + amount > constant.MAX_DAILY_TXN_AMOUNT:
                        print(constant.MSG_DAILY_AMOUNT_LIMIT.format(constant.MAX_DAILY_TXN_AMOUNT))
                        continue
                    user_bank = user.get('bank_id')
                    atm_bank = atm.get('bank_id')
                    if user_bank != atm_bank:
                        if amount > constant.CROSS_BANK_WITHDRAWAL_LIMIT:
                            print(constant.CROSS_BANK_WITHDRAWAL_LIMIT_ERROR)
                            continue
                    else:
                        if amount > constant.MAX_WITHDRAWAL_PER_TXN:
                            print(constant.MSG_SINGLE_LIMIT.format(constant.MAX_WITHDRAWAL_PER_TXN))
                            continue
                    self._withdraw_money(user_id, amount, atm_id)
                    break

            elif choice == "3":
                if not self._validate_pin_for_transaction(user_id):
                    continue
                while True:
                    new_pin = input(constant.ATM_NEW_PIN_INPUT).strip()
                    if self._change_pin(user_id, new_pin):
                        break

            elif choice == "4":
                if not self._validate_pin_for_transaction(user_id):
                    continue
                self._check_balance(user_id)

            print(constant.BACK_TO_MAIN_MENU)

    def _withdraw_money(self, user_id, amount, atm_id):
        """Processes a withdrawal transaction, checking limits, fees, and updating balances.
        
        Takes user_id (string), amount (float), atm_id (string).
        
        Returns nothing.
        """
        user = users.get(user_id)
        atm = atms.get(atm_id)

        if not user:
            print(constant.USER_NOT_FOUND)
            return
        if not atm:
            print(constant.ATM_NOT_FOUND)
            return

        daily_amount = user.get('daily_withdrawn', 0)
        daily_count = user.get('daily_withdrawal_count', 0)

        user_bank = user.get('bank_id')
        atm_bank = atm.get('bank_id')
        fee_percent = 0 if user_bank == atm_bank else constant.CROSS_BANK_FEE_PERCENT
        fee = (fee_percent / 100.0) * amount
        total_deduct = amount + fee

        if total_deduct > user.get('balance', 0):
            print("\n" + constant.MSG_INSUFFICIENT_BALANCE)
            return

        user['balance'] -= total_deduct
        atm['available_atm_balance'] -= amount


        user_bank_id = user.get('bank_id')
        atm_bank_id = atm.get('bank_id')
        
        if user_bank_id != atm_bank_id:
            banks[atm_bank_id]['vault'] += fee

        user['daily_withdrawn'] = daily_amount + amount
        user['daily_withdrawal_count'] = daily_count + 1

        if fee > 0:
            print("\n" + constant.MSG_CROSS_BANK_CHARGE.format(fee_percent, fee))

        print("\n" + constant.MSG_TOTAL_DEDUCTED.format(total_deduct))
        print(constant.MSG_WITHDRAW_SUCCESS.format(amount, user['balance']))
        print(constant.MSG_REMAINING_LIMIT.format(
            constant.MAX_DAILY_TXN_AMOUNT - user['daily_withdrawn'],
            constant.MAX_DAILY_TXN_COUNT - user['daily_withdrawal_count']
        ))

    def _deposit_money(self, user_id, atm_id, amount):
        """Deposits money into the user's account and updates ATM balance.
        
        Takes user_id (string), atm_id (string), amount (float).
        
        Returns nothing.
        """
        user = users.get(user_id)
        atm = atms.get(atm_id)

        if not user:
            print(constant.USER_NOT_FOUND)
            return
        if not atm:
            print(constant.ATM_NOT_FOUND)
            return

        daily_deposited = user.get('daily_deposited', 0)

        user['balance'] += amount
        atm['available_atm_balance'] = atm.get('available_atm_balance', 0) + amount
        
        # Deduct from bank vault
        bank_id = user.get('bank_id')
        banks[bank_id]['vault'] -= amount
        
        user['daily_deposited'] = daily_deposited + amount
        user['daily_deposit_count'] = user.get('daily_deposit_count', 0) + 1
        
        print("\n" + constant.MSG_DEPOSIT_SUCCESS.format(amount, user['balance']))
        print(f" Daily deposited: INR {user['daily_deposited']}")

    def _change_pin(self, user_id, new_pin):
        """Changes the user's PIN.
        
        Takes user_id (string), new_pin (string).
        
        Returns True if successful, False otherwise.
        """
        user = users.get(user_id)
        if not user:
            print(constant.USER_NOT_FOUND)
            return False

        if not new_pin.isdigit() or len(new_pin) != 4:
            print(constant.PIN_FORMAT_ERROR)
            return False

        if str(user['pin']) == str(new_pin):
            print(constant.PIN_CHANGE_SAME_ERROR)
            return False

        user['pin'] = int(new_pin)
        user['pin_changed'] = True
        print(constant.PIN_CHANGE_SUCCESS)
        return True

    def _check_balance(self, user_id):
        """Displays the user's current balance.
        
        Takes user_id (string).
        
        Returns nothing.
        """
        user = users.get(user_id)
        if not user:
            print("\n" + constant.USER_NOT_FOUND)
            return

        print(f"\nCurrent balance: INR {user['balance']:.2f}")

    def _admin_login(self):
        """Authenticates admin by ID and password.
        
        Takes no arguments.
        
        Returns True if authenticated, False otherwise.
        """
        print("\n-- Admin Login --")

        admin_id = input("  Enter admin ID: ").strip()
        if admin_id != constant.ADMIN_ID:
            print("\nInvalid admin ID. Please try again.")
            return False

        # Now ask for password up to 3 attempts
        for attempt in range(3):
            password = input("  Enter admin password: ").strip()
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if password_hash == constant.ADMIN_PASSWORD_HASH:
                print("\nAdmin authenticated successfully.")
                return True
            else:
                remaining_attempts = 3 - attempt - 1
                if remaining_attempts > 0:
                    print("\nInvalid password. Please try again.")
                else:
                    print("\nMaximum password attempts exceeded.")
                    return False


    def _exit(self):
        """Exits the ATM system.
        
        Takes no arguments.
        
        Returns nothing.
        """
        print(constant.THANK_YOU_ATM)
        print(f"\n  Developed by {constant.DEVELOPER_NAME}")
        self.is_running = False

    def run(self):
        """Runs the main ATM system loop, displaying the menu and handling user choices.
        
        Takes no arguments.
        
        Returns nothing.
        """
        while self.is_running:

            print("1. User")
            print("2. Admin")
            print("3. Bank")
            print("4. Exit")
            print()

            try:
                choice = int(input("Enter your choice: "))
                if choice not in [1, 2, 3, 4]:
                    print(constant.INVALID_MAIN_CHOICE)
                    continue
            except ValueError:
                print(constant.INVALID_MAIN_INPUT)
                continue

            if choice == 1:
                self._select_atm()
            elif choice == 2:
                if self._admin_login():
                    admin = Admin()
                    admin.admin_menu()
            elif choice == 3:
                bank = Bank()
                bank.bank_menu()
            elif choice == 4:
                self._exit()

