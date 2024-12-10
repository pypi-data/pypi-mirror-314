# Modules
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import argparse
from datetime import datetime
import os

# Functions
def find_in_dataframe(df, target, target_format='auto', rows=None, cols=None, list=False):

    # Filter the DataFrame based on specified rows and columns, if provided
    if rows is not None:
        df = df.loc[rows]
    if cols is not None:
        df = df[cols]

    # If 'auto', decide based on target's type
    if target_format == 'auto':
        if pd.isna(target):  # If target is NaN, force 'nan' search
            target_format = 'nan'
        elif isinstance(target, str):
            target_format = 'string'
        else:
            target_format = 'numeric'
    
    # Numeric search: Exact match for numeric values
    if target_format == 'numeric':
        match = df == target

    # String search: Keyword match for strings using vectorized string search
    elif target_format == 'string':
        match = df.astype(str).apply(lambda col: col.str.contains(str(target), na=False))

    # NaN search: Use pandas' isna() function
    elif target_format == 'nan':
        match = df.isna()

    # Use stack to get a list of (row, column) indices where matches occurred
    if(list):
        return match.stack()[match.stack()].index.tolist()
    else:
        return match

def aggregate_volumes(df, recipients=None, products=None, 
                                   start_date=None, end_date=None, 
                                   agg_period='D', agg_func='sum',
                                   price_col='price_cents'):
    """
    Aggregates sent, staged, approved, and rejected volumes over time, and calculates 
    revenue_gain and revenue_loss based on approved and rejected volumes, respectively.

    Parameters:
    - df: The original DataFrame with volume and event data.
    - recipients: List of recipients to filter by (default None means no filtering).
    - products: List of products to filter by (default None means no filtering).
    - start_date: Start date for filtering (default None means use min date from DataFrame).
    - end_date: End date for filtering (default None means use max date from DataFrame).
    - agg_period: Aggregation period ('h' for hourly, 'D' for daily, 'W' for weekly, 'M' for monthly, 'Y' for yearly).
    - agg_func: Aggregation function, either 'sum', 'mean', or 'both'.
    - price_col: Column name for the price data (default is 'price_cents').

    Returns:
    - Aggregated DataFrame with sent, staged, approved, rejected volumes, and revenue columns.
    """

    # Step 1: Filter based on recipients and products
    if recipients is not None:
        df = df[df['recipient'].isin(recipients)]
    if products is not None:
        df = df[df['product'].isin(products)]
    
    # Step 2: Ensure the 'ts' column is in datetime format and set it as the index
    df['ts'] = pd.to_datetime(df['ts'])  # Convert to datetime
    df.set_index('ts', inplace=True)     # Set 'ts' as the index

    # Step 3: Set start and end dates based on input or min/max of DataFrame
    if start_date is None:
        start_date = df.index.min()  # Use the minimum date from the DataFrame
    if end_date is None:
        end_date = df.index.max()    # Use the maximum date from the DataFrame

    # Filter the DataFrame based on the date range
    df = df[(df.index >= start_date) & (df.index <= end_date)]

    # Step 4: Define aggregation functions
    if agg_func == 'sum':
        agg_func_dict = 'sum'
    elif agg_func == 'mean':
        agg_func_dict = 'mean'
    elif agg_func == 'both':
        agg_func_dict = ['sum', 'mean']
    else:
        raise ValueError("Invalid aggregation function. Use 'sum', 'mean', or 'both'.")

    # Step 5: Handle revenue calculation by resampling price
    price_resampled = df[price_col].resample(agg_period).mean()

    # Step 6: Aggregate data for gate_closure = 1 and gate_closure = 2 separately
    df_gc1 = df[df['gate_closure'] == 1].resample(agg_period).agg({
        'sent_volume': agg_func_dict, 
        'staged_volume': agg_func_dict, 
        'approved_volume': agg_func_dict, 
        'rejected_volume': agg_func_dict
    })
    df_gc2 = df[df['gate_closure'] == 2].resample(agg_period).agg({
        'sent_volume': agg_func_dict, 
        'staged_volume': agg_func_dict, 
        'approved_volume': agg_func_dict, 
        'rejected_volume': agg_func_dict
    })

    # Step 7: Calculate revenue for each gate_closure
    df_gc1['revenue_gain_1'] = df_gc1['approved_volume'] * price_resampled / 100.  # Convert cents to euros
    df_gc1['revenue_loss_1'] = df_gc1['rejected_volume'] * price_resampled / 100.  # Convert cents to euros
    df_gc2['revenue_gain_2'] = df_gc2['approved_volume'] * price_resampled / 100.  # Convert cents to euros
    df_gc2['revenue_loss_2'] = df_gc2['rejected_volume'] * price_resampled / 100.  # Convert cents to euros

    # Step 8: Aggregate data for both gate_closures together
    df_combined = df[df['gate_closure'].isin([1, 2])].resample(agg_period).agg({
        'sent_volume': agg_func_dict, 
        'staged_volume': agg_func_dict, 
        'approved_volume': agg_func_dict, 
        'rejected_volume': agg_func_dict
    })

    # Step 9: Calculate combined revenue
    df_combined['revenue_gain'] = df_combined['approved_volume'] * price_resampled / 100.  # Convert cents to euros
    df_combined['revenue_loss'] = df_combined['rejected_volume'] * price_resampled / 100.  # Convert cents to euros

    # Step 10: Rename only volume columns to reflect gate_closure=1, gate_closure=2
    df_gc1.rename(columns=lambda col: f"{col}_1" if 'volume' in col else col, inplace=True)
    df_gc2.rename(columns=lambda col: f"{col}_2" if 'volume' in col else col, inplace=True)

    # Step 11: Merge all three DataFrames together
    df_agg = pd.concat([df_gc1, df_gc2, df_combined], axis=1)

    # Step 12: Return the resulting DataFrame
    return df_agg.reset_index()

