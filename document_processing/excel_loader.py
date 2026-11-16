import pandas as pd

def extract_excel(file):
    sheets = pd.read_excel(
        file,
        sheet_name=None
    )

    content = ""

    for sheet_name, df in sheets.items():
        content += f"\nSheet: {sheet_name}\n"
        content += df.to_string(index=False)

    return content