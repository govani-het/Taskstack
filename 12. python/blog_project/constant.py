TOKEN_LENGTH = 32
TOKEN_GENERATE_MAX_ATTEMPTS = 10

RESET_EMAIL_SUBJECT = "Reset Your Password"
RESET_EMAIL_BODY_TEMPLATE = (
    "Use this link to reset your password:\n\n"
    "{reset_link}\n\n"
    "This link expires in {minutes} minutes."
)

MSG_INVALID_CREDENTIALS = "Invalid Credentials"
MSG_INVALID_PASSWORD = "Invalid password"
MSG_USER_NOT_FOUND = "User not found"
MSG_PROFILE_NOT_FOUND = "Profile not found"
MSG_UNABLE_GENERATE_RESET_TOKEN = "Unable to generate reset token. Please try again."
MSG_SMTP_NOT_CONFIGURED = "EMAIL_ID or EMAIL_PASSWORD is not configured in .env"
MSG_FAILED_CREATE_RESET_TOKEN = "Failed to create reset token"
MSG_RESET_TOKEN_CREATED = "Reset token generated and email queued successfully"
MSG_PASSWORD_MISMATCH = "New password and confirm password do not match"
MSG_TOKEN_LENGTH = "Token length must be 32"
MSG_INVALID_TOKEN = "Invalid token"
MSG_TOKEN_ALREADY_USED = "Token already used"
MSG_TOKEN_EXPIRED = "Token expired"
MSG_NEW_PASSWORD_SAME_AS_CURRENT = "New password cannot be same as current password"
MSG_FAILED_RESET_PASSWORD = "Failed to reset password"
MSG_PASSWORD_RESET_SUCCESS = "Password reset successful"
MSG_TOKEN_REQUIRED = "Token is required"
MSG_PASSWORD_REQUIRED = "Password cannot be empty"
MSG_MISSING_ENV = "Missing required environment variable"
MSG_COULD_NOT_VALIDATE_CREDENTIALS = "Could not validate credentials"
MSG_BLOG_NOT_FOUND = "Blog not found"
MSG_COMMENT_NOT_FOUND = "Comment not found"
MSG_REPLY_NOT_FOUND = "Reply not found"
MSG_DELETE_ONLY_OWN_COMMENT = "You can delete only your own comment"
MSG_DELETE_ONLY_OWN_REPLY = "You can delete only your own reply"
MSG_FAILED_DELETE_COMMENT = "Failed to delete comment"
MSG_FAILED_DELETE_REPLY = "Failed to delete reply"
MSG_COMMENT_DELETED = "Comment deleted successfully"
MSG_REPLY_DELETED = "Reply deleted successfully"

RESP_KEY_MESSAGE = "message"
RESP_KEY_RESET_LINK = "reset_link"
RESP_KEY_ACCESS_TOKEN = "access_token"
RESP_KEY_TOKEN_TYPE = "token_type"

TOKEN_TYPE_BEARER = "bearer"

