import os
import pdfplumber
import pandas as pd

def extract_pay_slip_data(pdf_path):
    data_rows = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            
            if not text:
                continue

            try:
                # Extract dates and payment details
                pay_period_start = text.split('Pay Period From:')[1].split('To:')[0].strip()
                pay_period_end = text.split('To:')[1].split('Payment Date:')[0].strip()
                payment_date = text.split('Payment Date:')[1].split('\n')[0].strip()
                
                gross_pay = text.split('GROSS PAY:')[1].split('\n')[0].strip().replace('$', '')
                net_pay = text.split('NET PAY:')[1].split('\n')[0].strip().replace('$', '')

                # Extract table data
                for table in page.extract_tables():
                    for row in table:
                        if table.index(row) == 0:
                            continue

                        data_row = [pay_period_start, pay_period_end, payment_date, gross_pay, net_pay]
                        data_row.extend(row[1:])
                        data_rows.append(data_row)
            except IndexError:
                print(f"Error processing file {pdf_path}: Text extraction issues.")

    print(f"Number of rows extracted from {pdf_path}: {len(data_rows)}")
    return data_rows

def process_pdfs_in_folder(folder_path, output_csv_path):
    all_data_rows = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            if not os.path.exists(pdf_path):
                print(f"File not found: {pdf_path}")
                continue

            print(f"Processing file: {pdf_path}")
            data_rows = extract_pay_slip_data(pdf_path)
            all_data_rows.extend(data_rows)

    if all_data_rows:
        df = pd.DataFrame(all_data_rows)
        df.to_csv(output_csv_path, index=False, header=False)
        print(f"Data extracted and saved to {output_csv_path}")
    else:
        print("No data extracted.")

# Example usage
folder_path = r'C:\Users\sandh\Downloads\pdf to csv\pdftocsvafter2015'  # Replace with your folder path
output_csv_path = r'C:\Users\sandh\Downloads\pdf to csv\pdftocsvafter2015.csv'  # Replace with your desired output CSV path
process_pdfs_in_folder(folder_path, output_csv_path)
