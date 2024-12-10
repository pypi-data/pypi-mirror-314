import argparse
import sys
from .benchmark_ml import main as benchmark_main
from .train_autoencoder import main as autoencoder_main
from .ClusteringSurvival import ClusteringSurvival 

def main():
    # Create the top-level parser
    parser = argparse.ArgumentParser(description="Run the Benchmark ML or Autoencoder training pipeline.")

    subparsers = parser.add_subparsers(dest="command", help="Sub-command to run (benchmark or autoencoder)")

    # Benchmark sub-command
    benchmark_parser = subparsers.add_parser('benchmark', help="Run the benchmark ML pipeline")
    benchmark_parser.add_argument('--n_samples', type=int, default=None, help='Number of samples to generate for the dataset. Leave empty if using an existing dataset.')
    benchmark_parser.add_argument('--n_features', type=int, default=10, help='Number of features in the generated dataset.')
    benchmark_parser.add_argument('--data', type=str, help='Path to the existing CSV file containing the dataset.')
    benchmark_parser.add_argument('--target', type=str, default='label', help='Target column name in the dataset.')
    benchmark_parser.add_argument('--output', type=str, required=True, help='Directory to save the final results and plots.')
    benchmark_parser.add_argument('--prelim_output', type=str, required=True, help='Directory to save the preliminary results (predictions).')
    benchmark_parser.add_argument('--n_runs', type=int, default=20, help='Number of runs for model stability evaluation.')
    benchmark_parser.add_argument('--seed', type=int, default=42, help='Seed for random state.')

    # Autoencoder sub-command
    autoencoder_parser = subparsers.add_parser('autoencoder', help="Train and evaluate an autoencoder model")
    autoencoder_parser.add_argument('--data', type=str, required=True, help='Path to the input CSV file containing the data.')
    autoencoder_parser.add_argument('--target', type=str, default='label', help='Target column name in the dataset.')
    autoencoder_parser.add_argument('--sampleID', type=str, default='sampleID', help='SampleID column name in the dataset.')   
    autoencoder_parser.add_argument('--encoder_config', type=str, help='Path to the JSON file defining encoder architecture. If not provided, a temporary config will be generated.')
    autoencoder_parser.add_argument('--latent_dim', type=int, help='Dimensionality of the latent space. If not specified, defaults to input_dim // 8.')
    autoencoder_parser.add_argument('--activation', type=str, default='relu', help='Activation function to use in hidden layers.')
    autoencoder_parser.add_argument('--optimizer', type=str, default='adam', help='Optimizer to use for training.')
    autoencoder_parser.add_argument('--loss', type=str, default='mse', help='Loss function to use.')
    autoencoder_parser.add_argument('--metrics', nargs='+', default=['mse'], help='List of metrics to evaluate.')
    autoencoder_parser.add_argument('--test_size', type=float, default=0.2, help='Proportion of data to use as test set.')
    autoencoder_parser.add_argument('--validation_split', type=float, default=0.1, help='Proportion of training data to use as validation set.')
    autoencoder_parser.add_argument('--epochs', type=int, default=50, help='Number of training epochs.')
    autoencoder_parser.add_argument('--batch_size', type=int, default=32, help='Training batch size.')
    autoencoder_parser.add_argument('--output_dir', type=str, required=True, help='Directory to save the final results and models.')
    autoencoder_parser.add_argument('--prelim_output', type=str, required=True, help='Directory to save the preliminary results (predictions).')
    autoencoder_parser.add_argument('--early_stopping', action='store_true', help='Enable early stopping.')
    autoencoder_parser.add_argument('--patience', type=int, default=5, help='Patience for early stopping.')
    autoencoder_parser.add_argument('--checkpoint', action='store_true', help='Enable model checkpointing.')
    autoencoder_parser.add_argument('--seed', type=int, default=42, help='Seed for random state.')

    clustering_parser = subparsers.add_parser('survival_clustering', help="Run the survival clustering pipeline")
    clustering_parser.add_argument('--data_path', type=str, required=True, help='Path to the input CSV file containing patient features.')
    clustering_parser.add_argument('--clinical_df_path', type=str, required=True, help='Path to the input CSV file containing clinical data.')
    clustering_parser.add_argument('--save_dir', type=str, required=True, help='Directory to save the results.')


    # Parse the command-line arguments
    args = parser.parse_args()

    if args.command == 'benchmark':
        # Call the benchmark function with the relevant arguments
        sys.argv = [''] + [f'--{k}' if v is True else f'--{k}={v}' for k, v in vars(args).items() if v is not None and k != 'command']
        benchmark_main()

    elif args.command == 'autoencoder':
        # Call the autoencoder function and pass the args
        autoencoder_main(args)
        
    elif args.command == 'survival_clustering':
        # Initialize and run the clustering survival pipeline
        clustering_survival = ClusteringSurvival(
            data_path=args.data_path,
            clinical_df_path=args.clinical_df_path,
            save_path=args.save_dir
        )
    else:
        parser.print_help()
if __name__ == "__main__":
    main()
