"""Work Log-related constants."""

# Module paths
REPOSITORY_MODULE = "app.repositories.work_log_repository"
SERVICE_MODULE = "app.services.work_log_service"
ROUTER_MODULE = "app.api.v1.routes.work_logs"
SCHEMA_MODULE = "app.schemas.work_log_schemas"
MODEL_MODULE = "app.models.work_log"

# Class names
SERVICE_CLASS = "WorkLogService"
MODEL_CLASS = "WorkLog"

# Router prefix
ROUTER_PREFIX = "/work-logs"
ROUTER_TAG = "work logs"

# Success messages
SUCCESS_WORK_LOG_CREATED = "Work log created successfully"
SUCCESS_WORK_LOG_FETCHED = "Work log fetched successfully"
SUCCESS_WORK_LOGS_FETCHED = "Work logs fetched successfully"
SUCCESS_WORK_LOG_UPDATED = "Work log updated successfully"
SUCCESS_WORK_LOG_DELETED = "Work log deleted successfully"

# Error messages
ERROR_WORK_LOG_NOT_FOUND = "Work log not found"
ERROR_WORK_LOG_ACCESS_DENIED = "Access denied for this work log"
ERROR_WORK_LOG_CREATION_DENIED = "You don't have permission to create work logs for this ticket"
ERROR_WORK_LOG_UPDATE_DENIED = "You don't have permission to update this work log"
ERROR_WORK_LOG_DELETE_DENIED = "You don't have permission to delete this work log"
ERROR_INVALID_TIME_SPENT = "Time spent must be greater than 0"
ERROR_TICKET_NOT_FOUND = "Ticket not found"
ERROR_PROJECT_ACCESS_DENIED = "You don't have access to this project"