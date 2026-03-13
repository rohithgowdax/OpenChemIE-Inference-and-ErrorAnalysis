# OpenServer - OpenChemie SMILES Recognition Pipeline

A data processing and inference pipeline for chemical structure recognition, converting CDXML chemistry files to images and predicting molecular SMILES strings using AWS SageMaker.

## Overview

This project implements an end-to-end machine learning pipeline for:

- Converting chemical structure files (CDXML) to image format (PNG)
- Extracting molecular SMILES strings from chemistry data
- Running inference on chemical structure images using a pre-trained neural network
- Evaluating prediction accuracy against ground truth labels

## Project Structure

```
├── data_pipeline.py              # CDXML to PNG conversion & SMILES extraction
├── inference.py                  # AWS SageMaker inference for SMILES prediction
├── error_analysis.ipynb          # Error analysis and visualization notebook
├── utility.ipynb                 # Utility functions and analysis helpers
├── evaluation_results.csv        # Inference results with predictions and targets
├── target.csv                    # Target dataset with images and SMILES
├── classification_report.png     # Classification metrics visualization
├── image_for_testing.png         # Sample image for testing
├── correct/                      # Directory containing correctly predicted images
├── incorrect/                    # Directory containing incorrectly predicted images
├── images/                       # Processed chemical structure images
└── .env                          # Environment configuration (AWS credentials)
```

## Features

### Data Pipeline (`data_pipeline.py`)

- Converts CDXML (ChemDraw XML) chemistry files to PNG images
- Extracts SMILES (Simplified Molecular Input Line Entry System) strings from molecular structures
- Filters invalid fragments and removes invalid molecules
- Generates structured CSV dataset with image paths and SMILES notation
- Handles batch processing with error handling for malformed inputs

### Inference (`inference.py`)

- Loads target dataset from CSV
- Sends images to AWS SageMaker endpoint for SMILES prediction
- Converts SMILES to InChI format for validation
- Compares predictions against ground truth labels
- Generates evaluation results with match status
- Base64 encodes images for API transmission

### Analysis Notebooks

- **error_analysis.ipynb**: Analyzes prediction errors and mismatches
- **utility.ipynb**: Helper functions and exploratory data analysis

## Dependencies

The project requires the following Python packages:

- `rdkit` - Chemistry informatics toolkit
- `boto3` - AWS SDK for SageMaker inference
- `pandas` - Data manipulation and analysis
- `cdxml_converter` - CDXML to image conversion
- `python-dotenv` - Environment variable management

## Usage

### 1. Generate Dataset from CDXML Files

```bash
python data_pipeline.py
```

This will:

- Convert CDXML files to PNG format
- Extract SMILES strings
- Generate `dataset.csv` with image paths and corresponding SMILES

### 2. Run Inference

```bash
python inference.py
```

This will:

- Read target images from `target.csv`
- Send images to the SageMaker endpoint
- Validate predictions using InChI conversion
- Output results to `evaluation_results.csv`

### 3. Analyze Results

Open and run the analysis notebooks:

- `error_analysis.ipynb` - Detailed error analysis and visualization
- `utility.ipynb` - Additional analysis and utilities

## Output

### Evaluation Results (`evaluation_results.csv`)

Columns:

- `image` - Path to the input chemical structure image
- `target` - Ground truth SMILES string
- `prediction` - Predicted SMILES string from the model
- `match` - Boolean indicating if prediction matches target

## Key Components

### Chemical Structure Processing

- RDKit for molecular operations
- CDXMLConverter for format transformation
- SVGRasterizer for image generation

### AWS Integration

- SageMaker for model inference
- Base64 encoding for image transmission
- Automatic error handling and retry logic

### Validation

- InChI (International Chemical Identifier) conversion for chemical validation
- SMILES canonicalization for comparison
- Fragment filtering for data quality

## Performance Metrics

The `classification_report.png` file contains visual summaries of model performance metrics.

## Error Handling

Both scripts include comprehensive error handling:

- Invalid molecular structures are skipped
- Missing or corrupted images are logged
- AWS API errors are caught and reported
- Failed conversions are tracked for debugging

## Notes

- CDXML files should be in the configured source directory
- Images are processed in batch mode for efficiency
- The SageMaker endpoint must be active for inference
- Chemical structures are filtered to remove invalid fragments
