"""Project Member-related constants."""

# Module paths
REPOSITORY_MODULE = "app.repositories.project_member_repository"
SERVICE_MODULE = "app.services.project_member_service"
ROUTER_MODULE = "app.api.v1.routes.project_members"
SCHEMA_MODULE = "app.schemas.project_member_schemas"
MODEL_MODULE = "app.models.project_member"

# Class names
SERVICE_CLASS = "ProjectMemberService"
MODEL_CLASS = "ProjectMember"

# Router prefix
ROUTER_PREFIX = "/project-members"
ROUTER_TAG = "project-members"


# Success messages
SUCCESS_PROJECT_MEMBERS_FETCHED = "Project members fetched successfully"
SUCCESS_ALL_PROJECT_MEMBERS_FETCHED = "All project members fetched successfully"

# Error messages
ERROR_PROJECT_NOT_FOUND = "Project not found"
ERROR_ACCESS_DENIED = "Access denied"
ERROR_PROJECT_MEMBER_NOT_FOUND = "Project member not found"