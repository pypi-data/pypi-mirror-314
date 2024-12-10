# Benchmark-Adv-ML

**Benchmark-Adv-ML** is a Python package designed to facilitate advanced benchmarking and analysis of machine learning models. It provides comprehensive pipelines for model stability evaluation, autoencoder training, and survival clustering analysis, enabling users to evaluate model performance, generate predictions, and visualize results through various plots, including AUC curves, feature importance charts, and Kaplan-Meier survival plots.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Benchmark Machine Learning Models](#benchmark-machine-learning-models)
  - [Train Autoencoder Model](#train-autoencoder-model)
  - [Survival Clustering Analysis](#survival-clustering-analysis)
- [Command-Line Arguments](#command-line-arguments)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

## Features

- **Model Stability Evaluation**: Automatically runs multiple machine learning models (Logistic Regression, Support Vector Classifier, Random Forest Classifier) across multiple runs to assess stability and performance.
- **Autoencoder Training**: Implements an autoencoder for dimensionality reduction and feature extraction, customizable with various hyperparameters.
- **Survival Clustering Analysis**: Performs clustering on patient features and integrates clinical data to generate Kaplan-Meier survival plots and log-rank tests.
- **Prediction and Metrics Generation**: Generates and saves predictions, feature importance scores, and various performance metrics for each model and run.
- **Aggregation of Results**: Aggregates results across runs and models for comprehensive analysis, facilitating comparison and evaluation.
- **Visualization Tools**: Generates plots including AUC curves, AUC box plots, feature importance charts, radar charts for model performance comparison, and survival analysis plots.

## Installation

You can install the package directly from PyPI:

```bash
pip install benchmark-adv-ml
```
Alternatively, install from source:

```bash
git clone https://github.com/yourusername/benchmark-adv-ml.git
cd benchmark-adv-ml
pip install .
```

## Useage
The package provides a command-line interface (CLI) for ease of use. Below are examples of how to use each component.

### Download example data
```bash
wget https://github.com/VatsalPatel18/benchmark-adv-ml/blob/master/temp_data.csv
```

### Benchmark Machine Learning Models
Run the benchmark ML pipeline to evaluate model stability across multiple runs.

```bash
benchmark-adv-ml benchmark --data ./your_dataset.csv --output ./final_results --prelim_output ./prelim_results --n_runs 10 --seed 42
```
### Train Autoencoder Model
Train and evaluate an autoencoder model for feature extraction.

```bash
benchmark-adv-ml autoencoder --data ./your_dataset.csv --sampleID 'PatientID' --output_dir ./final_results --prelim_output ./prelim_results --latent_dim 10 --epochs 50 --batch_size 32 --validation_split 0.1 --test_size 0.2 --seed 42
```

### Survival Clustering Analysis
```bash
benchmark-adv-ml survival_clustering --data_path ./latent_features.csv --clinical_df_path ./clinical_data.csv --save_dir ./final_results
```

## Command-Line Arguments

### Common Arguments
- `--data`: Path to the existing CSV file containing the dataset.
- `--output`: Directory to save the final results and plots.
- `--prelim_output`: Directory to save the preliminary results (predictions).
- `--seed`: Seed for random state (default is 42).

### Benchmark Command Arguments

- `--target`: Target column name in the dataset (default: 'label').
- `--n_runs`: Number of runs for model stability evaluation (default: 20).

### Autoencoder Command Arguments

- `--sampleID`: Column name representing the sample or patient ID (default: 'sampleID').
- `--latent_dim`: Dimensionality of the latent space (default: input_dim // 8).
- `--epochs`: Number of training epochs (default: 50).
- `--batch_size`: Training batch size (default: 32).
- `--validation_split`: Proportion of training data to use as validation set (default: 0.1).
- `--test_size`: Proportion of data to use as test set (default: 0.2).
- `--early_stopping`: Enable early stopping (use flag to activate).
- `--patience`: Patience for early stopping (default: 5).
- `--checkpoint`: Enable model checkpointing (use flag to activate).

### Survival Clustering Command Arguments

- `--data_path`: Path to the CSV file containing patient features.
- `--clinical_df_path`: Path to the CSV file containing clinical data.
- `--save_dir`: Directory to save the results.

## Dependencies

- Python 3.11+
- numpy
- pandas
- scikit-learn
- matplotlib
- seaborn
- tensorflow
- lifelines
- yellowbrick

## License 
This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. See the LICENSE file for details.

## Author
Vatsal Patel - VatsalPatel18