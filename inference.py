'''
Script used for Inference
'''
import os
import json
import csv
import base64
import boto3
import dotenv
import pandas as pd
from rdkit import Chem
from rdkit.Chem import inchi
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')

dotenv.load_dotenv()

REGION = "ap-south-1"
ENDPOINT_NAME = "openchemie-3"

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

DATASET_CSV = "target.csv"
OUTPUT_CSV = "evaluation_results.csv"


def smiles_to_inchi(smiles):
    """Convert SMILES to InChI for Validation"""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            return inchi.MolToInchi(mol)
    except:
        pass
    return None


def run_inference(runtime, image_path):

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    image_b64 = base64.b64encode(image_bytes).decode()

    payload = {
        "image": image_b64,
        "what": "smiles",
        "fast": True
    }

    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType="application/json",
        Body=json.dumps(payload)
    )

    result = json.loads(response["Body"].read().decode())

    if result.get("smiles"):
        return result["smiles"][0]

    return None


def main():

    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGION
    )

    runtime = session.client("sagemaker-runtime")

    df = pd.read_csv(DATASET_CSV)

    rows = []

    for idx, row in df.iterrows():

        image_path = row["image"]
        target_smiles = row["smiles"]

        if not os.path.exists(image_path):
            print("Missing image:", image_path)
            continue

        print("Processing:", image_path)

        pred_smiles = run_inference(runtime, image_path)

        target_inchi = smiles_to_inchi(target_smiles)
        pred_inchi = smiles_to_inchi(pred_smiles) if pred_smiles else None

        match = target_inchi == pred_inchi

        rows.append([
            image_path,
            target_smiles,
            pred_smiles,
            match
        ])

    with open(OUTPUT_CSV, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "image",
            "target",
            "prediction",
            "match"
        ])

        writer.writerows(rows)

    print("\nSaved results to:", OUTPUT_CSV)


if __name__ == "__main__":
    main()