"""Login-related constants."""

# Module paths
REPOSITORY_MODULE = "app.repositories.auth_query"
SCHEMA_MODULE = "app.schemas.login_schemas"
ROUTER_MODULE = "app.api.v1.routes.login"

# Router prefix
ROUTER_PREFIX = "/app/v1/auth"
ROUTER_TAG = "login"

# Error messages
ERROR_COULD_NOT_VALIDATE_CREDENTIALS = "Could not validate credentials"
ERROR_INVALID_OR_MISSING_TOKEN = "Invalid or missing token"
ERROR_FORBIDDEN = "Forbidden"