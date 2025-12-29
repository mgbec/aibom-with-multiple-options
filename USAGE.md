# AIBOM Agent System - Usage Guide

This guide provides comprehensive examples and use cases for the AIBOM Agent System, covering single model analysis, multi-model comparisons, and advanced scenarios.

## Table of Contents

- [Basic Usage](#basic-usage)
- [Single Model Analysis](#single-model-analysis)
- [Multi-Model Comparison](#multi-model-comparison)
- [Advanced Use Cases](#advanced-use-cases)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [Report Analysis](#report-analysis)

## Basic Usage

### Prerequisites

Ensure your agent is deployed and accessible:

```bash
# Check agent status
agentcore status

# List available agents
agentcore configure list
```

### Basic Invocation Pattern

```bash
agentcore invoke '{"action": "<action_type>", ...parameters}'
```

## Single Model Analysis

### Analyze a Conversational Model

```bash
agentcore invoke '{"action": "analyze_model", "model_name": "microsoft/DialoGPT-medium"}'
```

**Expected Response:**
```json
{
  "success": true,
  "action": "analyze_model",
  "model_name": "microsoft/DialoGPT-medium",
  "security_issues_count": 0,
  "compliance_gaps_count": 0,
  "report_path": "reports/aibom_report_microsoft_DialoGPT-medium_20251228_162108.html",
  "aibom_summary": {
    "components_count": 6,
    "vulnerabilities_count": 1,
    "risk_level": "MEDIUM"
  }
}
```

### Analyze a Text Generation Model

```bash
agentcore invoke '{"action": "analyze_model", "model_name": "gpt2"}'
```

### Analyze an Embedding Model

```bash
agentcore invoke '{"action": "analyze_model", "model_name": "BAAI/bge-m3"}'
```

### Analyze a Large Language Model

```bash
agentcore invoke '{"action": "analyze_model", "model_name": "meta-llama/Llama-2-7b-hf"}'
```

## Multi-Model Comparison

### Compare Two Conversational Models

```bash
agentcore invoke '{
  "action": "compare_models", 
  "model_names": [
    "microsoft/DialoGPT-medium", 
    "facebook/blenderbot-400M-distill"
  ]
}'
```

**Expected Response:**
```json
{
  "success": true,
  "action": "compare_models",
  "model_names": ["microsoft/DialoGPT-medium", "facebook/blenderbot-400M-distill"],
  "models_analyzed": 2,
  "total_security_issues": 0,
  "total_compliance_gaps": 0,
  "report_path": "reports/aibom_comparison_microsoft_DialoGPT-medium_vs_facebook_blenderbot-400M-distill_20251228_163638.html",
  "comparison_summary": {
    "common_components_count": 5,
    "unique_components_per_model": {
      "microsoft/DialoGPT-medium": 1,
      "facebook/blenderbot-400M-distill": 3
    },
    "highest_risk_model": "microsoft/DialoGPT-medium"
  }
}
```

### Compare Multiple Text Generation Models

```bash
agentcore invoke '{
  "action": "compare_models", 
  "model_names": [
    "gpt2", 
    "gpt2-medium", 
    "gpt2-large"
  ]
}'
```

### Compare Different Model Types

```bash
agentcore invoke '{
  "action": "compare_models", 
  "model_names": [
    "bert-base-uncased",
    "roberta-base",
    "distilbert-base-uncased"
  ]
}'
```

### Compare Embedding Models

```bash
agentcore invoke '{
  "action": "compare_models", 
  "model_names": [
    "sentence-transformers/all-MiniLM-L6-v2",
    "sentence-transformers/all-mpnet-base-v2",
    "BAAI/bge-m3"
  ]
}'
```

## Advanced Use Cases

### Large-Scale Model Comparison (5+ Models)

```bash
agentcore invoke '{
  "action": "compare_models", 
  "model_names": [
    "microsoft/DialoGPT-small",
    "microsoft/DialoGPT-medium",
    "microsoft/DialoGPT-large",
    "facebook/blenderbot-400M-distill",
    "facebook/blenderbot-1B-distill",
    "google/flan-t5-small"
  ]
}'
```

### Cross-Domain Model Analysis

Compare models from different domains to understand component diversity:

```bash
agentcore invoke '{
  "action": "compare_models", 
  "model_names": [
    "microsoft/DialoGPT-medium",     # Conversational
    "sentence-transformers/all-MiniLM-L6-v2",  # Embedding
    "facebook/bart-large-mnli",      # Classification
    "t5-small",                      # Text-to-text
    "microsoft/codebert-base"        # Code understanding
  ]
}'
```

### Security-Focused Analysis

Analyze models known to have different security profiles:

```bash
agentcore invoke '{
  "action": "compare_models", 
  "model_names": [
    "gpt2",                    # Older model
    "microsoft/DialoGPT-medium",  # Newer conversational
    "facebook/opt-125m"        # Recent open model
  ]
}'
```

### Model Size Comparison

Compare models of different sizes within the same family:

```bash
agentcore invoke '{
  "action": "compare_models", 
  "model_names": [
    "google/flan-t5-small",
    "google/flan-t5-base", 
    "google/flan-t5-large"
  ]
}'
```

## Error Handling

### Invalid Model Name

```bash
agentcore invoke '{"action": "analyze_model", "model_name": "nonexistent/model"}'
```

**Expected Response:**
```json
{
  "success": false,
  "error": "Model not found: nonexistent/model",
  "action": "analyze_model"
}
```

### Missing Required Parameters

```bash
agentcore invoke '{"action": "analyze_model"}'
```

**Expected Response:**
```json
{
  "error": "model_name is required for analyze_model action"
}
```

### Invalid Action

```bash
agentcore invoke '{"action": "invalid_action", "model_name": "gpt2"}'
```

**Expected Response:**
```json
{
  "error": "Unknown action: invalid_action",
  "supported_actions": ["analyze_model", "compare_models"]
}
```

### Insufficient Models for Comparison

```bash
agentcore invoke '{"action": "compare_models", "model_names": ["gpt2"]}'
```

**Expected Response:**
```json
{
  "error": "At least 2 model names required for compare_models action"
}
```

## Best Practices

### 1. Model Selection

**Good Practices:**
- Use specific model versions when available
- Choose models from the same domain for meaningful comparisons
- Include a mix of model sizes for comprehensive analysis

**Examples:**
```bash
# Good: Specific versions
agentcore invoke '{"action": "compare_models", "model_names": ["gpt2", "gpt2-medium"]}'

# Better: Domain-specific comparison
agentcore invoke '{"action": "compare_models", "model_names": ["bert-base-uncased", "roberta-base", "distilbert-base-uncased"]}'
```

### 2. Batch Processing

For analyzing multiple models individually:

```bash
# Analyze each model separately for detailed individual reports
for model in "gpt2" "bert-base-uncased" "t5-small"; do
  echo "Analyzing $model..."
  agentcore invoke "{\"action\": \"analyze_model\", \"model_name\": \"$model\"}"
  sleep 2  # Rate limiting
done
```

### 3. Session Management

Use consistent session IDs for related analyses:

```bash
# Use session ID for related analyses
SESSION_ID="analysis-session-$(date +%Y%m%d)"
agentcore invoke '{"action": "analyze_model", "model_name": "gpt2"}' --session-id "$SESSION_ID"
```

### 4. Report Organization

Organize your analysis workflow:

```bash
# Create analysis timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Single model analysis
agentcore invoke '{"action": "analyze_model", "model_name": "microsoft/DialoGPT-medium"}' > "analysis_single_$TIMESTAMP.json"

# Comparison analysis
agentcore invoke '{"action": "compare_models", "model_names": ["microsoft/DialoGPT-medium", "facebook/blenderbot-400M-distill"]}' > "analysis_comparison_$TIMESTAMP.json"
```

## Report Analysis

### Understanding Single Model Reports

Key metrics to focus on:

- **components_count**: Number of components in the AIBOM
- **vulnerabilities_count**: Known security vulnerabilities
- **risk_level**: Overall risk assessment (LOW, MEDIUM, HIGH, CRITICAL)
- **security_issues_count**: Number of security concerns identified
- **compliance_gaps_count**: Compliance-related issues

### Enhanced Security Analysis Sections

The reports now include detailed interactive sections:

#### 🔍 Analysis Methodology
- **Approach**: Explanation of the security assessment methodology
- **Data Sources**: What information was analyzed
- **Analysis Steps**: Step-by-step process followed
- **Tools Used**: Security analysis tools and techniques employed
- **Coverage**: Scope of the analysis performed
- **Limitations**: Any constraints or assumptions made

#### ⚡ Risk Factors Analysis
- **Technical Risks**: 
  - Unsafe serialization (pickle files, etc.)
  - Dependency vulnerabilities
  - Code injection risks
  - Data poisoning potential
- **Operational Risks**:
  - Supply chain security
  - Licensing compliance
  - Maintenance and support status
- **Privacy Risks**:
  - Data exposure potential
  - Model inversion vulnerabilities
  - Membership inference attacks

#### ✅ Security Checklist
- **File Format Analysis**: Safe vs unsafe formats detected
- **Dependency Scan**: Vulnerability scanning results
- **License Compliance**: Legal compliance verification
- **Code Analysis**: Source code security review (when available)
- **Provenance Verification**: Author and source trustworthiness

#### 🎯 Threat Model
- **Attack Vectors**: Specific threats with likelihood and impact ratings
- **Threat Actors**: Potential attackers and their capabilities
- **Assets at Risk**: What could be compromised
- **Security Controls**: Preventive, detective, and corrective measures

### Understanding Comparison Reports

Key comparison metrics:

- **common_components_count**: Shared components across models
- **unique_components_per_model**: Model-specific components
- **highest_risk_model**: Model with the highest security risk
- **total_security_issues**: Aggregate security issues across all models

### Report File Locations

Reports are saved in the `reports/` directory with descriptive names:

- Single model: `aibom_report_{model_name}_{timestamp}.html`
- Comparison: `aibom_comparison_{model1}_vs_{model2}_{timestamp}.html`

### Accessing Reports

```bash
# List recent reports
ls -la reports/ | head -10

# Open latest report (macOS)
open reports/$(ls -t reports/ | head -1)

# Open latest report (Linux)
xdg-open reports/$(ls -t reports/ | head -1)
```

## Monitoring and Debugging

### Check Agent Logs

```bash
# Real-time log monitoring
aws logs tail /aws/bedrock-agentcore/runtimes/aibom_agent_system_west-xJwUxW9sGq-DEFAULT --follow

# Check recent logs
aws logs tail /aws/bedrock-agentcore/runtimes/aibom_agent_system_west-xJwUxW9sGq-DEFAULT --since 1h
```

### Performance Monitoring

```bash
# Check agent status
agentcore status

# View GenAI Observability Dashboard
# https://console.aws.amazon.com/cloudwatch/home?region=us-west-2#gen-ai-observability/agent-core
```

## Common Use Case Scenarios

### 1. Model Selection for Production

Compare candidate models for production deployment:

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

### 2. Security Audit

Analyze models for security compliance:

```bash
# Individual security analysis
agentcore invoke '{"action": "analyze_model", "model_name": "microsoft/DialoGPT-medium"}'

# Comparative security analysis
agentcore invoke '{
  "action": "compare_models", 
  "model_names": [
    "microsoft/DialoGPT-medium",
    "facebook/blenderbot-400M-distill"
  ]
}'
```

### 3. Model Evolution Tracking

Track changes across model versions:

```bash
agentcore invoke '{
  "action": "compare_models", 
  "model_names": [
    "microsoft/DialoGPT-small",
    "microsoft/DialoGPT-medium", 
    "microsoft/DialoGPT-large"
  ]
}'
```

### 4. Vendor Comparison

Compare models from different vendors:

```bash
agentcore invoke '{
  "action": "compare_models", 
  "model_names": [
    "microsoft/DialoGPT-medium",  # Microsoft
    "facebook/blenderbot-400M-distill",  # Meta
    "google/flan-t5-base"  # Google
  ]
}'
```

This comprehensive usage guide covers the most common scenarios and best practices for using the AIBOM Agent System effectively.