"""Dashboard-related constants."""

# Module paths
REPOSITORY_MODULE = "app.repositories.dashboard_repository"
SERVICE_MODULE = "app.services.dashboard_service"
ROUTER_MODULE = "app.api.v1.routes.dashboard"
SCHEMA_MODULE = "app.schemas.dashboard_schemas"

# Router prefix
ROUTER_PREFIX = "/dashboard"
ROUTER_TAG = "dashboard"

# Success messages
SUCCESS_DASHBOARD_SUMMARY_FETCHED = "Dashboard summary retrieved successfully"
SUCCESS_PENDING_ISSUES_FETCHED = "Pending issues retrieved successfully"
SUCCESS_COMPLETED_TASKS_FETCHED = "Completed tasks retrieved successfully"

# Error messages
ERROR_DASHBOARD_ACCESS_DENIED = "Access denied. Only admins and project managers can access dashboard"