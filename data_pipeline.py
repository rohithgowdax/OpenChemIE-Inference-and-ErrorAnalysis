"""Script used to generate Dataset """

import os
import glob
import csv
from rdkit import Chem
from cdxml_converter.converter import convert_cdxml
from cdxml_converter.svg_rasterizer import SVGRasterizer
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')


base = "/Users/rohithgowda/Downloads/sample_cdxml_files"
image_dir = os.path.join(base, "dataset/images")

os.makedirs(image_dir, exist_ok=True)

dataset = []

rasterizer_ctx = SVGRasterizer()

with rasterizer_ctx as rasterizer:

    files = glob.glob(os.path.join(base, "*.cdxml"))

    for f in files:

        name = os.path.splitext(os.path.basename(f))[0]
        img_path = os.path.join(image_dir, name + ".png")

        # ---------- Convert CDXML → PNG ----------
        try:
            convert_cdxml(
                f,
                output_dir=image_dir,
                formats=["png"],
                _rasterizer=rasterizer
            )
        except Exception as e:
            print("Image conversion failed:", name)
            continue
        
        with open(f) as file:
                cdxml_string = file.read()

        # ---------- Extract SMILES ----------

        all_smiles = []

        try:
            mols = Chem.MolsFromCDXML(cdxml_string)

            if mols:
                for mol in mols:

                    if mol is None:
                        continue
                    try:    
                        smi = Chem.MolToSmiles(mol, canonical=True)
                    except: continue
                    parts = smi.split('.')
                    
                    # remove '*, C, O' fragments

                    filtered = [p for p in parts if len(p) > 1]
                    all_smiles.extend(filtered)

        except Exception as e:
            print("SMILES extraction failed:", name)

        # ---------- If no valid SMILES → remove image ----------
        if not all_smiles:
            print("No valid SMILES, deleting image:", name)


            if os.path.isfile(img_path):
                os.remove(img_path)

            continue

        all_smiles = list(set(all_smiles))

        dataset.append([
            f"images/{name}.png",
            ".".join(all_smiles)
        ])

# ---------- Write CSV ----------
csv_path = os.path.join(base, "dataset.csv")

with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["image", "smiles"])
    writer.writerows(dataset)

print("Dataset saved:", csv_path)