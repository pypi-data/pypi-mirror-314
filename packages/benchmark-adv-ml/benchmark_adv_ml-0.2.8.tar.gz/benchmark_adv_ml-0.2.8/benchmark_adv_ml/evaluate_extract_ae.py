# evaluate_extract_ae.py

import argparse
import os
import pandas as pd
import numpy as np
from tensorflow.keras import models
from .pre_processing import load_prep_for_ae
from .train_autoencoder import save_evaluation_metrics

def main(args):
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Load and preprocess data
    df = load_prep_for_ae(args.data, args.sampleID)
    print(f"Data loaded and preprocessed from {args.data}, shape: {df.shape}")

    # Convert DataFrame to numpy array for model input
    X_data = df.to_numpy()

    # Load the trained models
    encoder = models.load_model(os.path.join(args.model_dir, 'encoder.h5'))
    decoder = models.load_model(os.path.join(args.model_dir, 'decoder.h5'))
    autoencoder_model = models.load_model(os.path.join(args.model_dir, 'autoencoder.h5'))
    print(f"Autoencoder models loaded from {args.model_dir}")

    # Evaluate the autoencoder on the new data
    evaluation = autoencoder_model.evaluate(X_data, X_data, batch_size=args.batch_size, verbose=1)
    print(f"Evaluation on new data: {evaluation}")

    # Save evaluation metrics
    metrics_file_path = os.path.join(args.output_dir, 'evaluation_metrics.txt')
    with open(metrics_file_path, 'w') as metrics_file:
        metrics_file.write(f"Test Loss: {evaluation[0]}\n")
        for metric_name, metric_value in zip(autoencoder_model.metrics_names[1:], evaluation[1:]):
            metrics_file.write(f"{metric_name}: {metric_value}\n")
    print(f"Evaluation metrics saved to {metrics_file_path}")

    # Extract latent features
    latent_features = encoder.predict(X_data, batch_size=args.batch_size, verbose=1)
    num_latent_features = latent_features.shape[1]
    latent_feature_columns = [f'latent_{i+1}' for i in range(num_latent_features)]

    # Save the latent features as a new CSV, keeping track of sampleID
    latent_features_df = pd.DataFrame(latent_features, index=df.index, columns=latent_feature_columns)
    latent_features_path = os.path.join(args.output_dir, 'latent_features.csv')
    latent_features_df.to_csv(latent_features_path)
    print(f"Latent features saved to {latent_features_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate and extract latent features from an autoencoder model.")

    parser.add_argument('--data', type=str, required=True, help='Path to the input CSV file containing the data.')
    parser.add_argument('--sampleID', type=str, default='sampleID', help='SampleID column name in the dataset.')
    parser.add_argument('--model_dir', type=str, required=True, help='Directory where the trained models are saved.')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save the evaluation metrics and latent features.')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size for evaluation and feature extraction.')

    args = parser.parse_args()
    main(args)
