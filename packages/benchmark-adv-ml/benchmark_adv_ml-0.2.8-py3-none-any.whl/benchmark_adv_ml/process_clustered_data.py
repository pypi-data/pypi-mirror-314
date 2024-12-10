# process_clustered_data.py

import pandas as pd
import argparse

def process_clustered_data(file_path, group1, group2, id_column='PatientID', output_file=None):
    """
    Processes the clustered data to keep only two specified groups and assign binary labels.

    :param file_path: Path to the clustered_data.csv file.
    :param group1: The first group number to keep.
    :param group2: The second group number to keep.
    :param id_column: The name of the ID column ('PatientID' or 'SampleID').
    :param output_file: (Optional) Path to save the processed dataframe.
    :return: The processed dataframe.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Ensure the ID column is at the front
    if id_column in df.columns:
        # Move the ID column to the first position
        cols = df.columns.tolist()
        cols.insert(0, cols.pop(cols.index(id_column)))
        df = df[cols]
    else:
        raise ValueError(f"ID column '{id_column}' not found in the data.")

    # Remove the columns: 'Overall Survival Status', 'Overall Survival (Months)', 'PC1', 'PC2', 'tX', 'tY'
    columns_to_remove = ['Overall Survival Status', 'Overall Survival (Months)', 'PC1', 'PC2', 'tX', 'tY']
    df = df.drop(columns=[col for col in columns_to_remove if col in df.columns])

    # Check if 'groups' column exists
    if 'groups' not in df.columns:
        raise ValueError("Column 'groups' not found in the data.")
    
    # Filter the dataframe to keep only the specified groups
    df_filtered = df[df['groups'].isin([group1, group2])].copy()

    # Map the groups to labels 0 and 1
    group_to_label = {group1: 0, group2: 1}
    df_filtered['label'] = df_filtered['groups'].map(group_to_label)

    # Remove the 'groups' column
    df_filtered = df_filtered.drop(columns=['groups'])

    # Ensure the 'label' column is at the end
    cols = df_filtered.columns.tolist()
    cols.append(cols.pop(cols.index('label')))
    df_filtered = df_filtered[cols]

    # Optionally, save the processed dataframe
    if output_file:
        df_filtered.to_csv(output_file, index=False)
        print(f"Processed dataframe saved to {output_file}")

    return df_filtered

def main(args=None):
    parser = argparse.ArgumentParser(description="Process clustered data to keep two groups and assign binary labels.")
    parser.add_argument('--data', type=str, required=True, help='Path to the clustered_data.csv file.')
    parser.add_argument('--group1', type=int, required=True, help='First group number to keep.')
    parser.add_argument('--group2', type=int, required=True, help='Second group number to keep.')
    parser.add_argument('--sampleID', type=str, default='PatientID', help='SampleID column name in the dataset.')
    parser.add_argument('--output_file', type=str, required=True, help='Path to save the processed dataframe.')
    parsed_args = parser.parse_args(args)

    # Call the function with parsed arguments
    process_clustered_data(
        file_path=parsed_args.data,
        group1=parsed_args.group1,
        group2=parsed_args.group2,
        id_column=parsed_args.sampleID,
        output_file=parsed_args.output_file
    )

if __name__ == "__main__":
    main()