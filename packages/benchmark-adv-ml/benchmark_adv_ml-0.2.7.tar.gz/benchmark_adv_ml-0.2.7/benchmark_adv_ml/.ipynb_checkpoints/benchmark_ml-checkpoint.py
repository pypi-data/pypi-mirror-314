import argparse
import os
from .make_temp_data import generate_random_data
from .classification_model_stability_test import FeatureClassifiers
from .result_process import aggregate_metrics, aggregate_feature_importance, save_aggregated_data
from .make_plots import plot_auc_curves, plot_auc_boxplot, plot_feature_importance, plot_radar_chart

def main():
    parser = argparse.ArgumentParser(description="Run the full benchmark ML pipeline.")
    parser.add_argument('--n_samples', type=int, default=None, help='Number of samples to generate for the dataset. Leave empty if using an existing dataset.')
    parser.add_argument('--n_features', type=int, default=10, help='Number of features in the generated dataset.')
    parser.add_argument('--data', type=str, help='Path to the existing CSV file containing the dataset.')
    parser.add_argument('--output', type=str, required=True, help='Directory to save the results and plots.')
    parser.add_argument('--n_runs', type=int, default=20, help='Number of runs for model stability evaluation.')
    parser.add_argument('--seed', type=int, default=42, help='Seed for random state.')

    args = parser.parse_args()

    # Step 1: Handle dataset generation or loading
    if args.data:
        # Load the provided dataset
        temp_data_path = args.data
        print(f"Using provided dataset: {temp_data_path}")
    else:
        # Generate the random dataset
        df = generate_random_data(n_samples=args.n_samples, n_features=args.n_features)
        temp_data_path = os.path.join(args.output, 'temp_dataset.csv')
        df.to_csv(temp_data_path, index=True)
        print(f"Generated random dataset at: {temp_data_path}")

    # Step 2: Run classification model stability tests
    classifiers = ['RandomForestClassifier', 'LogisticRegression', 'SVC']
    for clf in classifiers:
        fc = FeatureClassifiers()
        fc.model_stability_evaluation(temp_data_path, 'label', clf, n_runs=args.n_runs, prediction_dir=args.output, random_state=args.seed)
    
    # Step 3: Process results
    aggregated_metrics = aggregate_metrics(args.output)
    aggregated_importance = aggregate_feature_importance(args.output)
    save_aggregated_data(aggregated_metrics, aggregated_importance, args.output)

    # Step 4: Generate plots
    plot_auc_curves(args.output, args.output)
    plot_auc_boxplot(args.output, args.output)
    plot_feature_importance(args.output, args.output)
    plot_radar_chart(args.output, args.output)

if __name__ == "__main__":
    main()
