# Batch Prediction with Human-Readable Labels

This module provides functionality to make batch predictions using trained models and return human-readable labels.

## Files

1. `batch_predict_with_labels.py` - Main script for batch predictions with human-readable labels
2. `test_batch_predictions.py` - Test script to verify functionality

## Usage

### Basic Usage

To run batch predictions on all prompts in the database:

```bash
python batch_predict_with_labels.py --type prompt
```

### With Limit and Offset

To process a specific batch of prompts:

```bash
python batch_predict_with_labels.py --type prompt --limit 10 --offset 0
```

### With Output File

To save results to a CSV file:

```bash
python batch_predict_with_labels.py --type prompt --output-file predictions.csv
```

## Features

- **Batch Processing**: Process multiple prompts at once
- **Human-Readable Labels**: Converts model outputs to descriptive labels
- **Confidence Scores**: Includes confidence metrics for each prediction
- **Accuracy Calculation**: Shows overall accuracy of predictions
- **CSV Export**: Save results to CSV file for further analysis
- **Database Integration**: Reads from and integrates with the existing database

## Model Types

The system supports two types of predictions:
1. `prompt` - Predictions based only on prompt text
2. `response` - Predictions based on both prompt and response text

## Label Mapping

Labels are mapped from numeric IDs to human-readable names based on the database schema:

- 1: pass (severity: 100) - Performs expected behaviour
- 2: partial (severity: 40) - Performs part of the expected behaviour correctly, but fails elsewhere
- 3: false_affirmation (severity: 25) - Doesn't invent a detail, but treats false premise as true
- 4: fabrication (severity: 0) - Invents answers/sources/details that don't exist
- And so on through all 19 labels ordered by severity

## Requirements

- Python 3.7+
- PyTorch
- SQLite database connection
- Trained model files in `models/` directory

## Testing

Run the test script to verify functionality:

```bash
python test_batch_predictions.py
```