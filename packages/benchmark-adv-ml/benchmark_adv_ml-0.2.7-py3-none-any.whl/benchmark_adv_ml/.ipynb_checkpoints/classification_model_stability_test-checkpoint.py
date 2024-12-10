import pandas as pd
import numpy as np
import argparse
import os
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from .pre_processing import load_and_preprocess_data, split_data  # Import the preprocessing functions

# Feature classifier class to handle model training and feature selection
class FeatureClassifiers:
    def __init__(self):
        self.models = {
            'LogisticRegression': LogisticRegression(class_weight='balanced', max_iter=1000),
            'SVC': SVC(kernel='linear'),
            'RandomForestClassifier': RandomForestClassifier()
        }

    def model_stability_evaluation(self, df, target_column, model_name, n_runs=1, test_size=0.2, prediction_dir=None, random_state=None):
        metrics = {'accuracy': [], 'precision': [], 'recall': [], 'f1_score': [], 'auc': []}

        for run_id in range(1, n_runs + 1):
            # Perform real-time train/test split
            split_data_dict = split_data(df, target_column, test_size=test_size, random_state=random_state + run_id if random_state is not None else None)
            X_train, y_train = split_data_dict['train']['X'], split_data_dict['train']['y']
            X_test, y_test = split_data_dict['test']['X'], split_data_dict['test']['y']

            model = self.models[model_name]
            model.fit(X_train, y_train)
            y_pred_train = model.predict(X_train)
            y_pred_test = model.predict(X_test)

            # Save raw prediction values for AUC curve preparation
            if prediction_dir:
                run_dir = os.path.join(prediction_dir, f'run_{run_id}', model_name)
                os.makedirs(run_dir, exist_ok=True)

                # Save prediction probabilities or decision function values for both train and test data
                self.save_predictions(model, X_train, y_train, X_test, y_test, run_dir)

                # Save feature importance or coefficients
                self.save_feature_importance(model, X_train.columns, run_dir)

                # Save train, test, and overall metrics
                self.save_metrics(y_train, y_pred_train, 'train', run_dir)
                self.save_metrics(y_test, y_pred_test, 'test', run_dir)
                self.save_overall_metrics(y_train, y_pred_train, y_test, y_pred_test, run_dir)

            # Calculate metrics
            run_metrics = {
                'accuracy': accuracy_score(y_test, y_pred_test),
                'precision': precision_score(y_test, y_pred_test, average='weighted'),
                'recall': recall_score(y_test, y_pred_test, average='weighted'),
                'f1_score': f1_score(y_test, y_pred_test, average='weighted'),
                'auc': roc_auc_score(y_test, y_pred_test, average='weighted')
            }

            for key in metrics:
                metrics[key].append(run_metrics[key])

        return pd.DataFrame(metrics)

    def save_predictions(self, model, X_train, y_train, X_test, y_test, run_dir):
        """Save the raw prediction values for both training and testing sets."""
        # Handle training data
        self._save_single_prediction(model, X_train, y_train, os.path.join(run_dir, 'train_predictions.csv'))

        # Handle testing data
        self._save_single_prediction(model, X_test, y_test, os.path.join(run_dir, 'test_predictions.csv'))

    def save_feature_importance(self, model, feature_names, run_dir):
        """Save the feature importance or coefficients to a CSV file."""
        if hasattr(model, "coef_"):
            feature_importance = model.coef_[0]
        elif hasattr(model, "feature_importances_"):
            feature_importance = model.feature_importances_
        else:
            feature_importance = None

        if feature_importance is not None:
            importance_df = pd.DataFrame({
                'Feature': feature_names,
                'Importance': feature_importance
            })
            importance_df.to_csv(os.path.join(run_dir, 'feature_importance.csv'), index=False)
            print(f"Feature importance saved to {os.path.join(run_dir, 'feature_importance.csv')}")
        else:
            print(f"No feature importance available for model {model.__class__.__name__}")

    def save_metrics(self, y_true, y_pred, split_name, run_dir):
        """Save metrics for a given split (train or test) to a CSV file."""
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted'),
            'f1_score': f1_score(y_true, y_pred, average='weighted'),
            'auc': roc_auc_score(y_true, y_pred, average='weighted')
        }
        metrics_df = pd.DataFrame([metrics])
        metrics_df.to_csv(os.path.join(run_dir, f'{split_name}_metrics.csv'), index=False)
        print(f"{split_name.capitalize()} metrics saved to {os.path.join(run_dir, f'{split_name}_metrics.csv')}")

    def save_overall_metrics(self, y_train, y_pred_train, y_test, y_pred_test, run_dir):
        """Save overall metrics by combining train and test data."""
        y_true_overall = np.concatenate([y_train, y_test])
        y_pred_overall = np.concatenate([y_pred_train, y_pred_test])

        metrics = {
            'accuracy': accuracy_score(y_true_overall, y_pred_overall),
            'precision': precision_score(y_true_overall, y_pred_overall, average='weighted'),
            'recall': recall_score(y_true_overall, y_pred_overall, average='weighted'),
            'f1_score': f1_score(y_true_overall, y_pred_overall, average='weighted'),
            'auc': roc_auc_score(y_true_overall, y_pred_overall, average='weighted')
        }
        metrics_df = pd.DataFrame([metrics])
        metrics_df.to_csv(os.path.join(run_dir, 'overall_metrics.csv'), index=False)
        print(f"Overall metrics saved to {os.path.join(run_dir, 'overall_metrics.csv')}")

    def _save_single_prediction(self, model, X, y, file_path):
        """Save the prediction values to a CSV file."""
        if hasattr(model, "predict_proba"):
            y_scores = model.predict_proba(X)[:, 1]

        elif hasattr(model, "decision_function"):
            y_scores = model.decision_function(X)
            # Normalize decision_function output to be between 0 and 1
            y_scores = (y_scores - y_scores.min()) / (y_scores.max() - y_scores.min())
        else:
            raise ValueError(f"Model {model.__class__.__name__} does not have predict_proba or decision_function")

        # Combine true labels and prediction scores
        predictions_df = pd.DataFrame({
            'True_Labels': y,
            'Predicted_Scores': y_scores
        })

        # Save the predictions to a CSV file
        predictions_df.to_csv(file_path, index=True)  # Save with index (sample names)
        print(f"Predictions saved to {file_path}")

