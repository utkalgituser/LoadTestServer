````md
# Lightweight HTTP Response Simulation Server – Final Engineering Prompt

## Objective

Act as a Senior Backend Engineer and System Architect.

Design and generate a production-ready lightweight HTTP response simulation server using either:

- Python (Preferred: FastAPI + Uvicorn)
OR
- Node.js (Preferred: Express.js)

The solution must be optimized to run efficiently on a standard laptop with:

- 8GB RAM
- Dual-core or higher CPU
- Local development environment

The final implementation should support:
- API mocking
- QA validation
- Integration testing
- Postman sanity testing
- Lightweight load testing
- Failure simulation
- Concurrent request testing

---

# 1. Core Functional Requirements

## 1.1 Lightweight HTTP Server

Build a modular HTTP server that:
- Starts quickly
- Consumes minimal memory and CPU
- Supports concurrent requests efficiently
- Uses minimal external dependencies
- Is easy to maintain and extend
- Follows clean architecture principles
- Supports asynchronous/non-blocking request handling where possible

Preferred runtimes:
- FastAPI + Uvicorn
OR
- Express.js + PM2/Cluster

---

# 2. Dynamic HTTP Response Engine

The server must dynamically return configurable HTTP responses (1XX–5XX) based on:

- Query parameters
- Request headers
- HTTP methods
- Request payload validation
- Config-driven endpoint behavior

---

## 2.1 Supported Response Simulation Examples

Examples:
- Missing required header → `400 Bad Request`
- Invalid token → `401 Unauthorized`
- Unsupported method → `405 Method Not Allowed`
- Invalid JSON → `422 Unprocessable Entity`
- Query param `?status=503` → `503 Service Unavailable`
- Header `X-Debug-Mode=true` → verbose debug response
- Timeout simulation → delayed response

---

## 2.2 Response Engine Features

The response system must support:
- Configurable HTTP status codes
- Configurable response bodies
- Configurable response headers
- JSON responses
- Plain text responses
- Configurable response delays
- Timeout simulation
- Error simulation
- Success/failure mock scenarios
- Centralized response configuration

---

# 3. API Design Requirements

Include the following endpoints:

- `/health`
- `/metrics`
- `/mock/*`
- `/status`
- `/config`

Optional:
- `/auth/mock`
- `/delay/mock`
- `/failure/mock`

---

# 4. Middleware Requirements

Implement middleware support for:
- Request validation
- Authentication simulation
- Rate limiting simulation
- Correlation/request IDs
- Request logging
- Error handling
- Timeout handling

---

# 5. Request Input Documentation (Mandatory)

For every endpoint, document all request inputs in detail.

---

## 5.1 Endpoint Documentation

For every endpoint include:
- Endpoint URL
- Supported HTTP methods
- Endpoint description
- Request examples
- Response examples
- Expected HTTP status codes

Example:
```yaml
Endpoint: /mock/payment
Method: POST
Description: Simulates payment processing API
```

---

## 5.2 Header Documentation

Document:
- Header name
- Data type
- Required/Optional
- Accepted values
- Default values
- Validation rules
- Example values

Example:
```yaml
Headers:
  Authorization:
    Type: String
    Required: Yes
    Format: Bearer Token

  X-Request-ID:
    Type: UUID
    Required: No
```

---

## 5.3 Query Parameter Documentation

Document:
- Parameter name
- Data type
- Required/Optional
- Default value
- Allowed values
- Validation rules
- Description
- Example

Example:
```yaml
Query Parameters:
  status:
    Type: Integer
    Required: No
    Allowed Values: 200,400,500

  delay:
    Type: Integer
    Unit: milliseconds
```

---

## 5.4 Request Body Documentation

Document:
- Content-Type support
- JSON schema
- Required fields
- Optional fields
- Validation rules
- Nested object structure
- Example payloads

Example:
```json
{
  "transactionId": "TXN12345",
  "amount": 1000,
  "currency": "USD"
}
```

Example schema:
```yaml
transactionId:
  Type: String
  Required: Yes

amount:
  Type: Number
  Required: Yes
  Minimum: 1
```

---

# 6. Validation Rules Documentation

Document:
- Mandatory fields
- Optional fields
- Header validation rules
- Query validation rules
- Request body validation rules
- Invalid request behavior
- Error response mappings

Examples:
- Missing Authorization header → 401
- Invalid JSON → 422
- Unsupported Content-Type → 415
- Unsupported method → 405

---

# 7. API Response Documentation

For every response include:
- HTTP status code
- Description
- Response headers
- Response schema
- Example payloads

Example:
```yaml
200 OK:
  Description: Successful request

400 Bad Request:
  Description: Missing required header

500 Internal Server Error:
  Description: Simulated failure
```

---

# 8. Logging System Requirements

Implement structured logging with:
- Timestamped log filenames
- Separate application logs
- Separate error logs
- Separate access logs

Support log levels:
- DEBUG
- INFO
- WARN
- ERROR

Example filename:
```bash
logs/server-2026-05-11_14-30-22.log
```

