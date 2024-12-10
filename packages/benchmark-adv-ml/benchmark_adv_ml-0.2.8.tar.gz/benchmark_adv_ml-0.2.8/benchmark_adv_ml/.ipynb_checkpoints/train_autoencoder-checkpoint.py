# train_autoencoder.py

import argparse
import json
import os
import pandas as pd
import numpy as np
import math
from .autoencoder import Autoencoder
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from .pre_processing import load_prep_for_ae, split_data_for_ae  

def save_training_log(history, output_dir):
    """
    Saves the training log to a text file.

    :param history: History object from model training.
    :param output_dir: Directory to save the log file.
    """
    log_file_path = os.path.join(output_dir, 'training_log.txt')
    with open(log_file_path, 'w') as log_file:
        log_file.write("Epoch, Loss, Val_Loss\n")
        for epoch in range(len(history.history['loss'])):
            log_file.write(f"{epoch + 1}, {history.history['loss'][epoch]}, {history.history.get('val_loss', [None])[epoch]}\n")
    print(f"Training log saved to {log_file_path}")

def save_evaluation_metrics(evaluation, output_dir):
    """
    Saves the evaluation metrics to a text file.

    :param evaluation: List of evaluation metrics.
    :param output_dir: Directory to save the metrics file.
    """
    metrics_file_path = os.path.join(output_dir, 'evaluation_metrics.txt')
    with open(metrics_file_path, 'w') as metrics_file:
        metrics_file.write(f"Test Loss: {evaluation}\n")
    print(f"Evaluation metrics saved to {metrics_file_path}")