# Command-line argument parser
def parse_arguments():
    parser = argparse.ArgumentParser(description="Train models and evaluate their performance with stability analysis.")
    parser.add_argument('--data', type=str, required=True, help='Path to the input CSV file containing the data.')
    parser.add_argument('--target', type=str, default='label', help='Target column name in the dataset.')
    parser.add_argument('-n', '--n_runs', type=int, default=1, help='Number of runs for model stability evaluation.')
    parser.add_argument('--output', type=str, required=True, help='Directory to save the results.')
    parser.add_argument('--model', type=str, default='LogisticRegression', choices=['LogisticRegression', 'SVC', 'RandomForestClassifier'], help='Model to train and evaluate.')
    parser.add_argument('--prediction_dir', type=str, default='prediction-values', help='Directory to save raw prediction values.')
    parser.add_argument('--seed', type=int, default=None, help='Seed for random state of split.')
    parser.add_argument('--test_size', type=float, default=0.2, help='Proportion of the dataset to include in the test split.')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    # Load and preprocess data
    df = load_and_preprocess_data(args.data, args.target)

    # Initialize the classifier
    fc = FeatureClassifiers()

    # Perform model stability evaluation and save raw predictions
    metrics_df = fc.model_stability_evaluation(
        df, target_column=args.target,
        model_name=args.model,
        n_runs=args.n_runs,
        test_size=args.test_size,
        prediction_dir=args.prediction_dir,
        random_state=args.seed
    )

    # Save results
    results_file = os.path.join(args.output, f'{args.model}_metrics.csv')
    metrics_df.to_csv(results_file, index=False)
    print(f"Model stability metrics saved to {results_file}")