Requirements:
- Console logging
- File logging
- Log rotation support
- Request correlation IDs

---

# 9. Configuration Management

Use `.env` based configuration.

Configurable values:
- HOST
- PORT
- LOG_LEVEL
- DEFAULT_STATUS_CODE
- TIMEOUT
- MAX_PAYLOAD_SIZE
- ALLOWED_HEADERS
- ENABLE_DEBUG
- RATE_LIMIT
- WORKER_COUNT

Generate:
- `.env.example`

---

# 10. Operational Scripts

Generate scripts for:
- Start server
- Stop server
- Restart server
- Status/health verification

Requirements:
- PID-based process management
- Graceful shutdown
- Background execution support
- Automatic log directory creation

Cross-platform support preferred.

---

# 11. Documentation Requirements

Generate the following documentation files:

- `README.md`
- `Instructions.md`
- `API_SPEC.md`
- `REQUEST_SCHEMA.md`
- `RESPONSE_SCHEMA.md`
- `.env.example`

---

# 12. README Requirements

The `README.md` must include:

## Setup
- Installation steps
- Dependency installation
- Environment setup
- Running locally

## Operations
- Start commands
- Stop commands
- Restart commands
- Health verification

## API Usage
- Curl examples
- Request examples
- Response examples

## Logging
- Log locations
- Log levels
- Rotation strategy

## Troubleshooting
- Common issues
- Fixes
- Debugging guidance

## Extension Guidance
- How to add endpoints
- How to add middleware
- How to add custom responses

---

# 13. Postman Compatibility Requirements

The APIs must be Postman-friendly.

Generate:
- Sample Postman collection
- Environment variables
- Example requests
- Positive test scenarios
- Negative test scenarios

Include sanity validation examples for:
- 200 OK
- 400 Bad Request
- 401 Unauthorized
- 404 Not Found
- 405 Method Not Allowed
- 422 Validation Error
- 500 Internal Server Error
- Timeout simulation

---

# 14. Load Testing Support

The server must support lightweight load testing using:
- Apache JMeter
- K6

The implementation should:
- Handle concurrent requests efficiently
- Avoid unnecessary memory usage
- Support keep-alive connections
- Maintain stable response times under small loads
- Use efficient request handling

---

# 15. Performance & Capacity Documentation

Generate a dedicated README section explaining:

## Recommended Environment

```yaml
System RAM: 8GB
CPU: Dual-core or higher
Recommended Concurrent Users: 50–200
Recommended RPS: 100–500
Payload Size: < 1MB
Recommended Test Duration: 5–15 minutes
```

Clearly explain:
- These are lightweight testing estimates
- Actual throughput depends on:
  - CPU
  - Network
  - Payload size
  - Logging level
  - Runtime choice
  - Background OS usage

---

# 16. Performance Optimization Requirements

Include:
- Keep-alive support
- Configurable worker count
- Minimal synchronous blocking
- Efficient logging
- Graceful degradation under load
- Memory-efficient request handling
- Optional gzip compression

Recommendations:
- Disable DEBUG logging during load testing
- Use async request handling
- Reuse connections

---

# 17. Benchmark & Load Testing Examples

Generate:
- Sample JMeter test plan structure
- Sample K6 script
- Example load test commands
- Example benchmark metrics

Metrics to include:
- Average response time
- P95 latency
- Throughput
- Error percentage
- Approximate memory usage

---

# 18. Stability & Resilience Requirements

The server should:
- Recover gracefully from invalid requests
- Avoid crashes during malformed payloads
- Handle concurrent requests safely
- Support graceful shutdown during active traffic
- Prevent memory leaks
- Maintain stable logging under concurrent load

---

# 19. Security Best Practices

Include:
- Input validation
- Request size limits
- Header sanitization
- Basic rate limiting
- Error sanitization
- Safe logging practices

Avoid:
- Hardcoded secrets
- Sensitive data logging

---

# 20. Docker Support (Optional but Preferred)

Generate:
- Lightweight Dockerfile
- Docker run instructions
- Optional docker-compose example

Prefer lightweight images.

---

# 21. Code Quality Expectations

Ensure the implementation:
- Uses modular folder structure
- Follows clean coding practices
- Includes inline comments where needed
- Avoids hardcoded values
- Uses reusable utility modules
- Is easy to scale later

---

# 22. Deliverables

Generate:
- Complete source code
- Folder structure
- Dependency manifest
- Startup scripts
- Shutdown scripts
- Restart scripts
- Full documentation
- Sample configs
- Sample requests
- Sample responses
- Validation examples
- Error simulation examples
- Load testing examples

---

# 23. Final Acceptance Criteria

The final solution must:
- Run successfully on an 8GB RAM laptop
- Support Postman sanity testing
- Support lightweight JMeter/K6 load testing
- Be easy to extend
- Be production-style and modular
- Be fully documented
- Be runnable with minimal setup
- Be stable during lightweight concurrent load testing
- Support realistic API mock and failure simulation scenarios
````
