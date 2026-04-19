"""Ticket-related constants."""

# Module paths
MODEL_MODULE = "app.models.ticket"

# Class names
MODEL_CLASS = "Ticket"

# Router constants
ROUTER_PREFIX = "/tickets"
ROUTER_TAG = "tickets"

# Ticket types
TICKET_TYPE_BUG = "bug"
TICKET_TYPE_TASK = "task"

# Ticket statuses
STATUS_PENDING = "pending"
STATUS_PROCESS = "process"
STATUS_COMPLETED = "completed"
STATUS_CANCELED = "canceled"

# Status workflow transitions (valid next statuses from current status)
STATUS_WORKFLOW = {
    STATUS_PENDING: [STATUS_PROCESS, STATUS_CANCELED],
    STATUS_PROCESS: [STATUS_COMPLETED, STATUS_CANCELED],
    STATUS_COMPLETED: [],
    STATUS_CANCELED: [],
}

# Ticket priorities
PRIORITY_HIGH = "high"
PRIORITY_INTERMEDIATE = "intermediate"
PRIORITY_LOW = "low"

# Response messages
SUCCESS_TICKET_CREATED = "Ticket created successfully"
SUCCESS_TICKET_FETCHED = "Ticket fetched successfully"
SUCCESS_TICKETS_FETCHED = "Tickets fetched successfully"
SUCCESS_TICKET_UPDATED = "Ticket updated successfully"
SUCCESS_TICKET_DELETED = "Ticket deleted successfully"
SUCCESS_TICKET_ASSIGNED = "Ticket assigned successfully"
SUCCESS_TICKET_CANCELED = "Ticket canceled successfully"
SUCCESS_COMMENT_CREATED = "Comment added successfully"
SUCCESS_COMMENTS_FETCHED = "Comments fetched successfully"

# Error messages
ERROR_TICKET_NOT_FOUND = "Ticket not found"
ERROR_TICKET_FORBIDDEN = "Access denied for this ticket"
ERROR_PROJECT_NOT_FOUND = "Project not found"
ERROR_TICKET_NOT_IN_PROJECT = "Ticket does not belong to the requested project"
ERROR_ASSIGNEE_INVALID = "Assignee must be an active project member with the proper role"
ERROR_TICKET_ASSIGNMENT_NOT_ALLOWED = "You cannot assign this ticket"
ERROR_TICKET_ASSIGN_NOT_ALLOWED = "Only project managers and admins can assign tickets"
ERROR_TICKET_STATUS_CHANGE_NOT_ALLOWED = "You cannot change ticket status"
ERROR_TICKET_UPDATE_NOT_ALLOWED = "You are not allowed to update this ticket"
ERROR_TICKET_DELETE_NOT_ALLOWED = "You are not allowed to delete this ticket"
ERROR_COMMENT_FORBIDDEN = "You are not allowed to comment on this ticket"
ERROR_INVALID_STATUS_TRANSITION = "Invalid status transition: cannot change from {current} to {target}"
ERROR_TICKET_CANCEL_NOT_ALLOWED = "You do not have permission to cancel this ticket"
ERROR_DEVELOPER_CANNOT_CANCEL = "Developers cannot cancel tickets"
SUCCESS_TICKET_CANCELED = "Ticket canceled successfully"
