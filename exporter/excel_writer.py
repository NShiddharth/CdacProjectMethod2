import pandas as pd
from typing import List, Dict

def export_to_excel(data: List[Dict], output_path: str) -> None:
    """
    Exports a list of dictionaries to an Excel file using pandas.
    The expected data format is:
    [
        {
            "Paragraph_ID": int,
            "Question_No": int,
            "Question": str,
            "Answer": str
        }, ...
    ]
    """
    if not data:
        print("No data to export.")
        return
        
    df = pd.DataFrame(data)
    
    # Ensure correct column ordering
    columns = ["Paragraph_ID", "Question_No", "Question", "Answer"]
    df = df[columns]
    
    try:
        df.to_excel(output_path, index=False, engine='openpyxl')
        print(f"Successfully exported {len(df)} records to {output_path}")
    except Exception as e:
        print(f"Error exporting to Excel: {e}")