def run_aggregation_and_plot(recipient, product, func, period, start_date, end_date):
    """
    # Usage example
    run_aggregation_and_plot(
        recipient=['volue'],
        product=['fcr-d-up'],
        gate_closure=[1, 2],
        func='sum',
        period='D',
        start_date='2024-08-01',
        end_date='2024-09-01'
    )
    """

    # Read the data
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    file_path = os.path.join(base_dir, 'data/', 'processed/')
    os.makedirs(file_path, exist_ok=True)       # Ensure directories exist
    file_name='output.csv'

    fcr = pd.read_csv(file_path + file_name, float_precision='round_trip', na_values=['', 'None', ' '])
    print(f"Data loaded. Number of rows: {fcr.shape[0]}")

    # Call the aggregation function
    df = aggregate_volumes(fcr, recipients=recipient, products=product, agg_func=func,
                           agg_period=period, start_date=start_date, end_date=end_date)
    print(f"Aggregation complete. DataFrame shape: {df.shape}")

    # Calculate dynamic bar width and alpha based on data
    num_bars = len(df)
    try:
        bar_width = 15.0 / num_bars
    except ZeroDivisionError:
        bar_width = 2.0  # Fallback value in case of division by zero    
    alpha_value = 1.0

    # Define the dataset structure
    y_values_volume = [
        [df['staged_volume'].values, df['sent_volume'].values, df['approved_volume'].values, df['rejected_volume'].values],
        [df['staged_volume_1'].values, df['sent_volume_1'].values, df['approved_volume_1'].values, df['rejected_volume_1'].values],
        [df['staged_volume_2'].values, df['sent_volume_2'].values, df['approved_volume_2'].values, df['rejected_volume_2'].values],
    ]
    y_values_revenue = [
        [df['revenue_gain'].values, df['revenue_loss'].values],
        [df['revenue_gain_1'].values, df['revenue_loss_1'].values],
        [df['revenue_gain_2'].values, df['revenue_loss_2'].values],
    ]

    # Save the aggregated data to a CSV file
    csv_save_path = os.path.join(file_path, f"aggregated_data_{'_'.join(recipient)}_{'_'.join(product)}_{start_date}_{end_date}_{period}.csv")
    df.to_csv(csv_save_path, index=False)
    print(f"Aggregated data saved to {csv_save_path}")


    # Plotting
    fig, axes = plt.subplots(3, 2, figsize=(15, 8), sharex=True)
    volume_labels = ["Staged", "Sent", "Approved", "Rejected"]
    revenue_labels = ["Gained", "Lost"]
    volume_colors = ['orange', 'blue', 'forestgreen', 'orangered']
    revenue_colors = ['forestgreen', 'orangered']
    x = df['ts'].values

    # Plot volumes and revenues
    for i in range(3):
        for j, y_volume in enumerate(y_values_volume[i]):
            axes[i, 0].bar(x, y_volume, width=bar_width, label=volume_labels[j], color=volume_colors[j], alpha=alpha_value)
        axes[i, 0].set_ylabel("Volume (MW)")

        for j, y_revenue in enumerate(y_values_revenue[i]):
            axes[i, 1].bar(x, y_revenue, width=bar_width, label=revenue_labels[j], color=revenue_colors[j], alpha=alpha_value)
        axes[i, 1].set_ylabel("Revenue (€)")

    # Add legend and title only to the first row for clarity
    axes[0, 0].set_title(r"$\bf{Recipients = }$"+','.join(recipient)
                        +"\n"+r"$\bf{Products = }$"+','.join(product)
                        +"\n"+r"$\bf{Frequency = }$"+period+"\n")

    axes[0, 1].set_title(r"$\bf{Period = }$"+start_date+" - "+end_date
                        +"\n"+r"$\bf{Total~revenue = }$"+"{:0,.2f}".format(df['revenue_gain'].sum())+" €"
                        +"\n"+r"$\bf{Average~revenue = }$"+"{:0,.2f}".format(df['revenue_gain'].mean())+" €"+"\n")

    axes[0, 0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.18), fancybox=True, shadow=True, ncol=4)
    axes[0, 1].legend(loc='upper center', bbox_to_anchor=(0.5, 1.18), fancybox=True, shadow=True, ncol=2)

    axes[1, 0].text(0.5, 0.98, 'gc=1', transform=axes[1, 0].transAxes, ha='center', bbox=dict(facecolor='white', edgecolor='black',pad=2., linewidth=0.1))
    axes[1, 1].text(0.5, 0.98, 'gc=1', transform=axes[1, 1].transAxes, ha='center', bbox=dict(facecolor='white', edgecolor='black',pad=2., linewidth=0.1))
    axes[-1, 0].text(0.5, 0.98, 'gc=2', transform=axes[-1, 0].transAxes, ha='center', bbox=dict(facecolor='white', edgecolor='black',pad=2., linewidth=0.1))
    axes[-1, 1].text(0.5, 0.98, 'gc=2', transform=axes[-1, 1].transAxes, ha='center', bbox=dict(facecolor='white', edgecolor='black',pad=2., linewidth=0.1))

    # Final adjustments
    axes[-1, 0].set_xlabel("Timestamp")
    axes[-1, 1].set_xlabel("Timestamp")
    plt.tight_layout()
    plt.gcf().autofmt_xdate()
    #plt.show()

    # Save the figure
    save_path = os.path.join(file_path, f"revenue_{'_'.join(recipient)}_{'_'.join(product)}_{start_date}_{end_date}_{period}.pdf")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig.savefig(save_path, dpi=100)
    print(f"Plot saved to {save_path}")

    return fig

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Aggregate and plot FCR data")
    parser.add_argument("--recipient", nargs='+', required=True, help="List of recipients to filter by")
    parser.add_argument("--product", nargs='+', required=True, help="List of products to filter by")
    parser.add_argument("--func", choices=['sum', 'mean', 'both'], default='sum', help="Aggregation function")
    parser.add_argument("--period", default='D', help="Aggregation period ('h'our, 'D'ay [default], 'W'eek, 'M'onth, 'Y'ear)")
    parser.add_argument("--start_date", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end_date", required=True, help="End date (YYYY-MM-DD)")

    args = parser.parse_args()

    # Convert dates to datetime format
    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    except ValueError as e:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    # Run the aggregation and plotting function
    run_aggregation_and_plot(
        args.recipient, 
        args.product, 
        args.func, 
        args.period, 
        args.start_date, 
        args.end_date
        )

if __name__ == "__main__":
    main()