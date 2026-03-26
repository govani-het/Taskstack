from bank.bank import Bank
from data import banks, users, atms
import constant

class ATMSystem:
    def __init__(self):
        """Initialize the ATM system."""
        self.is_running = True


    def _find_user_by_card(self, card_no):
        """Return user record matching card_no."""  
        for user_id, user_data in users.items():
            if str(user_data.get('card_no')) == str(card_no):
                user_data_copy = user_data.copy()
                user_data_copy['user_id'] = user_id
                return user_data_copy
        return

    def _authenticate_user(self):
        """Authenticate a user by card number and PIN with per-user attempt tracking."""
        while True:
            card_no = input(constant.ATM_CARD_INPUT).strip()


            if not card_no.isdigit():
                print(constant.CARD_NUMBER_DIGIT_ERROR)
                continue

            if len(card_no) != 16:
                print(constant.CARD_NUMBER_LENGTH_ERROR)
                continue

            user = self._find_user_by_card(card_no)
            if not user:
                print(constant.CARD_NOT_FOUND)
                continue

  
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

                user['login_attempt'] = user.get('login_attempt', 0) + 1
                remaining_attempts = constant.MAX_PIN_ATTEMPTS - user['login_attempt']

                if remaining_attempts > 0:
                    print(f"\nIncorrect PIN. {remaining_attempts} attempt(s) remaining.")
                else:
                    print(constant.MAX_PIN_ATTEMPTS_EXCEEDED)
                    print(constant.RETURN_TO_ATM_MENU)
                    return


    def _fetch_atm_by_branch(self, branch_name):
        """Get ATM data by branch name"""
        for atm_id, atm_data in atms.items():
            if atm_data.get('location').lower() == branch_name.lower():
                return atm_data, atm_id
        return None, None

    def _select_atm(self):
        """Allow the user to select an ATM from available options."""
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
        """Display the ATM action menu and handle user operations like deposit, withdraw, and PIN change."""
        atm = atms.get(atm_id)

        while True:

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

            user_id, user = self._authenticate_user()
            if not user:
                print(constant.TRY_AGAIN)
                continue


            if choice == "1":
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
                while True:
                    new_pin = input(constant.ATM_NEW_PIN_INPUT).strip()
                    if self._change_pin(user_id, new_pin):
                        break

            elif choice == "4":
                self._check_balance(user_id)

            print(constant.BACK_TO_MAIN_MENU)

    def _withdraw_money(self, user_id, amount, atm_id):
        """Process a withdrawal transaction, checking limits, fees, and updating balances."""
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
        """This function is used to deposit money into the user's account, and cross-bank deposits throw an error."""
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
        """Change the user's PIN."""
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
        print(constant.PIN_CHANGE_SUCCESS)
        return True

    def _check_balance(self, user_id):
        """Display the user's current balance."""
        user = users.get(user_id)
        if not user:
            print("\n" + constant.USER_NOT_FOUND)
            return

        print(f"\nCurrent balance: INR {user['balance']:.2f}")


    def _exit(self):
        """Exit the ATM system."""
        print(constant.THANK_YOU_ATM)
        print(f"\n  Developed by {constant.DEVELOPER_NAME}")
        self.is_running = False

    def run(self):
        """Run the main ATM system loop, displaying the menu and handling user choices."""
        while self.is_running:

            print("1. User")
            print("2. Bank")
            print("3. Exit")
            print()

            try:
                choice = int(input("Enter your choice: "))
                if choice not in [1, 2, 3]:
                    print(constant.INVALID_MAIN_CHOICE)
                    continue
            except ValueError:
                print(constant.INVALID_MAIN_INPUT)
                continue

            if choice == 1:
                self._select_atm()
            elif choice == 2:
                bank = Bank()
                bank.bank_menu()
            elif choice == 3:
                self._exit()

