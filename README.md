# AIBOM Agent System

An intelligent agent system that automatically generates, compares, and analyzes AI Bill of Materials (AIBOMs) for Hugging Face models using AWS AgentCore runtime and AWS Bedrock.

## Overview

This project creates an autonomous agent that:
- Fetches model information from Hugging Face
- Generates AIBOMs using the OWASP AIBOM Generator
- Performs comparative analysis between different models
- Identifies security risks and compliance gaps using AWS Bedrock
- Generates detailed comparison reports with interactive HTML visualizations

## Architecture

- **AWS AgentCore Runtime**: Orchestrates agent execution with ARM64 container deployment
- **OWASP AIBOM Generator**: Generates standardized AIBOMs for ML models
- **Hugging Face Integration**: Fetches model metadata and artifacts
- **AWS Bedrock**: Provides AI-powered security analysis and insights
- **Comparison Engine**: Analyzes differences in model components and risks

## Key Features

- 🤖 **AgentCore Runtime**: Intelligent workflow orchestration with multi-step reasoning
- � ***Automated AIBOM Generation**: Uses OWASP standard for ML model bills of materials
- � **AI-pPowered Analysis**: AWS Bedrock provides intelligent security insights
- 📊 **Comprehensive Reporting**: Interactive HTML reports with visualizations
- ☁️ **Cloud-Native**: Fully deployable to AWS with ARM64 container execution
- 🔒 **Security-First**: Identifies vulnerabilities, unsafe formats, and compliance gaps
- 🌍 **Multi-Region**: Supports deployment to multiple AWS regions

## Quick Start

### Prerequisites

- Python 3.11+
- AWS CLI configured with appropriate permissions
- AWS AgentCore CLI installed

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd aibom-agent-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure
```

### Deployment

```bash
# Configure the agent for your desired region
agentcore configure --name aibom_agent_system --region us-east-1 --create

# Deploy to AWS AgentCore
agentcore deploy --agent aibom_agent_system

# Test the deployment
agentcore invoke '{"action": "analyze_model", "model_name": "microsoft/DialoGPT-medium"}'
```

## Project Structure

```
├── aibom_agent/
│   ├── core/               # Core orchestration logic
│   │   ├── agent_orchestrator.py  # Main orchestration logic
│   │   └── agent_system.py        # Agent system interface
│   ├── services/           # Service implementations
│   │   ├── huggingface_service.py # Hugging Face API integration
│   │   ├── aibom_generator.py     # OWASP AIBOM generation
│   │   ├── bedrock_agent.py       # AWS Bedrock integration
│   │   ├── comparison_engine.py   # Model comparison logic
│   │   └── report_generator.py    # HTML report generation
│   ├── models/             # Data models
│   │   └── analysis_result.py     # Result data structures
│   ├── config/             # Configuration
│   │   └── settings.py            # Application settings
│   └── templates/          # HTML report templates
├── .bedrock_agentcore/     # AgentCore configuration and Dockerfiles
├── main.py                 # AgentCore runtime entrypoint
├── main_simple.py          # Simplified entrypoint for testing
├── cli.py                  # Local development CLI
├── deploy.py               # Deployment automation script
├── test_agent.py           # Agent testing utilities
├── requirements.txt        # Python dependencies
└── reports/                # Generated reports output
```

## Usage

### Single Model Analysis

```bash
# Analyze a single model
agentcore invoke '{"action": "analyze_model", "model_name": "microsoft/DialoGPT-medium"}'
```

**Response:**
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

### Model Comparison

```bash
# Compare multiple models
agentcore invoke '{"action": "compare_models", "model_names": ["microsoft/DialoGPT-medium", "facebook/blenderbot-400M-distill"]}'
```

**Response:**
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

## Multi-Region Deployment

The system supports deployment to multiple AWS regions:

```bash
# Deploy to us-west-2
agentcore configure --name aibom_agent_system_west --region us-west-2 --create
agentcore deploy --agent aibom_agent_system_west

# Deploy to us-east-1
agentcore configure --name aibom_agent_system_east --region us-east-1 --create
agentcore deploy --agent aibom_agent_system_east
```

## Monitoring and Observability

The system includes comprehensive observability:

- **CloudWatch Logs**: Automatic log collection and retention
- **X-Ray Tracing**: Distributed tracing for performance monitoring
- **GenAI Observability Dashboard**: Specialized dashboard for AI workloads
- **Custom Metrics**: Agent performance and usage metrics

```bash
# View logs
aws logs tail /aws/bedrock-agentcore/runtimes/aibom_agent_system-<id>-DEFAULT --follow

# Access GenAI Dashboard
# https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#gen-ai-observability/agent-core
```

## Local Development

For local development and testing:

```bash
# Run local CLI
python cli.py --help

# Test agent locally
python test_agent.py

# Run simple version
python main_simple.py
```

## Configuration

Key configuration options in `aibom_agent/config/settings.py`:

- **AWS Region**: Default region for AWS services
- **Bedrock Agent**: Configuration for AWS Bedrock integration
- **Hugging Face**: API settings and model access
- **Report Generation**: Output paths and template settings

## Troubleshooting

### Common Issues

1. **Ping Endpoint Errors**: These are cosmetic and don't affect functionality
2. **ARM64 Compatibility**: Ensure Docker base images support ARM64
3. **Region Permissions**: Verify AWS permissions in target regions

### Getting Help

- Check CloudWatch logs for detailed error information
- Use `agentcore status` to verify deployment health
- Review the GenAI Observability Dashboard for performance insights

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.