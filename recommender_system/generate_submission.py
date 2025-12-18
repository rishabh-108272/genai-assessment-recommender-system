import pandas as pd
import csv
from input_handler import process_input

INPUT_TEST_FILE = "evaluation/test_dataset.csv"
OUTPUT_CSV = "shl_submission.csv"

def generate_csv():
    # Read with keep_default_na=False to prevent "None" strings
    test_df = pd.read_csv(INPUT_TEST_FILE, keep_default_na=False)

    rows = []

    for _, row in test_df.iterrows():
        # DO NOT .strip() or modify the string in any way
        query = row["Query"]

        recommendations = process_input(query=query)
        
        # Limit to 10 as per your MAX_REC
        recommendations = recommendations[:10]

        for rec in recommendations:
            rows.append({
                "Query": query,
                "Assessment_url": rec["URL"]
            })

    submission_df = pd.DataFrame(rows)
    
    # Critical: Use quoting=csv.QUOTE_ALL to wrap the multi-line queries 
    # and lineterminator='\n' to ensure consistency across OS (Mac/Windows)
    submission_df.to_csv(
        OUTPUT_CSV, 
        index=False, 
        quoting=csv.QUOTE_ALL, 
        encoding='utf-8',
        lineterminator='\n' 
    )

    print(f"Submission CSV generated with {len(submission_df)} rows.")

if __name__ == "__main__":
    generate_csv()