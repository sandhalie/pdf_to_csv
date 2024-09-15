import pdfplumber
import pandas as pd
import re
import os

# Path to the folder containing PDF files
pdf_folder_path = "pdftocsvbefore2015/"
csv_file_path = "pdftocsvbefore2015.csv"

# Initialize a dictionary to store the extracted data
extracted_data = {
    'Pay Date': [],
    'Pay Period From': [],
    'Pay Period To': [],
    'Gross Pay': [],
    'Net Pay': [],
    'Text': []  # Field to store the extracted text
}

# Function to extract pay item details
def extract_pay_item_details(text):
    """ Extract Pay Item, Quantity, Rate, Taxable, and Extension from the text. """
    pay_items = re.findall(r"(\w+[\w\s]*?)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", text)
    return pay_items

# Process each PDF file in the folder
for filename in os.listdir(pdf_folder_path):
    if filename.endswith(".pdf"):
        pdf_file_path = os.path.join(pdf_folder_path, filename)
        print(f"Processing {filename}...")

        with pdfplumber.open(pdf_file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Extract and print all text from the page
                page_text = page.extract_text()
                if page_text:
                    # Process text to include only lines from line 10 onward and exclude the last 5 lines
                    lines = page_text.split('\n')
                    start_line = 9
                    end_line = -7  # Exclude the last 7 lines

                    # Ensure we don't exceed the bounds of the list
                    if len(lines) > start_line:
                        if end_line < -len(lines):
                            end_line = -len(lines)
                        text_from_line_10_to_exclude_last_5 = '\n'.join(lines[start_line:end_line])
                    else:
                        text_from_line_10_to_exclude_last_5 = ''

                    # Extract Pay Date, Pay Period From, and Pay Period To
                    pay_date_match = re.search(r"Pay Date:\s*(.*?)\s*Base Rate:", page_text)
                    pay_period_from_match = re.search(r"Pay Period:\s*(.*?)\s*to", page_text)
                    pay_period_to_match = re.search(r"to\s*(\d{2}/\d{2}/\d{4})", page_text)

                    extracted_data['Pay Date'].append(pay_date_match.group(1) if pay_date_match else 'N/A')
                    extracted_data['Pay Period From'].append(pay_period_from_match.group(1) if pay_period_from_match else 'N/A')
                    extracted_data['Pay Period To'].append(pay_period_to_match.group(1) if pay_period_to_match else 'N/A')

                    # Extract Gross Pay and Net Pay from text
                    gross_pay_match = re.search(r"Gross Pay:\s*([\d.]+)", page_text)
                    net_pay_match = re.search(r"Net Pay:\s*([\d.]+)", page_text)

                    extracted_data['Gross Pay'].append(gross_pay_match.group(1) if gross_pay_match else 'N/A')
                    extracted_data['Net Pay'].append(net_pay_match.group(1) if net_pay_match else 'N/A')

                    # Append the processed text to the 'Text' field
                    extracted_data['Text'].append(text_from_line_10_to_exclude_last_5)

# Convert the extracted data to a DataFrame
df = pd.DataFrame(extracted_data)

# Save the DataFrame to a CSV file
df.to_csv(csv_file_path, index=False)

print(f"Data successfully saved to {csv_file_path}")
