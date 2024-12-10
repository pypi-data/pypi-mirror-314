import pandas as pd
import numpy as np
import json

class DataPipeline:
    def __init__(self, df, df_price):
        self.df = df
        self.df_price = df_price

    def process_volume_data(self):
        """Processes volume data by grouping, pivoting, renaming, and merging columns."""
        # Step 1: Group by the necessary columns and sum the 'volume_mw_sum'
        df_grouped = self.df.groupby(['aggregate_id', 'gate_closure', 'version', 'ts', 'event_type'], as_index=False).agg({
            'volume_mw_sum': 'sum'
        })

        # Step 2: Pivot the 'event_type' into separate columns for 'sent', 'staged', 'approved'
        df_pivot = df_grouped.pivot_table(
            index=['aggregate_id', 'gate_closure', 'version', 'ts'], 
            columns='event_type', 
            values='volume_mw_sum',
            fill_value=0.,
            aggfunc='sum'
        ).fillna(0)

        # Step 3: Reset the index to flatten the DataFrame
        df_pivot = df_pivot.reset_index()

        # Step 4: Rename the columns to 'sent', 'staged', 'approved'
        df_pivot.columns.name = None  # Remove the name of the column axis
        df_pivot = df_pivot.rename(columns={
            'BidsApproved': 'approved_volume', 
            'BidsSent': 'sent_volume', 
            'BidsStaged': 'staged_volume'
        })

        # Step 5: Add the 'rejected_volume' column (approved - sent)
        df_pivot['rejected_volume'] = df_pivot['approved_volume'] - df_pivot['sent_volume']

        # Step 6: Merge with the original dataframe if you want to keep other columns
        df_final = pd.merge(self.df, df_pivot, on=['aggregate_id', 'gate_closure', 'version', 'ts'], how='left')

        # Update the main DataFrame to the processed one
        self.df = df_final
        return self.df
    
    def add_price(self, df_ts, df_price_ts):
        """Adds price information based on matching criteria."""
        # Check if the timestamp columns exist
        if df_ts not in self.df.columns:
            raise KeyError(f"Column '{df_ts}' not found in self.df")
        if df_price_ts not in self.df_price.columns:
            raise KeyError(f"Column '{df_price_ts}' not found in self.df_price")

        # Convert to datetime
        self.df[df_ts] = pd.to_datetime(self.df[df_ts], errors='coerce')
        self.df_price[df_price_ts] = pd.to_datetime(self.df_price[df_price_ts], errors='coerce')

        # Proceed with the rest of the merging process
        self.df_price = self.df_price[['start_ts', 'product', 'gate_closure', 'region', 'cents']]
        merged_df = pd.merge(
            self.df,
            self.df_price,
            left_on=['product', 'gate_closure', 'region', df_ts],
            right_on=['product', 'gate_closure', 'region', df_price_ts],
            how='left'
        )
        merged_df.rename(columns={'cents': 'price_cents'}, inplace=True)
        self.df = merged_df[['ts', 'aggregate_id', 'region', 'product', 'recipient', 
                            'gate_closure', 'approved_volume', 'sent_volume', 
                            'staged_volume', 'rejected_volume', 'price_cents']]
        return self

    def add_agg_column(self, column, column_new, function):
        """Adds a new column to the dataframe based on the aggregation function."""
        col_loc = self.df.columns.get_loc(column)

        # Calculate the aggregated values
        col_val = self.df[column].apply(function)

        # Check if the new column already exists
        if column_new in self.df.columns:
            # If it exists, you can choose to overwrite or skip
            print(f"Warning: Column '{column_new}' already exists. Overwriting the existing column.")
        
        # Insert or update the column in the DataFrame
        self.df[column_new] = col_val  # This will replace the column if it exists

        return self
    
    def rename_columns(self, old_names, new_names):
        """Renames columns based on provided old and new names."""
        if len(old_names) != len(new_names):
            raise ValueError("Length of old_names and new_names must be the same.")
        
        col_map = dict(zip(old_names, new_names))
        missing_cols = set(old_names) - set(self.df.columns)
        if missing_cols:
            raise ValueError(f"Columns {missing_cols} do not exist in the DataFrame.")
        
        self.df = self.df.rename(columns=col_map)
        return self

    def extract_json_column(self, dict_col, string=True, drop_original=True):
        """Extracts keys from a JSON column into new columns."""
        
        def fix_json(json_str):
            """Fixes improperly formatted JSON strings (e.g., single quotes)."""
            try:
                # Replace single quotes with double quotes
                return json_str.replace("'", '"')
            except AttributeError:
                # Return as is if not a string
                return json_str

        def safe_json_loads(json_str):
            """Safely loads a JSON string, returning None on failure."""
            try:
                # First, fix the JSON string if necessary
                fixed_json_str = fix_json(json_str)
                return json.loads(fixed_json_str)
            except (json.JSONDecodeError, TypeError) as e:
                # Log or handle errors as needed (return None for failed parsing)
                print(f"Error decoding JSON: {e}")
                return None  # Or you could return an empty dict or a default value

        if string:
            # Apply safe JSON loading to handle malformed strings
            self.df[dict_col] = self.df[dict_col].apply(safe_json_loads)

        # Use pd.json_normalize to extract keys into new columns
        dict_df = pd.json_normalize(self.df[dict_col])

        # Assign new columns directly to the original DataFrame
        for col in dict_df.columns:
            self.df[col] = dict_df[col]

        # Optionally drop the original dictionary column
        if drop_original:
            self.df = self.df.drop(columns=[dict_col])

        return self
    
    def explode_column(self, column):
        """Explodes a list-like column into individual rows."""
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame")
        
        self.df = self.df.explode(column).reset_index(drop=True)
        return self

    def convert_time_column(self, column_name, sort=True, ascending=True):
        """Converts a numeric time column to datetime and optionally sorts the DataFrame."""
        if not np.issubdtype(self.df[column_name].dtype, np.number):
            raise ValueError(f"Column {column_name} does not contain numeric values.")
        
        col_min = self.df[column_name].min()
        col_max = self.df[column_name].max()
        
        # Determine the likely time unit based on both min and max values
        if col_max > 1e18 or col_min > 1e18:  # Likely nanoseconds
            unit = 'ns'
        elif col_max > 1e15 or col_min > 1e15:  # Likely microseconds
            unit = 'us'
        elif col_max > 1e12 or col_min > 1e12:  # Likely milliseconds
            unit = 'ms'
        elif col_max > 1e9 or col_min > 1e9:  # Likely seconds
            unit = 's'
        else:
            raise ValueError(f"Values in {column_name} do not appear to be valid UNIX timestamps.")
        
        # Convert the column to datetime using the inferred unit
        self.df[column_name] = pd.to_datetime(self.df[column_name], unit=unit)

        # Sort the DataFrame if needed
        if sort:
            self.df = self.df.sort_values(by=column_name, ascending=ascending).reset_index(drop=True)

        return self

    def column_list_numpy(self, columns):
        """Converts specified columns into NumPy arrays."""
        for col in columns:
            self.df[col] = [np.array(val) for val in self.df[col].values]
        return self

    def convert_to_cents(self, price_col, currency_col):
        """Converts prices in euros to euro-cents based on the currency column."""
        def convert(row):
            if row[currency_col] == 'EUR':
                return row[price_col] * 100.  # Convert euros to euro-cents
            return row[price_col]  # Leave euro-cents as is
        
        self.df[price_col] = self.df.apply(convert, axis=1)
        return self
    
    
