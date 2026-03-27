from data import banks, users, atms
import constant
import hashlib
import random


class Admin:
    """Admin class for performing bank and user management tasks."""
    def __init__(self):
        """Initializes the Admin class.
        
        Takes no arguments.
        
        Returns nothing.
        """
        pass

    def _create_bank_id(self):
        """Generates a unique bank ID in the format BNK001, BNK002, etc.
        
        Takes no arguments.
        
        Returns a unique bank ID string.
        """
        existing_ids = [int(bid.replace('BNK', '')) for bid in banks.keys() if bid.startswith('BNK')]
        return f"BNK{str(max(existing_ids, default=0) + 1).zfill(3)}"

    def _is_bank_exists(self, name, branch):
        """Check if a bank with the given name and branch already exists.

        Args:
            name (str): The name of the bank to check.
            branch (str): The branch name of the bank to check.

        Returns:
            bool: True if the bank exists, False otherwise.
        """
        for bank in banks.values():
            if bank.get('name').lower() == name.lower() and bank.get('branch').lower() == branch.lower():
                return True
        return False

    def _generate_bank_password(self):
        """Generates a random bank password and its hash.
        
        Takes no arguments.
        
        Returns a tuple of (raw_password, hashed_password).
        """

        raw_password = f"Bank@{random.randint(1000, 9999)}"
        hashed_password = hashlib.sha256(raw_password.encode()).hexdigest()

        return raw_password, hashed_password

    def create_bank(self):
        """Creates a new bank with user input for name, branch, and vault amount.
        
        Takes no arguments.
        
        Returns nothing.
        """
        print(constant.ADMIN_CREATE_BANK_TITLE)
        
        while True:
            name = input(constant.ADMIN_BANK_NAME_INPUT).strip()
            if not name:
                print(constant.ADMIN_BANK_NAME_EMPTY_ERROR)
                continue
            if any(char.isdigit() for char in name):
                print(constant.ADMIN_BANK_NAME_DIGIT_ERROR)
                continue
            if not name.replace(' ', '').isalpha():
                print(constant.ADMIN_BANK_NAME_FORMAT_ERROR)
                continue
            break

        while True:
            branch = input(constant.ADMIN_BRANCH_NAME_INPUT).strip()
            if not branch:
                print(constant.ADMIN_BRANCH_NAME_EMPTY_ERROR)
                continue
            if any(char.isdigit() for char in branch):
                print(constant.ADMIN_BRANCH_NAME_DIGIT_ERROR)
                continue
            if not branch.replace(' ', '').isalpha():
                print(constant.ADMIN_BRANCH_NAME_FORMAT_ERROR)
                continue
            break

        if self._is_bank_exists(name, branch):
            print(constant.ADMIN_BANK_EXISTS_ERROR)
            return

        bank_id = self._create_bank_id()

        raw_password, password_hash = self._generate_bank_password()

        banks[bank_id] = {
            'name': name,
            'branch': branch,
            'vault': constant.BANK_VAULT_AMOUNT,
            'password': password_hash
        }

        print(constant.ADMIN_BANK_CREATED_SUCCESS.format(bank_id, name, branch, constant.BANK_VAULT_AMOUNT))
        print(constant.ADMIN_BANK_PASSWORD_MSG.format(raw_password))

    def show_banks(self):
        """Displays all banks with their details including user and ATM counts.
        
        Takes no arguments.
        
        Returns nothing.
        """
        print(constant.ADMIN_ALL_BANKS_TITLE)
        
        if not banks:
            print(constant.ADMIN_BANKS_NOT_FOUND)
            return
        
        for bank_id, bank_data in banks.items():
            user_count = sum(1 for user_data in users.values() if user_data.get('bank_id') == bank_id)
            atm_count = sum(1 for atm_data in atms.values() if atm_data.get('bank_id') == bank_id)
            print(f"{bank_id}: {bank_data.get('name')} | Branch: {bank_data.get('branch')} | Users: {user_count} | ATMs: {atm_count}")

    def show_atms(self):
        """Displays all ATMs with their location, associated bank, and cash balance.
        
        Takes no arguments.
        
        Returns nothing.
        """
        print(constant.ADMIN_ALL_ATMS_TITLE)
        
        if not atms:
            print(constant.ADMIN_ATMS_NOT_FOUND)
            return
        
        for atm_id, atm_data in atms.items():
            bank_name = banks.get(atm_data.get('bank_id'), {}).get('name', 'Unknown')
            print(f"{atm_id}: {atm_data.get('location')} | Bank: {bank_name} | Cash: INR {atm_data.get('available_atm_balance'):.2f}")

    def show_users(self):
        """Displays all users with their name, associated bank, and account balance.
        
        Takes no arguments.
        
        Returns nothing.
        """
        print(constant.ADMIN_ALL_USERS_TITLE)
        
        if not users:
            print(constant.ADMIN_USERS_NOT_FOUND)
            return
        
        for user_id, user_data in users.items():
            bank_name = banks.get(user_data.get('bank_id'), {}).get('name')
            print(f"{user_id}: {user_data.get('name')} | Bank: {bank_name} | Balance: INR {user_data.get('balance'):.2f}")

    def admin_menu(self):
        """Display and handle the admin menu for bank management operations.

        Provides a menu-driven interface for admin operations including:
        - Creating banks
        - Showing banks, users, and ATMs
        - Returning to main menu
        """
        admin = Admin()
        while True:
            print(constant.ADMIN_MENU_TITLE)
            print(constant.ADMIN_MENU_OPTION_1)
            print(constant.ADMIN_MENU_OPTION_2)
            print(constant.ADMIN_MENU_OPTION_3)
            print(constant.ADMIN_MENU_OPTION_4)
            print(constant.ADMIN_MENU_OPTION_5)
            print()
            choice = input(constant.ATM_CHOICE_INPUT).strip()

            if choice == '1':
                admin.create_bank()
            elif choice == '2':
                admin.show_banks()
            elif choice == '3':
                admin.show_users()
            elif choice == '4':
                admin.show_atms()
            elif choice == '5':
                print(constant.RETURN_TO_MAIN_MENU)
                break
            else:
                print(constant.INVALID_MENU_CHOICE)