def generate_temp_config(input_dim, latent_dim=None):
    """
    Generates a temporary encoder configuration based on the input dimension.

    :param input_dim: Integer, dimensionality of the input features.
    :param latent_dim: Integer, dimensionality of the latent space. Defaults to input_dim // 8.
    :return: List of dictionaries, each representing a layer configuration.
    """
    if latent_dim is None:
        latent_dim = max(1, input_dim // 8)  # Ensure latent_dim is always set to a positive integer
    config = [
        {
            "units": input_dim,
            "activation": "relu",
            "dropout": 0.25
        },
        {
            "units": max(1, math.ceil(input_dim / 4)),
            "activation": "relu",
            "dropout": 0.25
        },
        {
            "units": latent_dim,
            "activation": "relu",
            "dropout": 0.25
        }
    ]
    return config


def main(args):
    # Create output directories if they don't exist
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(args.prelim_output, exist_ok=True)

    # Load and preprocess data
    df = load_prep_for_ae(args.data,args.sampleID)
    print(f"Data loaded and preprocessed from {args.data}, shape: {df.shape}")

    # Split data into training and testing sets
    split_data_dict = split_data_for_ae(df, test_size=args.test_size, random_state=args.seed)
    X_train = split_data_dict['train']['X']
    X_test = split_data_dict['test']['X']

    print(f"Training data shape: {X_train.shape}, Testing data shape: {X_test.shape}")

    # Optionally, split training data into training and validation sets
    if args.validation_split > 0:
        val_split = int(X_train.shape[0] * (1 - args.validation_split))
        x_val = X_train[val_split:]
        X_train = X_train[:val_split]
        print(f"Validation data shape: {x_val.shape}")
    else:
        x_val = None

    # Generate encoder configuration dynamically if not provided
    if args.encoder_config:
        with open(args.encoder_config, 'r') as f:
            encoder_config = json.load(f)
    else:
        encoder_config = generate_temp_config(input_dim=X_train.shape[1], latent_dim=args.latent_dim)
        print(f"Generated temporary encoder configuration: {encoder_config}")


    # Initialize Autoencoder
    autoencoder = Autoencoder(
        encoder_config=generate_temp_config(input_dim=X_train.shape[1], latent_dim=10),
        input_dim=X_train.shape[1],
        latent_dim=args.latent_dim if args.latent_dim else max(1, X_train.shape[1] // 8),
        activation=args.activation,
        optimizer=args.optimizer,
        loss=args.loss,
        metrics=args.metrics
    )

    # Compile the model
    autoencoder.compile()
    print("Autoencoder compiled.")

    # Define callbacks
    callbacks = []
    if args.early_stopping:
        early_stop = EarlyStopping(monitor='val_loss', patience=args.patience, restore_best_weights=True)
        callbacks.append(early_stop)
        print("EarlyStopping callback added.")

    if args.checkpoint:
        checkpoint_path = os.path.join(args.output_dir, 'best_autoencoder.h5')
        checkpoint = ModelCheckpoint(filepath=checkpoint_path, monitor='val_loss', save_best_only=True, verbose=1)
        callbacks.append(checkpoint)
        print(f"ModelCheckpoint callback added. Saving to {checkpoint_path}")

    # Train the model
    history = autoencoder.train(
        x_train=X_train,
        x_val=x_val,
        epochs=args.epochs,
        batch_size=args.batch_size,
        callbacks=callbacks,
        verbose=1
    )
    print("Model training completed.")

    # Save the training log
    save_training_log(history, args.output_dir)

    # Evaluate the model
    evaluation = autoencoder.evaluate(X_test)
    print(f"Evaluation on test data: {evaluation}")

    # Save evaluation metrics
    save_evaluation_metrics(evaluation, args.output_dir)

    # Save models
    autoencoder.save_models(args.output_dir)

    # Prepare and save preliminary results for plotting
    prelim_results_path = os.path.join(args.prelim_output, 'prelim_results.csv')
    X_test_predictions = autoencoder.autoencoder.predict(X_test)
    prelim_results_df = pd.DataFrame({
        'True_Labels': np.squeeze(X_test.values).flatten(),
        'Predicted_Scores': np.squeeze(X_test_predictions).flatten()
    })

    prelim_results_df.to_csv(prelim_results_path, index=False)
    print(f"Preliminary results saved to {prelim_results_path}")

    # Extract latent features from X_train
    df_feature = df.to_numpy()
    print(df.index)
    latent_features = autoencoder.extract_latent_features(df_feature, batch_size=args.batch_size, verbose=1)
    # Save the latent features as a new CSV
    latent_features_df = pd.DataFrame(latent_features, index=df.index)
    latent_features_path = os.path.join(args.output_dir, 'latent_features.csv')
    latent_features_df.to_csv(latent_features_path)
    print(f"Latent features saved to {latent_features_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train and evaluate an autoencoder model.")

    parser.add_argument('--data', type=str, required=True, help='Path to the input CSV file containing the data.')
    parser.add_argument('--target', type=str, default='label', help='Target column name in the dataset.')
    parser.add_argument('--sampleID', type=str, default='sampleID', help='SampleID column name in the dataset.')    
    parser.add_argument('--encoder_config', type=str, help='Path to the JSON file defining encoder architecture. If not provided, a temporary config will be generated.')
    parser.add_argument('--latent_dim', type=int, help='Dimensionality of the latent space. If not specified, defaults to input_dim // 8.')
    parser.add_argument('--activation', type=str, default='relu', help='Activation function to use in hidden layers.')
    parser.add_argument('--optimizer', type=str, default='adam', help='Optimizer to use for training.')
    parser.add_argument('--loss', type=str, default='mse', help='Loss function to use.')
    parser.add_argument('--metrics', nargs='+', default=['mse'], help='List of metrics to evaluate.')
    parser.add_argument('--test_size', type=float, default=0.2, help='Proportion of data to use as test set.')
    parser.add_argument('--validation_split', type=float, default=0.1, help='Proportion of training data to use as validation set.')
    parser.add_argument('--epochs', type=int, default=50, help='Number of training epochs.')
    parser.add_argument('--batch_size', type=int, default=32, help='Training batch size.')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save the final results and models.')
    parser.add_argument('--prelim_output', type=str, required=True, help='Directory to save the preliminary results (predictions).')
    parser.add_argument('--early_stopping', action='store_true', help='Enable early stopping.')
    parser.add_argument('--patience', type=int, default=5, help='Patience for early stopping.')
    parser.add_argument('--checkpoint', action='store_true', help='Enable model checkpointing.')
    parser.add_argument('--seed', type=int, default=42, help='Seed for random state.')

    args = parser.parse_args()
    main(args)
