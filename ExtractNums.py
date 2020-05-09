import glob
import os
import re
from datetime import datetime

from tika import parser

pattern = r"(?P<date>\w+\s+\w+\s+\w+)\s+(?P<time>\d+:\d+:\d+)\s+(?P<num>\d{1,})\s+(?P<country>[A-Za-z]+\s?[A-Za-z]+)?\s?(?P<etime>\d+:\d+:\d+)\s+(?P<cost>[\d+\.]+)"
# pdfs_path = 'res'
# processed_path = 'processed'
extension = '.txt'
processed_prefix = '_processed_'
scraped_prefix = '_scraped_'


# regex match and processor
def filter_to_file(filename):
    parentlist = []

    with open(filename, "r") as f:

        lines = f.readlines()

        for line in lines:
            match = re.search(pattern, line)
            if match:
                data = match.groupdict()
                parentlist.append(data)

    # write data to a file appended with datetime
    filename = filename.rsplit('_')[0]
    date_time = datetime.utcnow().strftime('%m_%d_%H%M%S%f')[:-3]
    processed_file_name = filename + processed_prefix + date_time + extension
    with open(processed_file_name, "w+") as p:
        # loop over the children in the list
        for child in parentlist:
            if child.get('country') is None:
                child["country"] = 'Local'

            # Build the string
            line_format = f"{child['date']},{child['time']},\'{child['num']},{child['country']},{child['etime']},{child['cost']}\n"
            # Write the string to the file
            print(f'Writing: {line_format} to {processed_file_name}')
            p.write(line_format)


def read_pdf_and_write_to_txt(filepath):
    if filepath:
        # F-Strings can be used everywhere
        print(f'Filepath received: {filepath}')
        # parse the raw content
        raw_content = parser.from_file(filepath)
        # making the text file as the input received
        filename = filepath.rsplit('.')[0] + scraped_prefix + extension
        # Filter false values like empty strings
        # Give it to a list
        process_content = list(filter(None, raw_content.get('content').split("\n")))

        with open(filename, "w+") as f:
            # Loop over the lines
            for line in process_content:
                # Process the line here to avoid DRY
                f.write(line.encode("ascii", "ignore").decode() + "\n")
            print("Wrote scraped data to file")

            # could add the PDF's in a folder loop through the filenames and store them in the last format needed

            # raw_get.get('content') => Is a Dictionary key the split is to split after linebreaks
            # The filter function will filter all empty or non-truthy content such as ''
            # Cast the filter function to the list


def readfiles(path):
    os.chdir(path)
    pdfs = []
    for file in glob.glob("*.pdf"):
        print(file)
        pdfs.append(file)
    return pdfs


pdfs = readfiles('res')
for pdf in pdfs:
    print(f'file_path PDF: {pdf}')
    read_pdf_and_write_to_txt(pdf)
    pdf = pdf.rsplit('.')[0] + scraped_prefix + extension
    filter_to_file(pdf)
