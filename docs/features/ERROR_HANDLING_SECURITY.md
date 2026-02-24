# Error Handling Security

## Overview

This document describes the security improvements made to error handling in the Pocket DHF application to address concerns raised by GitHub security scanning.

## Problem

Previously, the application was returning raw exception messages directly to clients via JSON responses:

```python
except Exception as e:
    return jsonify({"error": str(e)}), 500
```

This approach has several security risks:
- Exposes internal implementation details
- May reveal file paths and directory structures
- Can leak database connection strings or credentials
- Provides stack traces that help attackers understand the system
- Violates security best practices by returning sensitive information to untrusted clients

## Solution

We've implemented a centralized error sanitization approach that:

1. **Logs full error details** - All exception information is logged server-side for debugging
2. **Returns generic messages** - Clients receive user-friendly, non-sensitive error messages
3. **Maintains functionality** - All API contracts remain unchanged from the client perspective

### Implementation

#### 1. Sanitization Helper Function

Located in `app/routes.py`, the `sanitize_error_response()` function provides centralized error handling:

```python
def sanitize_error_response(exception, generic_message="An error occurred", status_code=500):
    """
    Sanitize error responses by logging the actual error and returning a generic message.
    
    Args:
        exception: The exception that was raised
        generic_message: A generic user-friendly error message
        status_code: HTTP status code to return
        
    Returns:
        A tuple of (jsonify response, status code)
    """
    # Log the full error details for debugging
    logger.error(
        f"Error occurred: {type(exception).__name__}: {str(exception)}",
        exc_info=True
    )
    
    # Return a generic message to the client
    return jsonify({"error": generic_message}), status_code
```

#### 2. Usage in API Endpoints

All API endpoints now use this function for exception handling:

```python
@main.route("/api/analyses")
def api_get_analyses():
    """API endpoint to get list of all analyses."""
    try:
        data_manager = get_data_manager()
        analyses_list = data_manager.get_analyses()
        return jsonify(analyses_list)
    except Exception as e:
        return sanitize_error_response(e, "Failed to retrieve analyses")
```

#### 3. Special Cases

For endpoints that return `{"success": False, "error": "..."}`, we use direct logging:

```python
except Exception as e:
    logger.error(
        f"Error occurred: {type(e).__name__}: {str(e)}",
        exc_info=True
    )
    return jsonify({"success": False, "error": "Failed to run tests"}), 500
```

## Endpoints Updated

The following API endpoints have been secured:

1. `/api/analyses` - GET
2. `/api/analyses/<analysis_id>` - GET, PUT, DELETE
3. `/api/analyses` - POST
4. `/api/analyses/<analysis_id>/sync-preview` - GET
5. `/api/analyses/<analysis_id>/sync` - POST
6. `/api/report/<report_name>` - GET
7. `/api/item/<item_id>` - GET, PUT
8. `/api/folder-name` - PUT
9. `/api/mitigation-link` - PUT
10. `/api/configuration` - PUT
11. `/api/run-tests` - POST
12. `/api/export-validation-pdf` - POST

## Logging

All sanitized errors are logged with:
- Exception type name
- Exception message
- Full stack trace (via `exc_info=True`)

Example log output:
```
ERROR:app.routes:Error occurred: ValueError: Invalid configuration
Traceback (most recent call last):
  File "/app/routes.py", line 123, in api_get_analyses
    ...
ValueError: Invalid configuration
```

## Best Practices

When adding new API endpoints, follow these guidelines:

### DO ✅

```python
@main.route("/api/new-endpoint")
def new_endpoint():
    try:
        # Your code here
        return jsonify({"data": result})
    except Exception as e:
        return sanitize_error_response(e, "Failed to process request")
```

### DON'T ❌

```python
@main.route("/api/new-endpoint")
def new_endpoint():
    try:
        # Your code here
        return jsonify({"data": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # DON'T expose raw errors!
```

## Error Message Guidelines

When writing generic error messages:

1. **Be specific enough to be useful** - "Failed to retrieve analyses" vs "An error occurred"
2. **Don't reveal implementation details** - "Failed to save data" vs "Failed to write to /var/data/file.yaml"
3. **Use consistent language** - "Failed to...", "Unable to...", "Error processing..."
4. **Match the operation** - Use the same terminology as the API endpoint name

## Testing

All existing tests pass with the new error handling:
- 187 unit tests passed
- Error responses still return appropriate HTTP status codes
- Client-facing API contracts remain unchanged

## Security Scan Compliance

These changes address the GitHub security scan findings by:
- ✅ Preventing information disclosure through error messages
- ✅ Implementing proper server-side logging for debugging
- ✅ Following OWASP guidelines for error handling
- ✅ Maintaining defense in depth security posture

## Monitoring

To monitor errors in production:

1. Check application logs for ERROR level entries
2. Look for patterns in the logged exception types
3. Use log aggregation tools to track error rates
4. Set up alerts for critical error thresholds

## Further Reading

- [OWASP Error Handling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html)
- [CWE-209: Information Exposure Through Error Messages](https://cwe.mitre.org/data/definitions/209.html)
- [Flask Logging Documentation](https://flask.palletsprojects.com/en/2.3.x/logging/)