class DataProcessor:
    def __init__(self, file_path, out_dir):
        self.file_path = file_path
        self.out_dir = out_dir

    def load_data(self, file_name):
        df = pd.read_csv(f"{self.file_path}{file_name}")
        #print(f"Loaded data from {file_name}:")
        print(df.head())  # Print the first few rows
        #print("Columns:", df.columns.tolist())  # Print the column names
        print("Data column sample:", df['data'].head())  # Print the first few entries of the 'data' column
        return df

    def clean_data(self, fcr, verbose=False):
        """Clean and preprocess the FCR data."""
        group_columns = ['aggregate_id', 'event_type']
        grouped = fcr.groupby(group_columns, group_keys=False).apply(lambda x: x.sort_values('version'))
        
        rows = []
        print("processing...")
        for name, group in grouped.groupby(group_columns):
            row = group.query('version == version.max()')
            rows.extend(row.to_dict('records'))

        df_clean = pd.DataFrame(rows)
        # Print a preview of the cleaned DataFrame
        if verbose:
            print("\nCleaned Data Preview:")
            print(df_clean.head())  # Show only the first few rows

        return df_clean
    
    def convert_time_columns(self, fcr_df, time_columns):
        """Convert UNIX timestamps to pandas datetime."""
        for col in time_columns:
            fcr_df[col] = pd.to_datetime(fcr_df[col], unit='s')  # Adjust as needed
        return fcr_df

    def pivot_data(self, fcr_df):
        """Pivot the DataFrame to create separate columns for event types."""
        fcr_df.set_index('ts', inplace=True)
        df_pivot = fcr_df.pivot_table(
            index=['ts', 'from_ts', 'to_ts', 'recipient', 'product', 'region', 'gate_closure', 'version', 'aggregate_id'], 
            columns='event_type', 
            values='volume_mw_sum', 
            aggfunc='sum'
        ).fillna(0)
        return df_pivot.reset_index()

    def save_data(self, df, file_name):
        """Save the DataFrame to a CSV file."""
        df.to_csv(self.out_dir + file_name, index=True)

    def process(self, volume=True, price=False):
        """Main processing method."""
        if volume:
            fcr = self.load_data('fcr_bid.csv')
            fcr_clean = self.clean_data(fcr)
            fcr_df = self.convert_time_columns(fcr_clean, ['attr.to_ts', 'attr.from_ts', 'ts'])
            df_pivot = self.pivot_data(fcr_df)
            self.save_data(df_pivot, 'fcr_bid_cleaned.csv')

        if price:
            # Similar logic for price processing
            pass

if __name__ == "__main__":
    processor = DataProcessor(file_path='data/raw/', out_dir='data/processed/')
    processor.process()