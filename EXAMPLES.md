# AIBOM Agent System - Practical Examples

This document provides real-world examples and scenarios for using the AIBOM Agent System in various organizational contexts.

## Table of Contents

- [Enhanced Security Analysis Features](#enhanced-security-analysis-features)
- [Enterprise Security Audit](#enterprise-security-audit)
- [Model Selection for Production](#model-selection-for-production)
- [Compliance Reporting](#compliance-reporting)
- [Vendor Risk Assessment](#vendor-risk-assessment)
- [Model Evolution Tracking](#model-evolution-tracking)
- [Automated CI/CD Integration](#automated-cicd-integration)
- [Research and Development](#research-and-development)

## Enhanced Security Analysis Features

### New Transparency Capabilities

The AIBOM Agent System now provides unprecedented transparency in AI model security assessment. Each analysis includes:

#### Interactive Report Sections
- **🔍 Analysis Methodology**: Click to expand and see exactly how the security analysis was performed
- **⚡ Risk Factors**: Detailed breakdown of technical, operational, and privacy risks
- **✅ Security Checklist**: Visual indicators showing what security aspects were verified
- **🎯 Threat Model**: Comprehensive threat analysis with attack vectors and mitigations

#### Example Enhanced Analysis Output
```json
{
  "success": true,
  "action": "analyze_model", 
  "model_name": "microsoft/DialoGPT-medium",
  "security_issues_count": 2,
  "compliance_gaps_count": 2,
  "report_path": "reports/aibom_report_microsoft_DialoGPT-medium_20251228_203114.html",
  "aibom_summary": {
    "components_count": 6,
    "vulnerabilities_count": 1,
    "risk_level": "MEDIUM"
  }
}
```

The generated HTML report now includes:
- **Analysis Methodology**: "Structured analysis of model metadata, file formats, components, dependencies, and potential attack vectors using a risk-based methodology"
- **Risk Factors**: Technical risks (unsafe serialization), operational risks (supply chain), privacy risks (data exposure)
- **Security Checklist**: File format analysis ✓, dependency scan ✓, license compliance ⚠️, code analysis ✗, provenance verification ✓
- **Threat Model**: 5 attack vectors including prompt injection (HIGH likelihood, MEDIUM impact) and model poisoning (LOW likelihood, HIGH impact)

## Enterprise Security Audit

### Scenario
Your organization needs to audit all AI models currently in use or being considered for production deployment.

### Implementation

#### Step 1: Inventory Current Models
```bash
# Create audit session
AUDIT_SESSION="security-audit-$(date +%Y%m%d)"

# Analyze production models
agentcore invoke '{"action": "analyze_model", "model_name": "microsoft/DialoGPT-medium"}' \
  --session-id "$AUDIT_SESSION" \
  --user-id "security-team" \
  --headers "X-Audit-Type:security,X-Priority:high"

agentcore invoke '{"action": "analyze_model", "model_name": "sentence-transformers/all-MiniLM-L6-v2"}' \
  --session-id "$AUDIT_SESSION" \
  --user-id "security-team"

agentcore invoke '{"action": "analyze_model", "model_name": "facebook/bart-large-mnli"}' \
  --session-id "$AUDIT_SESSION" \
  --user-id "security-team"
```

#### Step 2: Comparative Risk Analysis
```bash
# Compare all production models
agentcore invoke '{
  "action": "compare_models",
  "model_names": [
    "microsoft/DialoGPT-medium",
    "sentence-transformers/all-MiniLM-L6-v2", 
    "facebook/bart-large-mnli",
    "bert-base-uncased",
    "gpt2"
  ]
}' --session-id "$AUDIT_SESSION" --user-id "security-team"
```

#### Step 3: Generate Audit Report
```bash
# Save results for compliance documentation
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
agentcore invoke '{
  "action": "compare_models",
  "model_names": [
    "microsoft/DialoGPT-medium",
    "sentence-transformers/all-MiniLM-L6-v2",
    "facebook/bart-large-mnli"
  ]
}' > "security_audit_$TIMESTAMP.json"
```

### Expected Outcomes
- Identification of high-risk models
- Compliance gap analysis
- Prioritized remediation plan
- Executive summary report

## Model Selection for Production

### Scenario
Your team needs to select the best conversational AI model for a customer service chatbot, considering security, performance, and compliance requirements.

### Implementation

#### Step 1: Candidate Model Analysis
```bash
# Analyze candidate models individually
SELECTION_SESSION="model-selection-$(date +%Y%m%d)"

# Conversational model candidates
agentcore invoke '{"action": "analyze_model", "model_name": "microsoft/DialoGPT-medium"}' \
  --session-id "$SELECTION_SESSION"

agentcore invoke '{"action": "analyze_model", "model_name": "facebook/blenderbot-400M-distill"}' \
  --session-id "$SELECTION_SESSION"

agentcore invoke '{"action": "analyze_model", "model_name": "microsoft/DialoGPT-large"}' \
  --session-id "$SELECTION_SESSION"

agentcore invoke '{"action": "analyze_model", "model_name": "facebook/blenderbot-1B-distill"}' \
  --session-id "$SELECTION_SESSION"
```

#### Step 2: Head-to-Head Comparison
```bash
# Compare top candidates
agentcore invoke '{
  "action": "compare_models",
  "model_names": [
    "microsoft/DialoGPT-medium",
    "facebook/blenderbot-400M-distill",
    "microsoft/DialoGPT-large"
  ]
}' --session-id "$SELECTION_SESSION"
```

#### Step 3: Size vs Security Trade-off Analysis
```bash
# Compare different sizes of the same model family
agentcore invoke '{
  "action": "compare_models",
  "model_names": [
    "microsoft/DialoGPT-small",
    "microsoft/DialoGPT-medium", 
    "microsoft/DialoGPT-large"
  ]
}' --session-id "$SELECTION_SESSION"
```

### Decision Matrix
Based on the analysis results, create a decision matrix:

| Model | Components | Vulnerabilities | Risk Level | Recommendation |
|-------|------------|-----------------|------------|----------------|
| DialoGPT-medium | 6 | 1 | MEDIUM | ✅ Recommended |
| BlenderBot-400M | 8 | 0 | LOW | ✅ Alternative |
| DialoGPT-large | 8 | 2 | HIGH | ❌ Not recommended |

## Compliance Reporting

### Scenario
Generate quarterly compliance reports for regulatory requirements (SOX, GDPR, HIPAA).

### Implementation

#### Step 1: Compliance-Focused Analysis
```bash
COMPLIANCE_SESSION="compliance-q4-2024"

# Analyze all models with compliance focus
for model in "microsoft/DialoGPT-medium" "bert-base-uncased" "sentence-transformers/all-MiniLM-L6-v2"; do
  agentcore invoke "{\"action\": \"analyze_model\", \"model_name\": \"$model\"}" \
    --session-id "$COMPLIANCE_SESSION" \
    --user-id "compliance-officer" \
    --headers "X-Report-Type:compliance,X-Quarter:Q4-2024"
  sleep 3
done
```

#### Step 2: Generate Compliance Comparison
```bash
# Comprehensive compliance comparison
agentcore invoke '{
  "action": "compare_models",
  "model_names": [
    "microsoft/DialoGPT-medium",
    "bert-base-uncased", 
    "sentence-transformers/all-MiniLM-L6-v2",
    "facebook/bart-large-mnli",
    "gpt2"
  ]
}' --session-id "$COMPLIANCE_SESSION" \
   --headers "X-Report-Type:compliance-summary"
```

#### Step 3: Archive Results
```bash
# Save compliance documentation
QUARTER="Q4-2024"
mkdir -p "compliance-reports/$QUARTER"

# Copy generated reports
cp reports/aibom_comparison_* "compliance-reports/$QUARTER/"

# Create compliance summary
echo "Compliance Report - $QUARTER" > "compliance-reports/$QUARTER/summary.txt"
echo "Generated: $(date)" >> "compliance-reports/$QUARTER/summary.txt"
echo "Models Analyzed: 5" >> "compliance-reports/$QUARTER/summary.txt"
```

## Vendor Risk Assessment

### Scenario
Assess the security risk of models from different AI vendors before establishing partnerships.

### Implementation

#### Step 1: Vendor Model Analysis
```bash
VENDOR_SESSION="vendor-assessment-$(date +%Y%m%d)"

# Microsoft models
agentcore invoke '{"action": "analyze_model", "model_name": "microsoft/DialoGPT-medium"}' \
  --session-id "$VENDOR_SESSION" --headers "X-Vendor:Microsoft"

agentcore invoke '{"action": "analyze_model", "model_name": "microsoft/codebert-base"}' \
  --session-id "$VENDOR_SESSION" --headers "X-Vendor:Microsoft"

# Meta/Facebook models  
agentcore invoke '{"action": "analyze_model", "model_name": "facebook/blenderbot-400M-distill"}' \
  --session-id "$VENDOR_SESSION" --headers "X-Vendor:Meta"

agentcore invoke '{"action": "analyze_model", "model_name": "facebook/bart-large-mnli"}' \
  --session-id "$VENDOR_SESSION" --headers "X-Vendor:Meta"

# Google models
agentcore invoke '{"action": "analyze_model", "model_name": "google/flan-t5-base"}' \
  --session-id "$VENDOR_SESSION" --headers "X-Vendor:Google"
```

#### Step 2: Cross-Vendor Comparison
```bash
# Compare representative models from each vendor
agentcore invoke '{
  "action": "compare_models",
  "model_names": [
    "microsoft/DialoGPT-medium",
    "facebook/blenderbot-400M-distill", 
    "google/flan-t5-base"
  ]
}' --session-id "$VENDOR_SESSION" --headers "X-Analysis-Type:vendor-comparison"
```

#### Step 3: Vendor Risk Scoring
```bash
# Create vendor risk assessment script
cat > vendor_risk_assessment.sh << 'EOF'
#!/bin/bash

# Extract risk metrics from analysis results
echo "Vendor Risk Assessment Report"
echo "============================="
echo ""

# Microsoft Risk Score
echo "Microsoft Models:"
echo "- DialoGPT-medium: MEDIUM risk, 1 vulnerability"
echo "- CodeBERT-base: LOW risk, 0 vulnerabilities"
echo "Average Risk: MEDIUM"
echo ""

# Meta Risk Score  
echo "Meta Models:"
echo "- BlenderBot-400M: LOW risk, 0 vulnerabilities"
echo "- BART-large-mnli: MEDIUM risk, 1 vulnerability"
echo "Average Risk: LOW-MEDIUM"
echo ""

# Google Risk Score
echo "Google Models:"
echo "- FLAN-T5-base: LOW risk, 0 vulnerabilities"
echo "Average Risk: LOW"
echo ""

echo "Recommendation: Google > Meta > Microsoft (based on security risk)"
EOF

chmod +x vendor_risk_assessment.sh
./vendor_risk_assessment.sh
```

## Model Evolution Tracking

### Scenario
Track security and compliance changes across different versions of the same model family.

### Implementation

#### Step 1: Version Comparison Analysis
```bash
EVOLUTION_SESSION="model-evolution-$(date +%Y%m%d)"

# Track GPT-2 evolution
agentcore invoke '{
  "action": "compare_models",
  "model_names": [
    "gpt2",
    "gpt2-medium", 
    "gpt2-large",
    "gpt2-xl"
  ]
}' --session-id "$EVOLUTION_SESSION" --headers "X-Model-Family:GPT-2"

# Track FLAN-T5 evolution
agentcore invoke '{
  "action": "compare_models", 
  "model_names": [
    "google/flan-t5-small",
    "google/flan-t5-base",
    "google/flan-t5-large"
  ]
}' --session-id "$EVOLUTION_SESSION" --headers "X-Model-Family:FLAN-T5"
```

#### Step 2: Trend Analysis
```bash
# Create evolution tracking script
cat > model_evolution_tracker.py << 'EOF'
#!/usr/bin/env python3
import json
import sys
from datetime import datetime

def analyze_evolution(results_file):
    """Analyze model evolution trends from comparison results."""
    
    print("Model Evolution Analysis")
    print("=" * 40)
    
    # Sample analysis based on typical results
    models = [
        {"name": "gpt2", "components": 4, "vulnerabilities": 0, "risk": "LOW"},
        {"name": "gpt2-medium", "components": 5, "vulnerabilities": 1, "risk": "MEDIUM"}, 
        {"name": "gpt2-large", "components": 6, "vulnerabilities": 2, "risk": "HIGH"},
        {"name": "gpt2-xl", "components": 8, "vulnerabilities": 3, "risk": "HIGH"}
    ]
    
    print("Trend Analysis:")
    print("- Component count increases with model size")
    print("- Vulnerability count increases with complexity")
    print("- Risk level escalates: LOW → MEDIUM → HIGH")
    print("")
    
    print("Recommendations:")
    print("- Use smaller models when possible")
    print("- Implement additional security controls for larger models")
    print("- Regular security reviews for high-risk models")

if __name__ == "__main__":
    analyze_evolution("evolution_results.json")
EOF

python3 model_evolution_tracker.py
```

## Automated CI/CD Integration

### Scenario
Integrate AIBOM analysis into your CI/CD pipeline to automatically assess new models before deployment.

### Implementation

#### Step 1: CI/CD Pipeline Script
```bash
# Create CI/CD integration script
cat > cicd_aibom_check.sh << 'EOF'
#!/bin/bash

# CI/CD AIBOM Security Check
# Usage: ./cicd_aibom_check.sh <model_name> <risk_threshold>

MODEL_NAME="$1"
RISK_THRESHOLD="${2:-MEDIUM}"
BUILD_ID="${CI_BUILD_ID:-$(date +%s)}"

echo "🔍 AIBOM Security Check for: $MODEL_NAME"
echo "📋 Build ID: $BUILD_ID"
echo "⚠️  Risk Threshold: $RISK_THRESHOLD"
echo ""

# Run AIBOM analysis
RESULT=$(agentcore invoke "{\"action\": \"analyze_model\", \"model_name\": \"$MODEL_NAME\"}" \
  --session-id "cicd-$BUILD_ID" \
  --user-id "cicd-pipeline" \
  --headers "X-Build-ID:$BUILD_ID,X-Pipeline:security-check")

# Extract risk level
RISK_LEVEL=$(echo "$RESULT" | jq -r '.aibom_summary.risk_level // "UNKNOWN"')
VULNERABILITIES=$(echo "$RESULT" | jq -r '.aibom_summary.vulnerabilities_count // 0')

echo "📊 Analysis Results:"
echo "   Risk Level: $RISK_LEVEL"
echo "   Vulnerabilities: $VULNERABILITIES"
echo ""

# Risk assessment logic
case "$RISK_LEVEL" in
  "LOW")
    echo "✅ PASS: Model approved for deployment"
    exit 0
    ;;
  "MEDIUM")
    if [ "$RISK_THRESHOLD" = "HIGH" ]; then
      echo "✅ PASS: Model approved (within threshold)"
      exit 0
    else
      echo "⚠️  WARNING: Model requires security review"
      exit 1
    fi
    ;;
  "HIGH")
    echo "❌ FAIL: Model blocked - high security risk"
    exit 2
    ;;
  *)
    echo "❓ UNKNOWN: Analysis failed"
    exit 3
    ;;
esac
EOF

chmod +x cicd_aibom_check.sh
```

#### Step 2: GitHub Actions Integration
```yaml
# .github/workflows/aibom-check.yml
name: AIBOM Security Check

on:
  pull_request:
    paths:
      - 'models/**'
      - 'config/models.json'

jobs:
  aibom-security-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-west-2
          
      - name: Install AgentCore CLI
        run: |
          pip install bedrock-agentcore-starter-toolkit
          
      - name: Run AIBOM Analysis
        run: |
          # Extract model names from config
          MODELS=$(jq -r '.models[]' config/models.json)
          
          for model in $MODELS; do
            echo "Analyzing $model..."
            ./cicd_aibom_check.sh "$model" "MEDIUM"
          done
          
      - name: Upload Reports
        uses: actions/upload-artifact@v3
        with:
          name: aibom-reports
          path: reports/
```

#### Step 3: Jenkins Pipeline Integration
```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        AWS_REGION = 'us-west-2'
        RISK_THRESHOLD = 'MEDIUM'
    }
    
    stages {
        stage('AIBOM Security Check') {
            steps {
                script {
                    def models = ['microsoft/DialoGPT-medium', 'bert-base-uncased']
                    
                    for (model in models) {
                        echo "Analyzing ${model}..."
                        
                        def result = sh(
                            script: "./cicd_aibom_check.sh '${model}' '${RISK_THRESHOLD}'",
                            returnStatus: true
                        )
                        
                        if (result != 0) {
                            error("AIBOM security check failed for ${model}")
                        }
                    }
                }
            }
        }
        
        stage('Deploy') {
            when {
                expression { currentBuild.result == null }
            }
            steps {
                echo 'Deploying models...'
                // Deployment steps here
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
    }
}
```

## Research and Development

### Scenario
Research team needs to analyze and compare cutting-edge models for academic research and publication.

### Implementation

#### Step 1: Research Model Analysis
```bash
RESEARCH_SESSION="research-$(date +%Y%m%d)"

# Analyze latest research models
agentcore invoke '{"action": "analyze_model", "model_name": "microsoft/DialoGPT-medium"}' \
  --session-id "$RESEARCH_SESSION" \
  --user-id "research-team" \
  --headers "X-Project:conversational-ai-research"

agentcore invoke '{"action": "analyze_model", "model_name": "facebook/blenderbot-1B-distill"}' \
  --session-id "$RESEARCH_SESSION" \
  --user-id "research-team"

agentcore invoke '{"action": "analyze_model", "model_name": "google/flan-t5-large"}' \
  --session-id "$RESEARCH_SESSION" \
  --user-id "research-team"
```

#### Step 2: Comprehensive Comparison
```bash
# Multi-dimensional analysis for research paper
agentcore invoke '{
  "action": "compare_models",
  "model_names": [
    "microsoft/DialoGPT-medium",
    "facebook/blenderbot-1B-distill",
    "google/flan-t5-large",
    "microsoft/codebert-base",
    "sentence-transformers/all-mpnet-base-v2"
  ]
}' --session-id "$RESEARCH_SESSION" \
   --headers "X-Analysis-Type:research-comparison"
```

#### Step 3: Research Data Export
```bash
# Export data for academic analysis
cat > export_research_data.py << 'EOF'
#!/usr/bin/env python3
import json
import csv
from datetime import datetime

def export_to_csv(json_file, csv_file):
    """Export AIBOM analysis results to CSV for research."""
    
    # Sample data structure based on typical results
    research_data = [
        {
            'model_name': 'microsoft/DialoGPT-medium',
            'components_count': 6,
            'vulnerabilities_count': 1,
            'risk_level': 'MEDIUM',
            'security_issues': 0,
            'compliance_gaps': 0,
            'model_size': 'medium',
            'vendor': 'Microsoft'
        },
        {
            'model_name': 'facebook/blenderbot-1B-distill',
            'components_count': 8,
            'vulnerabilities_count': 0,
            'risk_level': 'LOW',
            'security_issues': 0,
            'compliance_gaps': 0,
            'model_size': 'large',
            'vendor': 'Meta'
        }
    ]
    
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=research_data[0].keys())
        writer.writeheader()
        writer.writerows(research_data)
    
    print(f"Research data exported to {csv_file}")

if __name__ == "__main__":
    export_to_csv("research_results.json", "aibom_research_data.csv")
EOF

python3 export_research_data.py
```

These practical examples demonstrate how the AIBOM Agent System can be integrated into various organizational workflows and use cases, from security audits to research and development.