import pandas as pd
import numpy as np
import argparse
import os
from sklearn.model_selection import train_test_split

# Function to load data and preprocess it
def load_and_preprocess_data(file_path, target_column='label', id_column='SampleID'):
    df = pd.read_csv(file_path)  # Load the dataset
    print(f"Data shape: {df.shape}")  # Print the shape of the dataset
    print(f"Original target column values:\n{df[target_column].head()}")

    # Filter out the id column
    if id_column in df.columns:
        df = df.drop(columns=[id_column])
        print(f"Data shape after dropping id column: {df.shape}")

    # Ensure all columns except target are numeric
    for col in df.columns:
        if col != target_column:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Fill missing values with the mean of each column
    df.fillna(df.mean(), inplace=True)
    
    # Convert target column to numeric if it's categorical
    if df[target_column].dtype == 'object' or df[target_column].dtype.name == 'category':
        df[target_column], unique_vals = pd.factorize(df[target_column])
        print(f"Factorized target column values:\n{df[target_column].head()}")
        print(f"Mapping: {dict(enumerate(unique_vals))}")
    
    # Print the unique values to verify factorization
    print(f"Unique values in target column after factorization: {df[target_column].unique()}")
    print(f"Processed data:\n{df.head()}")  # Print the first few rows to ensure proper processing

    return df

def load_prep_for_ae(file_path, id_column='SampleID'):
    # Load the dataset
    df = pd.read_csv(file_path)
    print(f"Data shape: {df.shape}")  # Print the shape of the dataset

    # Set the ID column as index if it exists
    if id_column in df.columns:
        df.set_index(id_column, inplace=True)
        print(f"Data shape after setting ID column as index: {df.shape}")

    # Ensure all columns are numeric
    df = df.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='all')

    # Fill missing values with the mean of each column
    df.fillna(df.mean(), inplace=True)

    print(f"Processed data (first few rows):\n{df.head()}")  # Print the first few rows to ensure proper processing

    return df

# Function to split the data into training and testing sets, separately for each class
def split_data(df, target_column, test_size=0.2, random_state=None):
    # Check if the target column has been correctly processed
    print(f"Unique values in target column: {df[target_column].unique()}")

    # Separate the data by class
    df_class_0 = df[df[target_column] == 0]
    df_class_1 = df[df[target_column] == 1]

    print(f"Class 0 samples: {len(df_class_0)}, Class 1 samples: {len(df_class_1)}")

    # Ensure there are enough samples to split
    if len(df_class_0) == 0 or len(df_class_1) == 0:
        raise ValueError("One of the classes has no samples, cannot perform train/test split.")

    # Split each class individually, retaining indices
    X_train_0, X_test_0, y_train_0, y_test_0 = train_test_split(
        df_class_0.drop(columns=[target_column]), 
        df_class_0[target_column], 
        test_size=test_size, 
        random_state=random_state
    )

    X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(
        df_class_1.drop(columns=[target_column]), 
        df_class_1[target_column], 
        test_size=test_size, 
        random_state=random_state
    )

    # Combine the splits back together
    X_train = pd.concat([X_train_0, X_train_1])
    y_train = pd.concat([y_train_0, y_train_1])
    X_test = pd.concat([X_test_0, X_test_1])
    y_test = pd.concat([y_test_0, y_test_1])

    print(f"Train set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")

    print(X_train)
    
    return {'train': {'X': X_train, 'y': y_train},
            'test': {'X': X_test, 'y': y_test}}


# pre_processing.py

def split_data_for_ae(df, test_size=0.2, random_state=None):
    # Split the data into training and test sets
    X_train, X_test = train_test_split(df, test_size=test_size, random_state=random_state)

    # Print the sizes of the training and test sets
    print(f"Train set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")

    # Return a dictionary with the split data
    return {'train': {'X': X_train},
            'test': {'X': X_test}}


# Function to save the training and testing data into a specified output directory
def save_split_data(split_data_dict, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # Define file paths
    preprocessed_file_train_X = os.path.join(output_dir, 'train_X.csv')
    preprocessed_file_train_y = os.path.join(output_dir, 'train_y.csv')
    preprocessed_file_test_X = os.path.join(output_dir, 'test_X.csv')
    preprocessed_file_test_y = os.path.join(output_dir, 'test_y.csv')
    
    # Save the data with indices (sample names)
    split_data_dict['train']['X'].to_csv(preprocessed_file_train_X)
    split_data_dict['train']['y'].to_csv(preprocessed_file_train_y)
    split_data_dict['test']['X'].to_csv(preprocessed_file_test_X)
    split_data_dict['test']['y'].to_csv(preprocessed_file_test_y)

    print(f"Training and testing data saved to {output_dir}")

# Command-line argument parser
def parse_arguments():
    parser = argparse.ArgumentParser(description="Preprocess the dataset and optionally save the split data.")
    parser.add_argument('--data', type=str, required=True, help='Path to the input CSV file.')
    parser.add_argument('--target', type=str, default='label', help='Target column name in the dataset.')
    parser.add_argument('--sampleID', type=str, default='sampleID', help='SampleID column name in the dataset.')
    parser.add_argument('--output', type=str, help='Directory to save the preprocessed data (optional).')
    parser.add_argument('--seed', type=int, default=None, help='Seed for random state of split.')
    parser.add_argument('--test_size', type=float, default=0.2, help='Proportion of the dataset to include in the test split.')
    parser.add_argument('--return_split', action='store_true', help='If set, the function will return the split data instead of saving it.')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    # Load and preprocess data
    df = load_and_preprocess_data(args.data, args.target,args.sampleID)

    # Split the data with the provided test size and seed
    split_data_dict = split_data(df, args.target, test_size=args.test_size, random_state=args.seed)

    # Save the split data if an output directory is specified
    if args.output:
        save_split_data(split_data_dict, args.output)
    
    # If return_split is set, return the data (useful for real-time splits during model training)
    if args.return_split:
        train_X, train_y = split_data_dict['train']['X'], split_data_dict['train']['y']
        test_X, test_y = split_data_dict['test']['X'], split_data_dict['test']['y']
        print("Returning split data for further processing.")

