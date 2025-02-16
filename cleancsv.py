import pandas as pd
import os

def clean_data(df):
    print("Columns in the CSV file:", df.columns)

    df = df.drop(columns=["Company Name"], errors="ignore")

    client_columns = [
        "Clients (Domestic PF/EPFO)", "Clients (Domestic Corporates)", 
        "Clients (Domestic Non-Corporates)", "Clients (Foreign Non-Residents)", 
        "Clients (Foreign FPI)", "Clients (Foreign Others)"
    ]


    df[client_columns] = df[client_columns].apply(pd.to_numeric, errors='coerce')


    aum_columns = [
        "AUM (Domestic PF/EPFO)", "AUM (Domestic Corporates)", "AUM (Domestic Non-Corporates)",
        "AUM (Foreign Non-Residents)", "AUM (Foreign FPI)", "AUM (Foreign Others)", "AUM (Total)"
    ]
    
    missing_columns = [col for col in aum_columns if col not in df.columns]
    if missing_columns:
        print(f"Warning: The following AUM columns are missing: {missing_columns}")
        aum_columns = [col for col in aum_columns if col in df.columns]
    
    df[aum_columns] = df[aum_columns].apply(pd.to_numeric, errors='coerce')


    df[client_columns] = df[client_columns].fillna(0)
    df[aum_columns] = df[aum_columns].fillna(0)

    df['Clients (Total)'] = df[client_columns].sum(axis=1)
    df['AUM (Total)'] = df[aum_columns[:-1]].sum(axis=1)  

    return df

def clean_csv(csv_path):
    if not os.path.isfile(csv_path):
        print("File not found, please check the path.")
        return
    df = pd.read_csv(csv_path)
    df_cleaned = clean_data(df)
    cleaned_csv_path = csv_path.replace(".csv", "_cleaned.csv")
    df_cleaned.to_csv(cleaned_csv_path, index=False)

    print(f"Cleaned CSV file saved to: {cleaned_csv_path}")
    
csv = "C:\\Users\\Nilaksh\\Desktop\\Qode Assignment\\sebi_pms_data.csv"
clean_csv(csv)
