# AIBOM Agent System - API Reference

This document provides detailed API reference for the AIBOM Agent System, including request/response schemas, error codes, and advanced configuration options.

## Table of Contents

- [API Overview](#api-overview)
- [Request Schema](#request-schema)
- [Response Schema](#response-schema)
- [Error Codes](#error-codes)
- [Advanced Configuration](#advanced-configuration)
- [Rate Limiting](#rate-limiting)
- [Session Management](#session-management)

## API Overview

The AIBOM Agent System exposes a single endpoint that accepts JSON payloads with different actions. All requests are made through the AgentCore runtime.

### Base Command
```bash
agentcore invoke '<json_payload>' [options]
```

### Supported Actions
- `analyze_model`: Analyze a single Hugging Face model
- `compare_models`: Compare multiple Hugging Face models

## Request Schema

### Single Model Analysis

```json
{
  "action": "analyze_model",
  "model_name": "string"
}
```

**Parameters:**
- `action` (string, required): Must be "analyze_model"
- `model_name` (string, required): Hugging Face model identifier (e.g., "microsoft/DialoGPT-medium")

**Example:**
```bash
agentcore invoke '{
  "action": "analyze_model",
  "model_name": "microsoft/DialoGPT-medium"
}'
```

### Multi-Model Comparison

```json
{
  "action": "compare_models",
  "model_names": ["string", "string", ...]
}
```

**Parameters:**
- `action` (string, required): Must be "compare_models"
- `model_names` (array of strings, required): List of Hugging Face model identifiers (minimum 2, maximum 10)

**Example:**
```bash
agentcore invoke '{
  "action": "compare_models",
  "model_names": [
    "microsoft/DialoGPT-medium",
    "facebook/blenderbot-400M-distill",
    "google/flan-t5-base"
  ]
}'
```

## Response Schema

### Successful Single Model Analysis

```json
{
  "success": true,
  "action": "analyze_model",
  "model_name": "string",
  "security_issues_count": "integer",
  "compliance_gaps_count": "integer", 
  "report_path": "string",
  "aibom_summary": {
    "components_count": "integer",
    "vulnerabilities_count": "integer",
    "risk_level": "string"
  }
}
```

**Fields:**
- `success` (boolean): Always true for successful requests
- `action` (string): Echo of the requested action
- `model_name` (string): Echo of the analyzed model name
- `security_issues_count` (integer): Number of security issues identified (enhanced analysis may detect more issues)
- `compliance_gaps_count` (integer): Number of compliance gaps found
- `report_path` (string): Path to the generated HTML report with enhanced interactive sections
- `aibom_summary` (object): Summary of AIBOM analysis
  - `components_count` (integer): Total number of components in the AIBOM
  - `vulnerabilities_count` (integer): Number of known vulnerabilities
  - `risk_level` (string): Overall risk level ("LOW", "MEDIUM", "HIGH", "CRITICAL")

### Enhanced Security Analysis in Reports

The generated HTML reports now include detailed interactive sections:

#### Analysis Methodology Section
- Transparent explanation of the security assessment approach
- Data sources analyzed (AIBOM components, model metadata, file listings)
- Step-by-step analysis process
- Tools and techniques used
- Coverage scope and limitations

#### Risk Factors Analysis Section  
- **Technical Risks**: Unsafe serialization, dependency vulnerabilities, code injection, data poisoning
- **Operational Risks**: Supply chain security, licensing compliance, maintenance status
- **Privacy Risks**: Data exposure, model inversion, membership inference

#### Security Checklist Section
- File format analysis (safe/unsafe formats detected)
- Dependency vulnerability scanning results
- License compliance verification
- Code analysis status (when source available)
- Provenance verification (author trustworthiness)

#### Threat Model Section
- Attack vectors with likelihood and impact ratings
- Threat actors and their capabilities  
- Assets at risk identification
- Security controls (preventive, detective, corrective)

### Successful Multi-Model Comparison

```json
{
  "success": true,
  "action": "compare_models",
  "model_names": ["string", "string", ...],
  "models_analyzed": "integer",
  "total_security_issues": "integer",
  "total_compliance_gaps": "integer",
  "report_path": "string",
  "comparison_summary": {
    "common_components_count": "integer",
    "unique_components_per_model": {
      "model_name": "integer",
      ...
    },
    "highest_risk_model": "string"
  }
}
```

**Fields:**
- `success` (boolean): Always true for successful requests
- `action` (string): Echo of the requested action
- `model_names` (array): Echo of the compared model names
- `models_analyzed` (integer): Number of models successfully analyzed
- `total_security_issues` (integer): Aggregate security issues across all models
- `total_compliance_gaps` (integer): Aggregate compliance gaps across all models
- `report_path` (string): Path to the generated comparison HTML report
- `comparison_summary` (object): Summary of comparison analysis
  - `common_components_count` (integer): Components shared by all models
  - `unique_components_per_model` (object): Map of model names to unique component counts
  - `highest_risk_model` (string): Model with the highest security risk

### Error Response

```json
{
  "success": false,
  "error": "string",
  "action": "string"
}
```

**Fields:**
- `success` (boolean): Always false for error responses
- `error` (string): Human-readable error message
- `action` (string): Echo of the requested action (if parseable)

## Error Codes

### Client Errors (4xx equivalent)

#### Invalid Action
```json
{
  "error": "Unknown action: invalid_action",
  "supported_actions": ["analyze_model", "compare_models"]
}
```

#### Missing Required Parameters
```json
{
  "error": "model_name is required for analyze_model action"
}
```

```json
{
  "error": "At least 2 model names required for compare_models action"
}
```

#### Invalid Model Name
```json
{
  "success": false,
  "error": "Model not found: nonexistent/model",
  "action": "analyze_model"
}
```

#### Too Many Models
```json
{
  "success": false,
  "error": "Maximum 10 models allowed for comparison",
  "action": "compare_models"
}
```

### Server Errors (5xx equivalent)

#### Service Unavailable
```json
{
  "success": false,
  "error": "Hugging Face service temporarily unavailable",
  "action": "analyze_model"
}
```

#### Analysis Failed
```json
{
  "success": false,
  "error": "Failed to generate AIBOM for model: microsoft/DialoGPT-medium",
  "action": "analyze_model"
}
```

#### Bedrock Service Error
```json
{
  "success": false,
  "error": "AWS Bedrock service error: Rate limit exceeded",
  "action": "analyze_model"
}
```

## Advanced Configuration

### Session Management

Use session IDs to maintain context across multiple requests:

```bash
# Start a new session
SESSION_ID="analysis-$(date +%s)"

# Use session for related requests
agentcore invoke '{"action": "analyze_model", "model_name": "gpt2"}' --session-id "$SESSION_ID"
agentcore invoke '{"action": "analyze_model", "model_name": "bert-base-uncased"}' --session-id "$SESSION_ID"
```

### Custom Headers

Pass custom headers for additional context:

```bash
agentcore invoke '{"action": "analyze_model", "model_name": "gpt2"}' \
  --headers "X-Analysis-Purpose:security-audit,X-Requester:security-team"
```

### User ID for Authorization

Specify user ID for audit trails:

```bash
agentcore invoke '{"action": "analyze_model", "model_name": "gpt2"}' \
  --user-id "security-analyst-001"
```

## Rate Limiting

### Current Limits
- **Requests per minute**: 60
- **Concurrent requests**: 10
- **Models per comparison**: 10 maximum
- **Report retention**: 30 days

### Rate Limit Headers
The system doesn't currently return rate limit headers, but implements internal throttling.

### Best Practices
- Add delays between requests: `sleep 2`
- Use batch operations when possible
- Monitor CloudWatch metrics for throttling

## Session Management

### Session Lifecycle
1. **Creation**: Automatic on first request or explicit with `--session-id`
2. **Duration**: 30 minutes of inactivity
3. **Cleanup**: Automatic cleanup of expired sessions

### Session Benefits
- **Context Preservation**: Maintains analysis context across requests
- **Performance**: Cached model metadata and analysis results
- **Audit Trail**: Grouped logging and tracing

### Session Example
```bash
# Create named session
SESSION="security-audit-2025"

# Analyze multiple models in same session
agentcore invoke '{"action": "analyze_model", "model_name": "microsoft/DialoGPT-medium"}' -s "$SESSION"
agentcore invoke '{"action": "analyze_model", "model_name": "facebook/blenderbot-400M-distill"}' -s "$SESSION"

# Compare models in same session
agentcore invoke '{"action": "compare_models", "model_names": ["microsoft/DialoGPT-medium", "facebook/blenderbot-400M-distill"]}' -s "$SESSION"
```

## Model Name Formats

### Supported Formats
- **Organization/Model**: `microsoft/DialoGPT-medium`
- **Simple Name**: `gpt2`, `bert-base-uncased`
- **Versioned**: `microsoft/DialoGPT-medium@v1.0`
- **Branch/Tag**: `microsoft/DialoGPT-medium@main`

### Model Discovery
```bash
# Test if model exists
agentcore invoke '{"action": "analyze_model", "model_name": "test-model"}'
```

## Response Time Expectations

### Single Model Analysis (Enhanced Security Analysis)
- **Small models** (<100MB): 45-90 seconds
- **Medium models** (100MB-1GB): 2-4 minutes  
- **Large models** (>1GB): 4-12 minutes

### Multi-Model Comparison (Enhanced Analysis)
- **2-3 models**: 3-8 minutes
- **4-6 models**: 8-20 minutes
- **7-10 models**: 20-40 minutes

### Factors Affecting Performance
- Model size and complexity
- Network latency to Hugging Face
- AWS Bedrock service load (Claude 3 Sonnet processing time)
- Number of components in AIBOM
- **Enhanced analysis processing**: Additional time for detailed security analysis, risk factor assessment, and threat modeling

## Monitoring and Observability

### CloudWatch Metrics
- `AgentInvocations`: Total number of invocations
- `AnalysisLatency`: Time to complete analysis
- `ErrorRate`: Percentage of failed requests
- `ModelCacheHitRate`: Cache efficiency

### X-Ray Tracing
Distributed tracing is automatically enabled for:
- Hugging Face API calls
- AWS Bedrock interactions
- AIBOM generation process
- Report generation

### Log Levels
- **INFO**: Normal operation logs
- **WARN**: Non-critical issues (e.g., model metadata missing)
- **ERROR**: Failed operations
- **DEBUG**: Detailed execution traces (not enabled in production)

## Security Considerations

### Authentication
- Uses AWS IAM for authentication
- AgentCore handles credential management
- No API keys required in requests

### Authorization
- IAM policies control access to AgentCore
- Session-based access control
- User ID tracking for audit

### Data Privacy
- Model metadata cached temporarily (30 minutes)
- Reports stored for 30 days
- No model weights downloaded or stored
- PII scrubbing in logs

### Network Security
- All communications over HTTPS/TLS
- VPC deployment supported
- Security groups restrict access

This API reference provides comprehensive technical details for integrating with and using the AIBOM Agent System effectively.