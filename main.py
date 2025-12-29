#!/usr/bin/env python3
"""
AIBOM Agent System - AgentCore Runtime Implementation

An intelligent agent system that automatically generates, compares, and analyzes 
AI Bill of Materials (AIBOMs) for Hugging Face models using AWS AgentCore runtime.

Reports are securely stored in S3 with pre-signed URLs for access.
"""

import asyncio
import os
from typing import Dict, Any, List

from bedrock_agentcore.runtime import BedrockAgentCoreApp
from loguru import logger

# Initialize AgentCore app
app = BedrockAgentCoreApp()

# Global orchestrator instance - will be initialized on first use
orchestrator = None


def get_orchestrator(session_id: str):
    """Get or create orchestrator instance."""
    global orchestrator
    if orchestrator is None:
        from aibom_agent.core.agent_orchestrator import AIBOMAgentOrchestrator
        from aibom_agent.config.settings import Settings
        
        settings = Settings.load()
        
        # Set S3 bucket if not configured
        if not settings.aws.s3_bucket:
            settings.aws.s3_bucket = "aibom-reports-339712707840-us-west-2"
            logger.info(f"Using default S3 bucket: {settings.aws.s3_bucket}")
        
        # Ensure region matches bucket region
        if settings.aws.s3_bucket and "us-west-2" in settings.aws.s3_bucket:
            settings.aws.region = "us-west-2"
            logger.info(f"Set AWS region to us-west-2 to match S3 bucket")
        elif settings.aws.s3_bucket and "us-east-1" in settings.aws.s3_bucket:
            settings.aws.region = "us-east-1"
            logger.info(f"Set AWS region to us-east-1 to match S3 bucket")
        
        orchestrator = AIBOMAgentOrchestrator(settings, session_id)
    return orchestrator


@app.entrypoint
def invoke(payload: Dict[str, Any], context) -> Dict[str, Any]:
    """
    Main AgentCore entrypoint for AIBOM analysis requests.
    
    Expected payload formats:
    
    Single model analysis:
    {
        "action": "analyze_model",
        "model_name": "microsoft/DialoGPT-medium"
    }
    
    Model comparison:
    {
        "action": "compare_models", 
        "model_names": ["microsoft/DialoGPT-medium", "facebook/blenderbot-400M-distill"]
    }
    
    Args:
        payload: Request payload with action and parameters
        context: AgentCore request context with session_id
        
    Returns:
        Dictionary with analysis results and report information
    """
    
    try:
        # Get orchestrator
        session_id = getattr(context, 'session_id', 'default-session')
        orch = get_orchestrator(session_id)
        
        # Extract action and parameters
        action = payload.get("action")
        
        if action == "analyze_model":
            model_name = payload.get("model_name")
            if not model_name:
                return {"error": "model_name is required for analyze_model action"}
            
            logger.info(f"Starting single model analysis for: {model_name}")
            result = asyncio.run(orch.analyze_single_model(model_name))
            
            # Parse report paths (local|s3 format)
            local_path, s3_path = None, None
            if result.report_path:
                if "|" in result.report_path:
                    local_path, s3_path = result.report_path.split("|", 1)
                else:
                    local_path = result.report_path
            
            response = {
                "success": True,
                "action": "analyze_model",
                "model_name": model_name,
                "security_issues_count": result.security_issues_count,
                "compliance_gaps_count": result.compliance_gaps_count,
                "report_local_path": local_path,
                "report_s3_path": s3_path,
                "report_access": "Both local and S3" if s3_path else "Local file only",
                "aibom_summary": {
                    "components_count": len(result.aibom.components),
                    "vulnerabilities_count": len(result.aibom.vulnerabilities),
                    "risk_level": result.security_analysis.risk_level
                }
            }
            
            # Keep backward compatibility
            response["report_path"] = local_path
            
            return response
            
        elif action == "compare_models":
            model_names = payload.get("model_names", [])
            if not model_names or len(model_names) < 2:
                return {"error": "At least 2 model names required for compare_models action"}
            
            logger.info(f"Starting comparative analysis for: {model_names}")
            result = asyncio.run(orch.compare_models(model_names))
            
            # Parse report paths (local|s3 format)
            local_path, s3_path = None, None
            if result.report_path:
                if "|" in result.report_path:
                    local_path, s3_path = result.report_path.split("|", 1)
                else:
                    local_path = result.report_path
            
            response = {
                "success": True,
                "action": "compare_models",
                "model_names": model_names,
                "models_analyzed": len(model_names),
                "total_security_issues": result.security_issues_count,
                "total_compliance_gaps": result.compliance_gaps_count,
                "report_local_path": local_path,
                "report_s3_path": s3_path,
                "report_access": "Both local and S3" if s3_path else "Local file only",
                "comparison_summary": {
                    "common_components_count": len(result.comparison.common_components),
                    "unique_components_per_model": {
                        name: len(components) 
                        for name, components in result.comparison.unique_components.items()
                    },
                    "highest_risk_model": max(
                        result.individual_results,
                        key=lambda r: r.security_analysis.risk_score
                    ).model_name
                }
            }
            
            # Keep backward compatibility
            response["report_path"] = local_path
            
            return response
            
        else:
            return {
                "error": f"Unknown action: {action}",
                "supported_actions": ["analyze_model", "compare_models"]
            }
            
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return {
            "success": False,
            "error": str(e),
            "action": payload.get("action", "unknown")
        }


@app.ping
def health_check():
    """Custom health check for the AIBOM Agent System."""
    try:
        # Basic health check - verify we can import core modules
        from aibom_agent.config.settings import Settings
        settings = Settings.load()
        
        # Return a simple string that AgentCore can handle
        return "healthy"
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return "unhealthy"


if __name__ == "__main__":
    # For local development
    app.run()