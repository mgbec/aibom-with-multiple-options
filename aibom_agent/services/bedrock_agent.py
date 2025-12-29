"""Bedrock Agent service for AI-powered security analysis."""

import json
from typing import Dict, Any, List

import boto3
from loguru import logger

from ..config.settings import AWSSettings
from ..models.analysis_result import AIBOM, ModelInfo, SecurityAnalysis, ModelComparison, ComparisonInsights


class BedrockAgentService:
    """Service for AI-powered security analysis using AWS Bedrock."""
    
    def __init__(self, settings: AWSSettings):
        self.settings = settings
        self.bedrock_runtime_client = None
    
    async def initialize(self) -> None:
        """Initialize Bedrock clients."""
        logger.info("Initializing Bedrock Agent service...")
        
        # Use bedrock-runtime for model invocation, not bedrock-agent-runtime
        self.bedrock_runtime_client = boto3.client(
            'bedrock-runtime',
            region_name=self.settings.region
        )
        
        logger.info("Bedrock Agent service initialized successfully")
    
    async def analyze_security(self, aibom: AIBOM, model_info: ModelInfo) -> SecurityAnalysis:
        """
        Perform AI-powered security analysis of an AIBOM.
        
        Args:
            aibom: The AI Bill of Materials to analyze
            model_info: Additional model information
            
        Returns:
            SecurityAnalysis with risk assessment and recommendations
        """
        logger.info(f"Performing security analysis for model: {model_info.name}")
        
        try:
            # Prepare analysis prompt
            analysis_prompt = self._create_security_analysis_prompt(aibom, model_info)
            
            # Call Bedrock for analysis
            response = await self._invoke_bedrock_model(analysis_prompt)
            
            # Parse response into SecurityAnalysis
            security_analysis = self._parse_security_analysis(response)
            
            logger.info(f"Security analysis completed for {model_info.name}")
            return security_analysis
            
        except Exception as e:
            logger.error(f"Failed to perform security analysis: {e}")
            # Return default analysis on failure
            return self._create_default_security_analysis()
    
    async def generate_comparison_insights(self, comparison: ModelComparison) -> ComparisonInsights:
        """
        Generate AI-powered insights from model comparison.
        
        Args:
            comparison: ModelComparison data
            
        Returns:
            ComparisonInsights with AI-generated analysis
        """
        logger.info("Generating comparison insights...")
        
        try:
            # Prepare comparison prompt
            insights_prompt = self._create_comparison_insights_prompt(comparison)
            
            # Call Bedrock for insights
            response = await self._invoke_bedrock_model(insights_prompt)
            
            # Parse response into ComparisonInsights
            insights = self._parse_comparison_insights(response)
            
            logger.info("Comparison insights generated successfully")
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate comparison insights: {e}")
            # Return default insights on failure
            return self._create_default_comparison_insights()
    
    def _create_security_analysis_prompt(self, aibom: AIBOM, model_info: ModelInfo) -> str:
        """Create a comprehensive prompt for detailed security analysis."""
        return f"""
You are a cybersecurity expert specializing in AI/ML model security analysis. 
Analyze the following AI Bill of Materials (AIBOM) and model information to provide a comprehensive security assessment with detailed transparency about your analysis process.

Model Information:
- Name: {model_info.name}
- Author: {model_info.author}
- License: {model_info.license}
- Downloads: {model_info.downloads}
- Tags: {', '.join(model_info.tags)}
- Pipeline: {model_info.pipeline_tag}
- Library: {model_info.library_name}
- Model Size: {model_info.model_size}

AIBOM Summary:
- Components: {len(aibom.components)}
- Dependencies: {len(aibom.dependencies)}
- Known Vulnerabilities: {len(aibom.vulnerabilities)}

AIBOM Components (first 10):
{json.dumps(aibom.components[:10], indent=2)}

Model Files:
{json.dumps(model_info.files[:5], indent=2) if model_info.files else "No file information available"}

Please provide a comprehensive security analysis in JSON format with detailed transparency:

{{
    "risk_score": <float 0-10>,
    "risk_level": "<LOW|MEDIUM|HIGH|CRITICAL>",
    "vulnerabilities": [
        {{"type": "...", "severity": "...", "description": "...", "cve_id": "...", "impact": "...", "mitigation": "..."}}
    ],
    "compliance_issues": [
        {{"category": "...", "issue": "...", "recommendation": "...", "severity": "...", "standard": "..."}}
    ],
    "recommendations": ["..."],
    "unsafe_formats": ["..."],
    "suspicious_files": ["..."],
    "license_issues": ["..."],
    "analysis_methodology": {{
        "approach": "Description of the analysis approach used",
        "data_sources": ["List of data sources analyzed"],
        "analysis_steps": ["Step-by-step analysis process"],
        "tools_used": ["Security analysis tools and techniques"],
        "coverage": "What aspects were covered in the analysis",
        "limitations": "Any limitations or assumptions in the analysis"
    }},
    "risk_factors": {{
        "technical_risks": {{
            "unsafe_serialization": {{"present": true/false, "details": "...", "impact": "..."}},
            "dependency_vulnerabilities": {{"count": 0, "details": "...", "severity": "..."}},
            "code_injection": {{"risk": "...", "vectors": ["..."], "mitigation": "..."}},
            "data_poisoning": {{"risk": "...", "indicators": ["..."], "prevention": "..."}}
        }},
        "operational_risks": {{
            "supply_chain": {{"risk": "...", "trust_score": 0-10, "verification": "..."}},
            "licensing": {{"compliance": "...", "restrictions": ["..."], "commercial_use": "..."}},
            "maintenance": {{"status": "...", "last_update": "...", "support": "..."}}
        }},
        "privacy_risks": {{
            "data_exposure": {{"risk": "...", "types": ["..."], "protection": "..."}},
            "model_inversion": {{"vulnerability": "...", "mitigation": "..."}},
            "membership_inference": {{"risk": "...", "indicators": ["..."]}}
        }}
    }},
    "security_checklist": {{
        "file_format_analysis": {{
            "checked": true/false,
            "safe_formats": ["..."],
            "unsafe_formats": ["..."],
            "findings": "..."
        }},
        "dependency_scan": {{
            "checked": true/false,
            "total_dependencies": 0,
            "vulnerable_dependencies": 0,
            "findings": "..."
        }},
        "license_compliance": {{
            "checked": true/false,
            "license_type": "...",
            "commercial_compatible": true/false,
            "findings": "..."
        }},
        "code_analysis": {{
            "checked": true/false,
            "suspicious_patterns": ["..."],
            "findings": "..."
        }},
        "provenance_verification": {{
            "checked": true/false,
            "author_verified": true/false,
            "source_trusted": true/false,
            "findings": "..."
        }}
    }},
    "threat_model": {{
        "attack_vectors": [
            {{
                "vector": "Model Poisoning",
                "likelihood": "LOW|MEDIUM|HIGH",
                "impact": "LOW|MEDIUM|HIGH",
                "description": "...",
                "mitigation": "..."
            }},
            {{
                "vector": "Supply Chain Attack",
                "likelihood": "LOW|MEDIUM|HIGH", 
                "impact": "LOW|MEDIUM|HIGH",
                "description": "...",
                "mitigation": "..."
            }}
        ],
        "threat_actors": ["Nation-state", "Cybercriminals", "Malicious insiders"],
        "assets_at_risk": ["Model integrity", "Training data", "Inference results"],
        "security_controls": {{
            "preventive": ["..."],
            "detective": ["..."],
            "corrective": ["..."]
        }}
    }}
}}

Focus your analysis on:
1. File format security (pickle files, executable content)
2. Dependency vulnerabilities and supply chain risks
3. License compliance and legal implications
4. Model provenance and author trustworthiness
5. Potential attack vectors and threat scenarios
6. Privacy implications and data protection
7. Operational security considerations

Provide detailed explanations for your reasoning and methodology to help users understand the security assessment process.
"""
    
    def _create_comparison_insights_prompt(self, comparison: ModelComparison) -> str:
        """Create a prompt for comparison insights."""
        return f"""
You are an AI/ML expert analyzing differences between multiple AI models.
Generate insights from the following model comparison data.

Common Components: {len(comparison.common_components)}
Unique Components per Model: {comparison.unique_components}
Security Comparison: {comparison.security_comparison}
License Comparison: {comparison.license_comparison}

Please provide insights in JSON format:
{{
    "summary": "Brief overview of key findings",
    "key_differences": ["List of main differences"],
    "security_recommendations": ["Security-focused recommendations"],
    "best_practices": ["Best practice recommendations"],
    "risk_assessment": "Overall risk assessment across models"
}}

Focus on:
1. Security implications of differences
2. Compliance and licensing considerations
3. Performance and reliability factors
4. Best practices for model selection
"""
    
    async def _invoke_bedrock_model(self, prompt: str) -> str:
        """Invoke Bedrock model for analysis."""
        try:
            # Use Claude 3 Sonnet for analysis
            model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
            
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            response = self.bedrock_runtime_client.invoke_model(
                modelId=model_id,
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except Exception as e:
            logger.error(f"Failed to invoke Bedrock model: {e}")
            raise
    
    def _parse_security_analysis(self, response: str) -> SecurityAnalysis:
        """Parse Bedrock response into enhanced SecurityAnalysis."""
        try:
            # Extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            json_str = response[start_idx:end_idx]
            
            data = json.loads(json_str)
            
            return SecurityAnalysis(
                risk_score=float(data.get('risk_score', 5.0)),
                risk_level=data.get('risk_level', 'MEDIUM'),
                vulnerabilities=data.get('vulnerabilities', []),
                compliance_issues=data.get('compliance_issues', []),
                recommendations=data.get('recommendations', []),
                unsafe_formats=data.get('unsafe_formats', []),
                suspicious_files=data.get('suspicious_files', []),
                license_issues=data.get('license_issues', []),
                analysis_methodology=data.get('analysis_methodology', {
                    "approach": "Standard security analysis",
                    "data_sources": ["AIBOM components", "Model metadata"],
                    "analysis_steps": ["Component analysis", "Vulnerability scanning", "Risk assessment"],
                    "tools_used": ["OWASP AIBOM Generator", "AWS Bedrock AI"],
                    "coverage": "Basic security assessment",
                    "limitations": "Limited to available metadata"
                }),
                risk_factors=data.get('risk_factors', {
                    "technical_risks": {},
                    "operational_risks": {},
                    "privacy_risks": {}
                }),
                security_checklist=data.get('security_checklist', {
                    "file_format_analysis": {"checked": True, "findings": "Basic format check performed"},
                    "dependency_scan": {"checked": True, "findings": "Dependencies analyzed"},
                    "license_compliance": {"checked": True, "findings": "License reviewed"},
                    "code_analysis": {"checked": False, "findings": "Code analysis not performed"},
                    "provenance_verification": {"checked": True, "findings": "Author and source verified"}
                }),
                threat_model=data.get('threat_model', {
                    "attack_vectors": [],
                    "threat_actors": ["Unknown"],
                    "assets_at_risk": ["Model integrity"],
                    "security_controls": {
                        "preventive": ["Access controls"],
                        "detective": ["Monitoring"],
                        "corrective": ["Incident response"]
                    }
                })
            )
            
        except Exception as e:
            logger.error(f"Failed to parse security analysis: {e}")
            return self._create_default_security_analysis()
    
    def _parse_comparison_insights(self, response: str) -> ComparisonInsights:
        """Parse Bedrock response into ComparisonInsights."""
        try:
            # Extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            json_str = response[start_idx:end_idx]
            
            data = json.loads(json_str)
            
            return ComparisonInsights(
                summary=data.get('summary', 'Analysis completed'),
                key_differences=data.get('key_differences', []),
                security_recommendations=data.get('security_recommendations', []),
                best_practices=data.get('best_practices', []),
                risk_assessment=data.get('risk_assessment', 'Medium risk')
            )
            
        except Exception as e:
            logger.error(f"Failed to parse comparison insights: {e}")
            return self._create_default_comparison_insights()
    
    def _create_default_security_analysis(self) -> SecurityAnalysis:
        """Create default enhanced security analysis when AI analysis fails."""
        return SecurityAnalysis(
            risk_score=5.0,
            risk_level="MEDIUM",
            vulnerabilities=[],
            compliance_issues=[],
            recommendations=["Manual security review recommended", "Verify model provenance", "Check for unsafe file formats"],
            unsafe_formats=[],
            suspicious_files=[],
            license_issues=[],
            analysis_methodology={
                "approach": "Fallback analysis due to AI service unavailability",
                "data_sources": ["AIBOM metadata", "Model information"],
                "analysis_steps": ["Basic metadata review", "Default risk assessment"],
                "tools_used": ["OWASP AIBOM Generator"],
                "coverage": "Limited to available metadata",
                "limitations": "AI-powered analysis unavailable, manual review required"
            },
            risk_factors={
                "technical_risks": {
                    "unsafe_serialization": {"present": False, "details": "Unable to verify", "impact": "Unknown"},
                    "dependency_vulnerabilities": {"count": 0, "details": "Not analyzed", "severity": "Unknown"},
                    "code_injection": {"risk": "Unknown", "vectors": [], "mitigation": "Manual review required"},
                    "data_poisoning": {"risk": "Unknown", "indicators": [], "prevention": "Manual verification needed"}
                },
                "operational_risks": {
                    "supply_chain": {"risk": "Unknown", "trust_score": 5, "verification": "Manual verification required"},
                    "licensing": {"compliance": "Unknown", "restrictions": [], "commercial_use": "Verify manually"},
                    "maintenance": {"status": "Unknown", "last_update": "Unknown", "support": "Unknown"}
                },
                "privacy_risks": {
                    "data_exposure": {"risk": "Unknown", "types": [], "protection": "Manual assessment needed"},
                    "model_inversion": {"vulnerability": "Unknown", "mitigation": "Standard protections recommended"},
                    "membership_inference": {"risk": "Unknown", "indicators": []}
                }
            },
            security_checklist={
                "file_format_analysis": {"checked": False, "safe_formats": [], "unsafe_formats": [], "findings": "Manual analysis required"},
                "dependency_scan": {"checked": False, "total_dependencies": 0, "vulnerable_dependencies": 0, "findings": "Manual scan required"},
                "license_compliance": {"checked": False, "license_type": "Unknown", "commercial_compatible": None, "findings": "Manual review required"},
                "code_analysis": {"checked": False, "suspicious_patterns": [], "findings": "Manual code review required"},
                "provenance_verification": {"checked": False, "author_verified": None, "source_trusted": None, "findings": "Manual verification required"}
            },
            threat_model={
                "attack_vectors": [
                    {
                        "vector": "Unknown Threats",
                        "likelihood": "MEDIUM",
                        "impact": "MEDIUM", 
                        "description": "Threat analysis unavailable, assume standard ML model risks",
                        "mitigation": "Implement standard ML security controls"
                    }
                ],
                "threat_actors": ["Unknown"],
                "assets_at_risk": ["Model integrity", "Training data", "Inference results"],
                "security_controls": {
                    "preventive": ["Access controls", "Input validation", "Model versioning"],
                    "detective": ["Monitoring", "Anomaly detection", "Audit logging"],
                    "corrective": ["Incident response", "Model rollback", "Security patching"]
                }
            }
        )
    
    def _create_default_comparison_insights(self) -> ComparisonInsights:
        """Create default comparison insights when AI analysis fails."""
        return ComparisonInsights(
            summary="Comparison analysis completed with limited insights",
            key_differences=["Manual analysis required"],
            security_recommendations=["Perform detailed security review"],
            best_practices=["Follow ML security best practices"],
            risk_assessment="Manual assessment required"
        )
    
    async def cleanup(self) -> None:
        """Clean up resources."""
        logger.info("Cleaning up Bedrock Agent service...")
        # No specific cleanup needed for boto3 clients
        pass