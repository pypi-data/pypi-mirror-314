from ezyagent.logging import AgentLogger

# Create logger
logger = AgentLogger(
    level="DEBUG",
    # format="json",
    # outputs=["console", "file"]
)

# Bind context that will be included in all subsequent logs
logger.bind(user_id="123", session_id="abc")

# Basic logging examples
logger.debug("Starting application initialization")
logger.info("Application config loaded", config_path="/etc/app/config.yaml")
logger.warning("Database connection pool running low", connection_count=5)

# Using spans to track operation timing
with logger.span("database_query") as span:
    # Simulate some work
    import time

    time.sleep(1)

    # Add custom tags to the span
    span.set_tag("query_type", "select")
    span.set_tag("table", "users")

    # Log within the span
    logger.info("Executing database query", query="SELECT * FROM users")

# Example of error logging with exception
try:
    raise ValueError("Invalid configuration value")
except Exception as e:
    logger.error(
        "Failed to process configuration",
        error=str(e),
        config_section="database"
    )

# Using spans for nested operations
with logger.span("user_registration") as outer_span:
    outer_span.set_tag("registration_type", "new_user")

    logger.info("Starting user registration process")

    # Nested span for a sub-operation
    with logger.span("email_validation") as inner_span:
        inner_span.set_tag("email_provider", "gmail")
        logger.info("Validating email address")

    logger.info("User registration completed")

# Critical error example
logger.critical(
    "System shutdown initiated",
    reason="Out of memory",
    memory_usage_mb=1024
)