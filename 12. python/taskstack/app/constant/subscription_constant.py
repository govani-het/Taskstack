"""Subscription-related constants."""

# Module paths
REPOSITORY_MODULE = "app.repositories.subscription_repository"
SERVICE_MODULE = "app.services.subscription_service"
ROUTER_MODULE = "app.api.v1.routes.subscriptions"
SCHEMA_MODULE = "app.schemas.subscription_schemas"
MODEL_MODULE = "app.models.subscription"

# Class names
SERVICE_CLASS = "SubscriptionService"
MODEL_CLASS = "Subscription"

# Router prefix
ROUTER_PREFIX = "/subscriptions"
ROUTER_TAG = "subscriptions"

# Roles
ROLE_SYSTEM_ADMIN = "system admin"

# Success messages
SUCCESS_SUBSCRIPTION_CREATED = "Subscription created successfully"
SUCCESS_SUBSCRIPTION_FETCHED = "Subscription fetched successfully"
SUCCESS_SUBSCRIPTIONS_FETCHED = "Subscriptions fetched successfully"
SUCCESS_SUBSCRIPTION_UPDATED = "Subscription updated successfully"
SUCCESS_SUBSCRIPTION_DELETED = "Subscription deleted successfully"

# Error messages
ERROR_SUBSCRIPTION_PLAN_NAME_ALREADY_EXISTS = "Subscription plan name already exists"
ERROR_SUBSCRIPTION_NOT_FOUND = "Subscription not found"
ERROR_FAILED_TO_DELETE_SUBSCRIPTION = "Failed to delete subscription"