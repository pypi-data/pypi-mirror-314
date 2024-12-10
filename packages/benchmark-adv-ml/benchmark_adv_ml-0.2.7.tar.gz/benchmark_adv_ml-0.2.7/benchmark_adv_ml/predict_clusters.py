# predict_clusters.py

import argparse
import os
import pandas as pd
import numpy as np
from joblib import load
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
import itertools
import matplotlib.cm as cm

def main(args):
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Load the KMeans model
    model_path = os.path.join(args.model_dir, 'kmeans_model.joblib')
    kmeans = load(model_path)
    print(f"KMeans model loaded from {model_path}")

    # Load and preprocess data
    df = pd.read_csv(args.data).set_index('PatientID')
    latent_features = df.to_numpy()
    print(f"Data loaded from {args.data}, shape: {df.shape}")

    # Predict clusters
    labels = kmeans.predict(latent_features)
    df['groups'] = labels
    print("Cluster predictions completed.")

    # Save predictions
    predictions_path = os.path.join(args.output_dir, 'cluster_predictions.csv')
    df[['groups']].to_csv(predictions_path)
    print(f"Cluster predictions saved to {predictions_path}")

    # If survival data is available, perform survival analysis
    if 'Overall Survival (Months)' in df.columns and 'Overall Survival Status' in df.columns:
        print("Survival data detected. Performing survival analysis.")
        perform_survival_analysis(df, args.output_dir)
    else:
        print("Survival data not found in the input file. Skipping survival analysis.")

def perform_survival_analysis(df, output_dir):
    # Generate color list based on median survival
    color_list = generate_color_list_based_on_median_survival(df)

    # Perform log-rank test
    significant_pairs = perform_log_rank_test(df, output_dir)

    # Generate summary table
    summary_table = generate_summary_table(df, output_dir)

    # Plot Kaplan-Meier curves
    plot_kaplan_meier(df, color_list, output_dir)

    # Plot median survival bar chart
    plot_median_survival_bar(df, color_list, output_dir)

def generate_color_list_based_on_median_survival(df):
    groups = df['groups'].unique()
    median_survival_times = {group: df[df['groups'] == group]['Overall Survival (Months)'].median() for group in groups}
    sorted_groups = sorted(groups, key=median_survival_times.get, reverse=True)

    color_palette = sns.color_palette("hsv", len(groups))
    color_list = {group: color for group, color in zip(sorted_groups, color_palette)}
    return color_list

def perform_log_rank_test(df, output_dir, alpha=0.05):
    groups = df['groups'].unique()
    significant_pairs = []
    log_rank_results = []

    print("Log-rank test for survival")
    print("Group 1 vs Group 2 : p_value")

    for pair in itertools.combinations(groups, 2):
        group_a = df[df['groups'] == pair[0]]
        group_b = df[df['groups'] == pair[1]]
        results = logrank_test(group_a['Overall Survival (Months)'],
                               group_b['Overall Survival (Months)'],
                               event_observed_A=group_a['Overall Survival Status'],
                               event_observed_B=group_b['Overall Survival Status'])

        significance_marker = "****" if results.p_value < alpha else ""
        result_string = f"{pair[0]} vs {pair[1]} :  {results.p_value:.4f} {significance_marker}"
        log_rank_results.append(result_string)
        print(result_string)

        if results.p_value < alpha:
            significant_pairs.append(pair)

    # Save the log-rank results to a file
    log_rank_path = os.path.join(output_dir, 'log_rank_test_results.txt')
    with open(log_rank_path, 'w') as f:
        f.write("Log-rank Test Results for Survival\n")
        for result in log_rank_results:
            f.write(result + "\n")
    print(f"Log-rank test results saved to {log_rank_path}")

    if significant_pairs:
        significant_path = os.path.join(output_dir, 'significant_pairs.txt')
        with open(significant_path, 'w') as f:
            f.write("Significant Group Pairs (p < 0.05):\n")
            for pair in significant_pairs:
                f.write(f"{pair[0]} vs {pair[1]}\n")
        print(f"Significant pairs saved to {significant_path}")

    return significant_pairs

def generate_summary_table(df, output_dir):
    groups = df['groups'].unique()
    summary_table = pd.DataFrame(columns=['Total number of patients', 'Alive', 'Deceased', 'Median survival time'], index=groups)

    for group in groups:
        group_data = df[df['groups'] == group]
        total_patients = len(group_data)
        alive = len(group_data[group_data['Overall Survival Status'] == 0])
        deceased = len(group_data[group_data['Overall Survival Status'] == 1])

        kmf = KaplanMeierFitter()
        kmf.fit(group_data['Overall Survival (Months)'], group_data['Overall Survival Status'])

        median_survival_time = kmf.median_survival_time_
        summary_table.loc[group] = [total_patients, alive, deceased, median_survival_time]

    # Save the summary table as a CSV file
    summary_table_path = os.path.join(output_dir, 'summary_table.csv')
    summary_table.to_csv(summary_table_path)
    print(f"Summary table saved to {summary_table_path}")

    return summary_table

def plot_kaplan_meier(df, color_list, output_dir, name='kaplan_meier'):
    kmf = KaplanMeierFitter()

    plt.figure(figsize=(8, 6))
    groups = sorted(df['groups'].unique())
    for group in groups:
        group_data = df[df['groups'] == group]
        kmf.fit(group_data['Overall Survival (Months)'], group_data['Overall Survival Status'], label=f'Group {group}')
        kmf.plot(ci_show=False, linewidth=2, color=color_list[group])
    plt.title("Kaplan-Meier Curves for Each Group")
    plt.xlabel("Overall Survival (Months)", fontweight='bold')
    plt.ylabel("Survival Probability", fontweight='bold')
    plt.legend()
    plt.savefig(os.path.join(output_dir, f'{name}.jpeg'), dpi=300)
    plt.show()

def plot_median_survival_bar(df, color_list, output_dir, name='median_survival'):
    summary_df = generate_summary_table(df, output_dir)
    summary_df['group'] = summary_df.index
    max_val = summary_df["Median survival time"].replace(np.inf, np.nan).max()
    summary_df["Display Median"] = summary_df["Median survival time"].replace(np.inf, max_val * 1.1)

    summary_df = summary_df.sort_index()
    colors = [color_list[group] for group in summary_df.index]

    num_groups = len(summary_df)
    plt.figure(figsize=(6, num_groups * 0.8))
    plt.grid(False)
    sns.barplot(data=summary_df, y='group', x="Display Median", palette=colors, orient="h", order=summary_df.index)
    plt.xlabel("Median Survival Time (Months)")
    plt.ylabel("Groups")
    plt.title("Median Survival Time by Group")
    plt.tight_layout()

    plt.savefig(os.path.join(output_dir, f'{name}.jpeg'), dpi=300)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict clusters using a trained KMeans model and perform survival analysis.")

    parser.add_argument('--data', type=str, required=True, help='Path to the input CSV file containing the latent features.')
    parser.add_argument('--model_dir', type=str, required=True, help='Directory where the trained KMeans model is saved.')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save the cluster predictions and analysis results.')

    args = parser.parse_args()
    main(args)
