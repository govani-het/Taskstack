"""Project-related constants."""

# Module paths
REPOSITORY_MODULE = "app.repositories.project_repository"
SERVICE_MODULE = "app.services.project_service"
ROUTER_MODULE = "app.api.v1.routes.projects"
SCHEMA_MODULE = "app.schemas.project_schemas"
MODEL_MODULE = "app.models.projects"

# Class names
SERVICE_CLASS = "ProjectService"
MODEL_CLASS = "Project"

# Router prefix
ROUTER_PREFIX = "/projects"
ROUTER_TAG = "projects"

# Roles
ROLE_SYSTEM_ADMIN = "system admin"

# Success messages
SUCCESS_PROJECT_FETCHED = "Project fetched successfully"
SUCCESS_PROJECT_CREATED = "Project created successfully"
SUCCESS_PROJECTS_FETCHED = "Projects fetched successfully"
SUCCESS_ALL_PROJECTS_FETCHED = "All projects fetched successfully"

# Error messages
ERROR_PROJECT_NOT_FOUND = "Project not found"
ERROR_ACCESS_DENIED = "Access denied"
ERROR_NO_ORGANIZATION_ASSOCIATED = "No organization associated"