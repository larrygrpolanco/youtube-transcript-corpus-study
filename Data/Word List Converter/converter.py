import pandas as pd

def process_excel_to_word_families(excel_path, output_path):
    # Read the Excel file
    df = pd.read_excel(excel_path, sheet_name=0)  # Adjust sheet_name if needed

    # Open the output file in UTF-8 encoding
    with open(output_path, 'w', encoding='utf-8') as file:
        for index, row in df.iterrows():
            # Write the headword
            file.write(row['Headword'].upper() + '\n')

            # Write each flemma, indented
            for flemma in row[1:]:
                if not pd.isna(flemma):
                    file.write('\t' + flemma.upper() + '\n')

# Example usage
process_excel_to_word_families('Python/Word List Converter/3_ASWL_380.xlsx', '3_ASWL_380.txt')
