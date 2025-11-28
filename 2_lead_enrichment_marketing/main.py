import pandas as pd
import os
from dotenv import load_dotenv
from scraper import find_website, scrape_website
from enricher import enrich_company_data
import time

load_dotenv()

def main():
    print("Starting Lead Enrichment Agent...")
    
    input_file = "input.csv"
    output_file = "output.csv"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    df = pd.read_csv(input_file)
    
    # Initialize new columns if they don't exist
    new_cols = ["Website", "Description", "Industry", "Target Audience", "Pricing Model"]
    for col in new_cols:
        if col not in df.columns:
            df[col] = ""

    print(f"Found {len(df)} companies to process.")
    
    processed_df = process_dataframe(df)
    processed_df.to_csv(output_file, index=False)
    print(f"\nDone! Results saved to {output_file}")

def process_dataframe(df, progress_callback=None):
    """
    Processes the dataframe to enrich company data.
    Optional progress_callback(current, total, message) for UI updates.
    """
    # Initialize new columns if they don't exist
    new_cols = ["Website", "Description", "Industry", "Target Audience", "Pricing Model"]
    for col in new_cols:
        if col not in df.columns:
            df[col] = ""
            
    total = len(df)
    
    for index, row in df.iterrows():
        company = row["Company Name"]
        website = row["Website"]
        
        msg = f"Processing: {company}"
        print(msg)
        if progress_callback:
            progress_callback(index + 1, total, msg)
        
        # 1. Find Website if missing
        if pd.isna(website) or website == "":
            website = find_website(company)
            df.at[index, "Website"] = website
            time.sleep(1) # Polite delay
        
        # 2. Scrape
        text = scrape_website(website)
        
        # 3. Enrich
        data = enrich_company_data(company, text)
        
        df.at[index, "Description"] = data.get("description", "")
        df.at[index, "Industry"] = data.get("industry", "")
        df.at[index, "Target Audience"] = data.get("target_audience", "")
        df.at[index, "Pricing Model"] = data.get("pricing_model", "")
        
    return df

if __name__ == "__main__":
    main()
