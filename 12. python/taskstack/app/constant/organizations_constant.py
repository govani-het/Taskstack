"""Organization-related constants."""

# Module paths
REPOSITORY_MODULE = "app.repositories.organization_repository"
SERVICE_MODULE = "app.services.organization_service"
ROUTER_MODULE = "app.api.v1.routes.organizations"
SCHEMA_MODULE = "app.schemas.organization_schemas"
MODEL_MODULE = "app.models.organization"

# Class names
SERVICE_CLASS = "OrganizationService"
MODEL_CLASS = "Organization"

# Router prefix
ROUTER_PREFIX = "/organizations"
ROUTER_TAG = "organizations"

# Roles
ROLE_SYSTEM_ADMIN = "system admin"

# Success messages
SUCCESS_ORGANIZATION_CREATED = "Organization created successfully"
SUCCESS_ORGANIZATION_FETCHED = "Organization Fetch Successfully."
SUCCESS_ORGANIZATIONS_FETCHED = "SuccessFully fetch all organizations"
SUCCESS_ORGANIZATION_FETCHED_BY_ID = "Organization fetched successfully"
SUCCESS_UNAPPROVED_ORGANIZATIONS_FETCHED = "Successfully Fetch unapproved organization"
SUCCESS_ORGANIZATION_UPDATED = "Successfully Update Organization"
SUCCESS_ORGANIZATION_APPROVED = "Successfully Approved Organization"
SUCCESS_ORGANIZATION_DELETED = "Successfully Delete Organization"

# Error messages
ERROR_FAILED_TO_CREATE_ORGANIZATION = "Failed to create organization"
ERROR_FAILED_TO_FETCH_ORGANIZATION = "Failed to fetch organization"
ERROR_FAILED_TO_FETCH_ORGANIZATIONS = "Failed to fetch organizations"
ERROR_ORGANIZATION_NOT_FOUND = "Organization not found"
ERROR_NO_ORGANIZATION_ASSOCIATED = "No organization associated"
ERROR_FAILED_TO_FETCH_UNAPPROVED_ORGANIZATIONS = "Failed to fetch unapproved organizations"
ERROR_INVALID_SUBSCRIPTION_PLAN_ID = "Invalid subscription plan ID"
ERROR_ORGANIZATION_EMAIL_ALREADY_REGISTERED = "Organization email already registered"
ERROR_FAILED_TO_UPDATE_ORGANIZATION = "Failed to Update Organization"
ERROR_FAILED_TO_APPROVE_ORGANIZATION = "Failed to Approve Organization"
ERROR_FAILED_TO_DELETE_ORGANIZATION = "Failed to Delete Organization"
ADMIN_ROLE_NOT_FOUND = "Admin role not found"

