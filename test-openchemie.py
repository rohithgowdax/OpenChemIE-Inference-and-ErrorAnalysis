"""
Test script for OpenChemIE SageMaker endpoint.
Run: python test_endpoint.py <image_path>

Install: pip install boto3
"""

import dotenv
import sys
import json
import base64
import boto3
import os
dotenv.load_dotenv()

# Configuration
REGION = "ap-south-1"
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
ENDPOINT_NAME = "openchemie-3"
# INFERENCE_COMPONENT_NAME = "Opechemie-20260128-101723"  # Check SageMaker console if this doesn't work



def test_endpoint(image_path, what="both"):
    """Test the OpenChemIE endpoint with an image."""

    session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION
)
    runtime = session.client('sagemaker-runtime', region_name=REGION)

    # Read and encode image
    print(f"Reading image: {image_path}")
    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    image_b64 = base64.b64encode(image_bytes).decode('utf-8')
    print(f"Image size: {len(image_bytes)} bytes")

    # Create request payload
    payload = {
        "image": image_b64,
        "what": what,
        "fast": True
    }

    print(f"\nInvoking endpoint: {ENDPOINT_NAME}")
    print(f"Mode: {what}")
    print("Please wait...")

    # Invoke endpoint
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        # InferenceComponentName=INFERENCE_COMPONENT_NAME,
        ContentType='application/json',
        Body=json.dumps(payload)
    )

    result = json.loads(response['Body'].read().decode('utf-8'))

    print("\n" + "=" * 50)
    print("RESULTS")
    print("=" * 50)

    if result.get('smiles'):
        print(f"\nMOLECULES: count: {len(result.get('smiles'))}")
        for i, smiles in enumerate(result['smiles'], 1):
            print(f"  {i}. {smiles}")

    if result.get('reaction_smiles'):
        print("\nREACTIONS:")
        for i, rxn in enumerate(result['reaction_smiles'], 1):
            print(f"  {i}. {rxn.get('reactants', '')} -> {rxn.get('products', '')}")

    print("=" * 50)
    print("\nRaw JSON:")
    print(json.dumps(result, indent=2))
    print("")
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_endpoint.py <image_path> [smiles|reactions|both]")
        sys.exit(1)

    image_path = sys.argv[1]
    what = sys.argv[2] if len(sys.argv) > 2 else "both"
    test_endpoint(image_path, what)