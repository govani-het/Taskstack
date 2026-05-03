"""Role-related constants."""

# Module paths
REPOSITORY_MODULE = "app.repositories.role_repository"
SERVICE_MODULE = "app.services.role_service"
ROUTER_MODULE = "app.api.v1.routes.roles"
SCHEMA_MODULE = "app.schemas.role_schemas"
MODEL_MODULE = "app.models.roles"

# Class names
SERVICE_CLASS = "RoleService"
MODEL_CLASS = "Role"

# Router prefix
ROUTER_PREFIX = "/roles"
ROUTER_TAG = "roles"

# Roles
ROLE_SYSTEM_ADMIN = "system admin"
ROLE_ADMIN = "admin"
ROLE_PROJECT_MANAGER = "project manager"
ROLE_DEVELOPER = "developer"
ROLE_REPORTER = "reporter"

# Success messages
SUCCESS_ROLE_CREATED = "Role created successfully"
SUCCESS_ROLE_FETCHED = "Role fetched successfully"
SUCCESS_ROLES_FETCHED = "Roles fetched successfully"
SUCCESS_ROLE_UPDATED = "Role updated successfully"
SUCCESS_ROLE_DELETED = "Role deleted successfully"

# Error messages
ERROR_ROLE_NAME_ALREADY_EXISTS = "Role name already exists"
ERROR_ROLE_NOT_FOUND = "Role not found"
ERROR_FAILED_TO_DELETE_ROLE = "Failed to delete role"