import argparse
import os
import pandas as pd
#from .make_temp_data import generate_random_data
from .classification_model_stability_test import FeatureClassifiers
from .result_process import aggregate_metrics, aggregate_feature_importance, aggregate_predictions, save_aggregated_data
from .make_plots import plot_auc_curves, plot_auc_boxplot, plot_feature_importance, plot_radar_chart

def main():
    parser = argparse.ArgumentParser(description="Run the full benchmark ML pipeline using all models.")
    parser.add_argument('--n_samples', type=int, default=None, help='Number of samples to generate for the dataset. Leave empty if using an existing dataset.')
    parser.add_argument('--n_features', type=int, default=10, help='Number of features in the generated dataset.')
    parser.add_argument('--data', type=str, help='Path to the existing CV file containing the dataset.')
    parser.add_argument('--target', type=str, default='label', help='Target column name in the dataset.')  # Added target argument
    parser.add_argument('--output', type=str, required=True, help='Directory to save the final results and plots.')
    parser.add_argument('--prelim_output', type=str, required=True, help='Directory to save the preliminary results (predictions).')
    parser.add_argument('--n_runs', type=int, default=20, help='Number of runs for model stability evaluation.')
    parser.add_argument('--seed', type=int, default=42, help='Seed for random state.')

    args = parser.parse_args()

    # Step 1: Handle dataset generation or loading
    if args.data:
        # Load the provided dataset
        df = pd.read_csv(args.data, index_col=0)  # Load the CSV into a DataFrame
        print(f"Using provided dataset: {args.data}")
    else:
        print(f"Issue with the Data")

    # Step 2: Run classification model stability tests for all models
    models = ['LogisticRegression', 'SVC', 'RandomForestClassifier']
    fc = FeatureClassifiers()
    
    for model in models:
        print(f"Running model: {model}")
        fc.model_stability_evaluation(df, args.target, model, n_runs=args.n_runs, prediction_dir=args.prelim_output, random_state=args.seed)

    # Step 3: Process results
    aggregated_metrics = aggregate_metrics(args.prelim_output)
    aggregated_importance = aggregate_feature_importance(args.prelim_output)
    aggregated_predictions = aggregate_predictions(args.prelim_output)
    save_aggregated_data(aggregated_metrics, aggregated_importance, aggregated_predictions, args.output)

    # Step 4: Generate plots
    plot_auc_curves(args.output, args.output)
    plot_auc_boxplot(args.output, args.output)
    plot_feature_importance(args.output, args.output)
    plot_radar_chart(args.output, args.output)

if __name__ == "__main__":
    main()
