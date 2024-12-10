import pandas as pd
import numpy as np
import argparse
import os
import pickle
from collections import Counter, defaultdict
from sklearn.metrics import roc_curve

# Function to aggregate metrics across all runs for all models
def aggregate_metrics(results_dir):
    all_metrics = defaultdict(list)
    
    for run_dir in os.listdir(results_dir):
        run_path = os.path.join(results_dir, run_dir)
        if os.path.isdir(run_path):
            for model_dir in os.listdir(run_path):
                model_path = os.path.join(run_path, model_dir)
                if os.path.isdir(model_path):
                    for metric_file in ['train_metrics.csv', 'test_metrics.csv', 'overall_metrics.csv']:
                        metric_path = os.path.join(model_path, metric_file)
                        if os.path.exists(metric_path):
                            metrics_df = pd.read_csv(metric_path)
                            metrics_df['Model'] = model_dir
                            metrics_df['Run'] = run_dir
                            metrics_df['Type'] = metric_file.replace('_metrics.csv', '')
                            all_metrics[metric_file].append(metrics_df)
    
    aggregated_metrics = {}
    for metric_file, dfs in all_metrics.items():
        aggregated_metrics[metric_file] = pd.concat(dfs, ignore_index=True)
    
    return aggregated_metrics

# Function to aggregate feature importance across all runs for all models
def aggregate_feature_importance(results_dir):
    feature_importance_agg = defaultdict(list)
    
    for run_dir in os.listdir(results_dir):
        run_path = os.path.join(results_dir, run_dir)
        if os.path.isdir(run_path):
            for model_dir in os.listdir(run_path):
                model_path = os.path.join(run_path, model_dir)
                if os.path.isdir(model_path):
                    feature_importance_path = os.path.join(model_path, 'feature_importance.csv')
                    if os.path.exists(feature_importance_path):
                        feature_df = pd.read_csv(feature_importance_path)
                        feature_df['Model'] = model_dir
                        feature_df['Run'] = run_dir
                        feature_importance_agg['feature_importance'].append(feature_df)
    
    if feature_importance_agg['feature_importance']:
        feature_importance_df = pd.concat(feature_importance_agg['feature_importance'], ignore_index=True)
        return feature_importance_df
    else:
        return None

# Function to aggregate prediction data and calculate ROC curve coordinates
def aggregate_predictions(results_dir):
    prediction_agg = defaultdict(lambda: {'fpr': [], 'tpr': [], 'thresholds': []})
    
    for run_dir in os.listdir(results_dir):
        run_path = os.path.join(results_dir, run_dir)
        if os.path.isdir(run_path):
            for model_dir in os.listdir(run_path):
                model_path = os.path.join(run_path, model_dir)
                if os.path.isdir(model_path):
                    for pred_file in ['train_predictions.csv', 'test_predictions.csv']:
                        pred_path = os.path.join(model_path, pred_file)
                        if os.path.exists(pred_path):
                            pred_df = pd.read_csv(pred_path)
                            fpr, tpr, thresholds = roc_curve(pred_df['True_Labels'], pred_df['Predicted_Scores'])
                            prediction_agg[f'{model_dir}_{pred_file.replace("_predictions.csv", "")}']['fpr'].append(fpr)
                            prediction_agg[f'{model_dir}_{pred_file.replace("_predictions.csv", "")}']['tpr'].append(tpr)
                            prediction_agg[f'{model_dir}_{pred_file.replace("_predictions.csv", "")}']['thresholds'].append(thresholds)
    
    return prediction_agg

# Function to save aggregated data to CSV files
def save_aggregated_data(aggregated_metrics, aggregated_importance, aggregated_predictions, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for metric_name, metric_df in aggregated_metrics.items():
        output_file = os.path.join(output_dir, f'aggregated_{metric_name}')
        metric_df.to_csv(output_file, index=False)
        print(f"Aggregated metrics saved to {output_file}")
    
    if aggregated_importance is not None:
        output_file = os.path.join(output_dir, 'aggregated_feature_importance.csv')
        aggregated_importance.to_csv(output_file, index=False)
        print(f"Aggregated feature importance saved to {output_file}")
    
    if aggregated_predictions:
        for pred_key, pred_data in aggregated_predictions.items():
            fpr_df = pd.DataFrame(pred_data['fpr'])
            tpr_df = pd.DataFrame(pred_data['tpr'])
            thresholds_df = pd.DataFrame(pred_data['thresholds'])
            fpr_df.to_csv(os.path.join(output_dir, f'{pred_key}_fpr.csv'), index=False)
            tpr_df.to_csv(os.path.join(output_dir, f'{pred_key}_tpr.csv'), index=False)
            thresholds_df.to_csv(os.path.join(output_dir, f'{pred_key}_thresholds.csv'), index=False)
            print(f"Aggregated predictions saved for {pred_key}")

# Command-line argument parser
def parse_arguments():
    parser = argparse.ArgumentParser(description="Process the results of the model stability tests.")
    parser.add_argument('--results_dir', type=str, required=True, help='Path to the directory containing the results from model stability evaluation.')
    parser.add_argument('--output', type=str, required=True, help='Directory to save the processed results.')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    # Aggregate metrics, feature importance, and predictions across all runs and models
    aggregated_metrics = aggregate_metrics(args.results_dir)
    aggregated_importance = aggregate_feature_importance(args.results_dir)
    aggregated_predictions = aggregate_predictions(args.results_dir)

    # Save the aggregated data
    save_aggregated_data(aggregated_metrics, aggregated_importance, aggregated_predictions, args.output)
