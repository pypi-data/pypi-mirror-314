import pandas as pd
import numpy as np

# Function to generate random data for two classes with additional noise
def generate_random_data(n_samples=1000, n_features=10, class_1_mean=7, class_0_mean=3, noise_level=0.25):
    """
    Generate random data for two classes (1 and 0) from Gaussian distributions with added noise.
    
    :param n_samples: Total number of samples (will be split equally between classes 1 and 0)
    :param n_features: Number of features
    :param class_1_mean: Mean of the Gaussian distribution for class 1
    :param class_0_mean: Mean of the Gaussian distribution for class 0
    :param noise_level: Proportion of noise to add to the features
    :return: Pandas DataFrame containing the generated data with sample names as index
    """
    # Half samples for each class
    n_samples_per_class = n_samples // 2
    
    # Generate features for class 1 (right side of the Gaussian)
    class_1_features = np.random.normal(loc=class_1_mean, scale=2, size=(n_samples_per_class, n_features))
    class_1_features = np.clip(class_1_features, 0, None)  # Ensure non-negative values
    class_1_labels = np.ones(n_samples_per_class)  # Label for class 1
    
    # Generate features for class 0 (left side of the Gaussian)
    class_0_features = np.random.normal(loc=class_0_mean, scale=2, size=(n_samples_per_class, n_features))
    class_0_features = np.clip(class_0_features, 0, None)  # Ensure non-negative values
    class_0_labels = np.zeros(n_samples_per_class)  # Label for class 0
    
    # Combine the features and labels
    features = np.vstack((class_1_features, class_0_features))
    labels = np.hstack((class_1_labels, class_0_labels))
    
    # Introduce noise to the features
    noise = np.random.normal(loc=0, scale=1, size=features.shape) * noise_level
    features += noise
    
    # Reduce separability by overlapping class distributions slightly
    features += np.random.normal(loc=0, scale=1.5, size=features.shape)
    
    # Generate sample names
    sample_names = [f'Sample_{i+1}' for i in range(n_samples)]
    
    # Create a DataFrame with sample names as index
    df = pd.DataFrame(features, columns=[f'Feature_{i+1}' for i in range(n_features)], index=sample_names)
    df['label'] = labels.astype(int)
    
    return df

# Generate the data
df = generate_random_data(n_samples=200, n_features=10)

# Save to a temporary CSV file
csv_file_path = 'temp_dataset.csv'
df.to_csv(csv_file_path, index=True)  # Save with index

print(f"Temporary CSV file created at: {csv_file_path}")
