"""User-related constants."""

# Module paths
REPOSITORY_MODULE = "app.repositories.user_repository"
SERVICE_MODULE = "app.services.user_service"
ROUTER_MODULE = "app.api.v1.routes.users"
SCHEMA_MODULE = "app.schemas.user_schemas"
MODEL_MODULE = "app.models.users"

# Class names
SERVICE_CLASS = "UserService"
MODEL_CLASS = "User"

# Router prefix
ROUTER_PREFIX = "/users"
ROUTER_TAG = "users"



# Success messages
SUCCESS_USER_CREATED = "User created successfully"
SUCCESS_USER_FETCHED = "User fetched successfully"
SUCCESS_USERS_FETCHED = "Users fetched successfully"
SUCCESS_USER_UPDATED = "User updated successfully"
SUCCESS_USER_DELETED = "User deleted successfully"
SUCCESS_USER_PROMOTED_TO_ADMIN = "User promoted to admin successfully"
SUCCESS_MULTIPLE_ADMINS_PER_ORG = "Organization supports multiple admins"
SUCCESS_MULTIPLE_SUBSCRIPTIONS_PER_ORG = "Organization supports multiple subscription plans"
SUCCESS_MULTIPLE_PROJECT_MANAGERS_PER_PROJECT = "Project supports multiple project managers, developers, and reporters"

# Error messages
ERROR_EMAIL_ALREADY_REGISTERED = "Email already registered"
ERROR_CANNOT_CREATE_ROLE_USER = "You cannot create an {role_name} user"
ERROR_INVALID_ROLE_NAME = "Invalid role name"
ERROR_INVALID_ORGANIZATION_NAME = "Invalid organization name"
ERROR_USER_NOT_FOUND = "User not found"
ERROR_FAILED_TO_DELETE_USER = "Failed to delete user"
ERROR_USER_CAN_UPDATE_OWN_PROFILE = "User can only update own profile"
ERROR_ONLY_ADMIN_CAN_PROMOTE = "Only admins can promote users to admin role"
ERROR_CANNOT_PROMOTE_TO_ADMIN = "Cannot promote user to admin role"