"""Comment-related constants."""

# Module paths
MODEL_MODULE = "app.models.comment"

# Class names
MODEL_CLASS = "Comment"

# Success messages
SUCCESS_COMMENT_CREATED = "Comment created successfully"
SUCCESS_COMMENT_UPDATED = "Comment updated successfully"
SUCCESS_COMMENT_DELETED = "Comment deleted successfully"
SUCCESS_COMMENTS_FETCHED = "Comments fetched successfully"

# Error messages
ERROR_COMMENT_NOT_FOUND = "Comment not found"
ERROR_COMMENT_FORBIDDEN = "You do not have permission to perform this action on this comment"
ERROR_COMMENT_UPDATE_FORBIDDEN = "You can only update your own comments"
ERROR_COMMENT_DELETE_FORBIDDEN = "You can only delete your own comments"