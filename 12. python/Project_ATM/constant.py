
ATM_CARD_INPUT           = "\n  Enter card number : "
ATM_PIN_INPUT            = "\n  Enter PIN          : "
ATM_NEW_PIN_INPUT        = "\n  Enter new PIN      : "
ATM_AMOUNT_INPUT         = "\n  Enter amount (INR)   : "
ATM_SELECT_ATM_INPUT     = "\n  Select branch      : "
ATM_CHOICE_INPUT         = "\n  Select Options        : "
BANK_CHOICE_INPUT        = "\n  Select Bank         :"

ATM_BALANCE_INPUT        = "\n  Enter initial balance (INR) : "
ATM_ATM_ID_INPUT         = "\n  Enter branch name  : "
ATM_FUND_AMOUNT_INPUT    = "\n  Enter amount to add (INR) : "
ATM_DOB_INPUT            = "\n  Enter DOB (DD/MM/YYYY) : "
ATM_PHONE_INPUT          = "\n  Enter phone number (10 digits) : "
ATM_AADHAR_INPUT         = "\n  Enter Aadhar card (12 digits) : "
ATM_PAN_INPUT            = "\n  Enter PAN card : "
USER_NAME_INPUT          = "\n  Enter Your name         : "
NAME_BLANK_ERROR         = "\n  Name cannot be blank. Please enter a valid name."
NAME_LENGTH_ERROR        = "\n  Name must be between 3 and 60 characters. Please enter a valid name."
NAME_FORMAT_ERROR        = "\n  Name can only contain letters and spaces. Please enter a valid name."


PAN_FORMAT_ERROR         = "\n PAN format invalid."
PAN_ALREADY_EXISTS_ERROR = "\n This PAN card is already used."
INITIAL_BALANCE_MIN_ERROR = "\n Initial balance must be at least INR 1000."
INITIAL_BALANCE_MAX_ERROR = "\n Initial balance cannot exceed INR 50000."
ATM_BRANCH_NAME_ERROR    = "\n Please enter a valid branch name."
ATM_ALREADY_EXISTS_ERROR = "\n ATM already exists at this branch location. Please choose a different branch name."
ATM_FUND_AMOUNT_ERROR    = "\n Invalid cash amount. Please enter a valid number."
ATM_MINIMUM_FUNDING_ERROR = "\n Minimum ATM funding is INR 1,00,000 (1 Lakh). Please enter a valid amount."
INVALID_BRANCH_NAME      = "\n Invalid branch name. Please select from the list above."
INVALID_BRANCH_SELECTION = "\n Invalid branch name."
INVALID_MENU_CHOICE      = "\n Invalid input. Please enter a number between 1 and 7."
RETURN_TO_ATM_MENU      = "\n Please return to the ATM menu and try again."
MINIMUM_WITHDRAW_ERROR  = "\n Minimum withdraw amount is INR 100."
MULTIPLE_OF_100_ERROR   = "\n Amount must be in multiples of INR 100."
THANK_YOU_ATM           = "Thank you for using Project ATM."

DEVELOPER_NAME          = "Het Govani"


BANK_NOT_FOUND           = "\n  Bank not found."
USER_NOT_FOUND           = "\n  User not found."
ATM_NOT_FOUND            = "\n  ATM not found"

CROSS_BANK_DEPOSIT_ERROR    = "\n cross-bank deposits are not allowed at this ATM."
CROSS_BANK_WITHDRAWAL_LIMIT_ERROR = "\n Amount exceeds cross-bank withdrawal limit"

MSG_WITHDRAW_SUCCESS         = "\n  Withdrawal successful, Amount: INR{:.2f} , New Balance: INR{:.2f}"
MSG_DEPOSIT_SUCCESS          = "\n  Deposit successful, Amount: INR{:.2f} , New Balance: INR{:.2f}"
MSG_CROSS_BANK_CHARGE        = "\n  Cross-bank fee ({:.0f}%): INR{:.2f}"
MSG_TOTAL_DEDUCTED           = "\n  Total deducted: INR{:.2f}"
MSG_INSUFFICIENT_BALANCE     = "\n  Insufficient account balance."
MSG_INSUFFICIENT_ATM_BALANCE = "\n  ATM does not have sufficient cash. Please try another ATM."
MSG_INVALID_AMOUNT           = "\n  Invalid amount."


