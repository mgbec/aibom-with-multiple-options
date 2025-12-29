#!/bin/bash

# Setup IAM permissions for AIBOM Agent System in us-west-2
# This script creates and attaches the necessary IAM policy for S3 access

set -e

REGION="us-west-2"
ROLE_NAME="AmazonBedrockAgentCoreSDKRuntime-us-west-2-b8fafb0d44"
POLICY_NAME="AIBOMReportsS3AccessWest"
POLICY_FILE="iam-policy-us-west-2.json"
BUCKET_NAME="aibom-reports-339712707840-us-west-2"

echo "🔧 Setting up IAM permissions for AIBOM Agent System in $REGION"

# Check if policy file exists
if [ ! -f "$POLICY_FILE" ]; then
    echo "❌ Policy file $POLICY_FILE not found!"
    exit 1
fi

echo "📋 Creating IAM policy: $POLICY_NAME"

# Create the IAM policy
POLICY_ARN=$(aws iam create-policy \
    --policy-name "$POLICY_NAME" \
    --policy-document file://"$POLICY_FILE" \
    --description "S3 access policy for AIBOM reports in us-west-2" \
    --query 'Policy.Arn' \
    --output text 2>/dev/null || \
    aws iam get-policy \
    --policy-arn "arn:aws:iam::339712707840:policy/$POLICY_NAME" \
    --query 'Policy.Arn' \
    --output text)

echo "✅ Policy ARN: $POLICY_ARN"

echo "🔗 Attaching policy to role: $ROLE_NAME"

# Attach the policy to the role
aws iam attach-role-policy \
    --role-name "$ROLE_NAME" \
    --policy-arn "$POLICY_ARN"

echo "✅ Policy attached successfully!"

echo "🧪 Testing S3 bucket access..."

# Test bucket access
aws s3 ls "s3://$BUCKET_NAME/" --region "$REGION" || echo "⚠️  Bucket access test failed - this is expected if using role credentials"

echo "🎉 IAM setup complete!"
echo ""
echo "Next steps:"
echo "1. The AgentCore runtime should now have access to the S3 bucket"
echo "2. Test the agent with: agentcore invoke --payload '{\"action\":\"analyze_model\",\"model_name\":\"sentence-transformers/all-MiniLM-L6-v2\"}'"
echo "3. Check that reports are uploaded to S3 successfully"