#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import numpy as np
from kpi_monitor.utils import DataProcessor, DataPipeline

# Directories
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
default_raw_data_dir = os.path.join(base_dir, 'data', 'raw')
default_processed_data_dir = os.path.join(base_dir, 'data', 'processed')

# Ensure directories exist
os.makedirs(default_raw_data_dir, exist_ok=True)
os.makedirs(default_processed_data_dir, exist_ok=True)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process data and optionally save the output.')
    
    # Add arguments with default values
    parser.add_argument('input', type=str, nargs='?', default=os.path.join(default_raw_data_dir, 'bids_event.csv'), 
                        help='The input file name (CSV format), default is bids_event.csv in the ./data/raw/ directory')
    parser.add_argument('--price', type=str, nargs='?', default=os.path.join(default_raw_data_dir, 'fcr_clearing_price.csv'), 
                        help='The price file name (CSV format), default is fcr_clearing_price.csv in the ./data/raw/ directory')
    parser.add_argument('--save', action='store_true', help='Specify if you want to save the output')
    parser.add_argument('--output', type=str, default=os.path.join(default_processed_data_dir, 'output.csv'), 
                        help='The output file name (default: output.csv in the ./data/processed/ directory')

    # Parse arguments
    args = parser.parse_args()

    # Load your data
    df = pd.read_csv(args.input)
    df_price = pd.read_csv(args.price)

    # Create a processor and pipeline instance
    processor = DataProcessor(file_path=default_raw_data_dir, out_dir=default_processed_data_dir)
    data_clean = processor.clean_data(df, verbose=True)
    pipeline = DataPipeline(data_clean, df_price)

    # Apply transformations (same as your previous logic)
    pipeline.extract_json_column('data')
    pipeline.explode_column('time_slots')
    pipeline.extract_json_column('time_slots', string=False)
    for col in ['attr.to_ts', 'attr.from_ts', 'ts']:
        pipeline.convert_time_column(col)

    pipeline.column_list_numpy(['volume_w', 'price_eur_per_mw'])
    pipeline.df['volume_w'] *= 1.e-6  # Convert Watts to MW

    # Rename and aggregate
    pipeline.rename_columns(
        old_names=['attr.to_ts', 'attr.region', 'attr.from_ts', 'attr.product', 'attr.recipient', 'attr.gate_closure', 'volume_w'],
        new_names=['to_ts', 'region', 'from_ts', 'product', 'recipient', 'gate_closure', 'volume_mw']
    )
    pipeline.add_agg_column('volume_mw', 'volume_mw_sum', function=np.sum)

    # Process the volume data
    pipeline.process_volume_data()

    # Print columns for debugging
    print("Columns in df:", pipeline.df.columns)
    print("Columns in df_price:", pipeline.df_price.columns)

    # Add clearing price data
    pipeline.add_price(df_ts='ts', df_price_ts='start_ts')

    # Print file columns
    print(pipeline.df.columns)

    # Save processed data
    if args.save:
        pipeline.df.to_csv(args.output, index=False)
        print(f'Data saved to {args.output}')
    else:
        print('Output not saved. To save, run with the --save option.')

if __name__ == "__main__":
    main()