MSG_SINGLE_LIMIT         = "\n  Amount exceeds single-transaction limit of INR{:.2f}."
MSG_DAILY_AMOUNT_LIMIT   = "\n  Daily transaction amount limit of INR{:.2f} exceeded."
MSG_DAILY_COUNT_LIMIT    = "\n  Daily transaction limit of {} transactions reached."
MSG_REMAINING_LIMIT      = "\n  Remaining daily limit: INR{:.2f} , Remaining transactions: {}"


MSG_ATM_ADDED            = "\n  ATM added! ID: {} | Bank: {} | Balance: INR{:.2f}"
MSG_ATM_FUNDED           = "\n  ATM funded! New balance: INR{:.2f}"
MSG_USER_ADDED           = "\n  User created!\n  Name : {}\n  Card : {}\n  PIN  : {}\n  Bank : {}\n  Bal  : INR{:.2f}"

MSG_EXIT                 = "\n  Thank you for using ATM Simulation System. Goodbye!\n"
 
MAX_WITHDRAWAL_PER_TXN    = 25000      
MAX_DEPOSIT_PER_TXN       = 50000      
MAX_DAILY_DEPOSIT_AMOUNT  = 50000      
MAX_DAILY_TXN_AMOUNT      = 100000     
MAX_DAILY_TXN_COUNT       = 10         
CROSS_BANK_FEE_PERCENT    = 5           
MAX_PIN_ATTEMPTS          = 3 
CROSS_BANK_WITHDRAWAL_LIMIT = 10000


MINIMUM_DEPOSIT_ERROR = "\n Minimum deposit amount is 100."
DEPOSIT_AMOUNT_ERROR = "\n Amount must be in multiples of 100"
    
DAILY_DEPOSIT_LIMIT_ERROR = "\n Daily deposit limit exceeded"

INVALID_CHOICE_SELECTED = "\n Invalid operation selected"
RETURN_TO_MAIN_MENU = "\n Returning to main menu"
TRY_AGAIN = "\n Please try again"

AMOUNT_MUST_GREATER_THAN_ZERO = "\n Amount must be greater than zero"
INVALID_INPUT = "\n Invalid input"

BACK_TO_MAIN_MENU = "\n Returning to main menu"

AVAILABLE_ATM = "\n  Available ATMs:"
AVAILABLE_BANK = "\n  Available Banks:"

PHONE_NUMBER_ERROR = "\n Phone number must be exactly 10 digits with no alphabets."
PHONE_NUMBER_START_WITH_ERROR = '\n Phone number must start with digit 6, 7, 8, or 9.'

AGE_ERROR = "\n Your Age must be greater than 16."
OVER_AGE_ERROR = "\nInvalid date of birth."
DOB_FORMAT_ERROR = "\nInvalid date of birth format. Please use DD/MM/YYYY."

AADHAR_CARD_ERROR = "\n Aadhar card must be exactly 12 digits."
AADHAR_CARD_START_WITH_ERROR = "\n Aadhar card cannot start with 01 or 10."
AADHAR_CARD_ALREADY_EXISTS = "\n This Aadhar card is already registered in this bank."

INVALID_MAIN_CHOICE = "\n Invalid choice. Please enter a number between 1 and 3."
INVALID_MAIN_INPUT = "\n Invalid input. Please enter a number."
PIN_FORMAT_ERROR = "\n PIN must be exactly 4 digits."
PIN_CHANGE_SAME_ERROR = "\n New PIN cannot be the same as the old PIN."
PIN_CHANGE_SUCCESS = "\n PIN changed successfully."
CARD_NOT_FOUND = "\n Card not found."
CARD_NUMBER_DIGIT_ERROR = "\n Card number must be a digit."
MAX_PIN_ATTEMPTS_EXCEEDED = "\n Maximum PIN attempts exceeded. Please try again later."
CARD_NUMBER_LENGTH_ERROR = "\n Card number must be exactly 16 digits."
AUTH_SUCCESS = '\n Authentication successful for {} and Bank: {}'