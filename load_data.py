import os
import glob
import gdown
import pandas as pd

DATA_DIR = "raw_meter_data"

def download_and_combine_data():
    folder_url = "https://drive.google.com/drive/folders/1npGAp5quZO_DgQxlUdB0Jz6P8QJVxPkt?usp=drive_link"
    
    # Download the entire folder if it doesn't already exist
    if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
        print("Downloading folder from Google Drive...")
        gdown.download_folder(url=folder_url, output=DATA_DIR, quiet=False, use_cookies=False)
    
    # Find all CSV files inside the downloaded folder
    all_files = glob.glob(os.path.join(DATA_DIR, "**", "*.csv"), recursive=True)
    
    if not all_files:
        raise FileNotFoundError(f"No CSV files found in {DATA_DIR}")

    print(f"Found {len(all_files)} data files. Merging into DataFrame...")
    
    # Concatenate all daily files into a single master time series DataFrame
    df_list = [pd.read_csv(f) for f in all_files]
    combined_df = pd.concat(df_list, ignore_index=True)
    
    return combined_df

if __name__ == "__main__":
    df = download_and_combine_data()
    print(f"Successfully loaded {len(df):,} total rows across all daily files.")
    print(df.head())
