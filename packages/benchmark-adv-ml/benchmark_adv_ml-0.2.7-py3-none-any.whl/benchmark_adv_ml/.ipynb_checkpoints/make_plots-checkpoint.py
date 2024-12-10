import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc
from math import pi
import argparse

# Function to plot AUC curves for different models
def plot_auc_curves(processed_dir, output_dir):
    models = ['LogisticRegression', 'RandomForestClassifier', 'SVC']
    plt.figure(figsize=(10, 8))
    
    for model in models:
        fpr_file = os.path.join(processed_dir, f"{model}_test_fpr.csv")
        tpr_file = os.path.join(processed_dir, f"{model}_test_tpr.csv")
        
        fpr = pd.read_csv(fpr_file)
        tpr = pd.read_csv(tpr_file)
        
        # Sort the FPR and TPR values to ensure proper order for AUC calculation
        mean_fpr = np.linspace(0, 1, len(fpr.columns))
        mean_tpr = np.interp(mean_fpr, fpr.mean(axis=0).sort_values().values, tpr.mean(axis=0).sort_values().values)
        std_tpr = tpr.std(axis=0)
        
        # Compute AUC
        roc_auc = auc(mean_fpr, mean_tpr)
        
        plt.plot(mean_fpr, mean_tpr, label=f'{model} (AUC = {roc_auc:.3f})')
        plt.fill_between(mean_fpr, mean_tpr - std_tpr, mean_tpr + std_tpr, alpha=0.2)

    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves Across Models')
    plt.legend(loc="lower right")
    
    output_file = os.path.join(output_dir, 'auc_curves.png')
    plt.savefig(output_file)
    plt.show()
    print(f"AUC curves saved to {output_file}")

# Function to plot box plot of AUC values across models
def plot_auc_boxplot(processed_dir, output_dir):
    metrics_df = pd.read_csv(os.path.join(processed_dir, 'aggregated_overall_metrics.csv'))
    plt.figure(figsize=(10, 8))
    
    sns.boxplot(x='Model', y='auc', data=metrics_df, palette="Set3")
    sns.swarmplot(x='Model', y='auc', data=metrics_df, color='k', alpha=0.6)
    
    plt.title('AUC Distribution Across Models')
    plt.xlabel('Model')
    plt.ylabel('AUC Score')
    
    output_file = os.path.join(output_dir, 'auc_boxplot.png')
    plt.savefig(output_file)
    plt.show()
    print(f"AUC box plot saved to {output_file}")

# Function to plot feature importance range for each model
def plot_feature_importance(processed_dir, output_dir):
    feature_importance_df = pd.read_csv(os.path.join(processed_dir, 'aggregated_feature_importance.csv'))
    
    models = feature_importance_df['Model'].unique()
    
    for model in models:
        model_df = feature_importance_df[feature_importance_df['Model'] == model]
        plt.figure(figsize=(10, 20))
        
        sns.boxplot(x='Importance', y='Feature', data=model_df, palette="Set3")
        
        plt.title(f'Feature Importance Range for {model}')
        plt.xlabel('Importance')
        plt.ylabel('Feature')
        
        output_file = os.path.join(output_dir, f'{model}_feature_importance.png')
        plt.savefig(output_file)
        plt.show()
        print(f"Feature importance plot saved to {output_file}")

# Function to plot radar chart for mean performance metrics
def plot_radar_chart(processed_dir, output_dir):
    metrics_df = pd.read_csv(os.path.join(processed_dir, 'aggregated_overall_metrics.csv'))
    metrics_df = metrics_df.groupby('Model').mean().reset_index()
    
    categories = ['accuracy', 'precision', 'recall', 'f1_score', 'auc']
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    plt.figure(figsize=(10, 10))
    
    for index, row in metrics_df.iterrows():
        values = row[categories].tolist()
        values += values[:1]
        
        ax = plt.subplot(111, polar=True)
        plt.xticks(angles[:-1], categories, color='grey', size=8)
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=row['Model'])
        ax.fill(angles, values, alpha=0.1)
    
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.title('Model Performance Comparison (Mean Values)')
    
    output_file = os.path.join(output_dir, 'radar_chart.png')
    plt.savefig(output_file)
    plt.show()
    print(f"Radar chart saved to {output_file}")

# Command-line argument parser
def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate plots from the processed results.")
    parser.add_argument('--processed_dir', type=str, required=True, help='Path to the directory containing processed results.')
    parser.add_argument('--output', type=str, required=True, help='Directory to save the generated plots.')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    plot_auc_curves(args.processed_dir, args.output)
    plot_auc_boxplot(args.processed_dir, args.output)
    plot_feature_importance(args.processed_dir, args.output)
    plot_radar_chart(args.processed_dir, args.output)
