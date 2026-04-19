"""Reply-related constants."""

# Module paths
MODEL_MODULE = "app.models.reply"

# Class names
MODEL_CLASS = "Reply"

# Success messages
SUCCESS_REPLY_CREATED = "Reply created successfully"
SUCCESS_REPLY_UPDATED = "Reply updated successfully"
SUCCESS_REPLY_DELETED = "Reply deleted successfully"
SUCCESS_REPLIES_FETCHED = "Replies fetched successfully"

# Error messages
ERROR_REPLY_NOT_FOUND = "Reply not found"
ERROR_REPLY_FORBIDDEN = "You do not have permission to perform this action on this reply"
ERROR_REPLY_UPDATE_FORBIDDEN = "You can only update your own replies"
ERROR_REPLY_DELETE_FORBIDDEN = "You can only delete your own replies"