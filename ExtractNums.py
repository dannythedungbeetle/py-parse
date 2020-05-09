import re

from tika import parser

pattern = r"(?P<date>\w+\s+\w+\s+\w+)\s+(?P<time>\d+:\d+:\d+)\s+(?P<num>\d{1,})\s+(?P<country>[A-Za-z]+\s?[A-Za-z]+)?\s?(?P<etime>\d+:\d+:\d+)\s+(?P<cost>[\d+\.]+)"


def filter_to_file(filename):
    parentlist = []

    with open(filename, "r") as f:

        lines = f.readlines()

        for line in lines:
            match = re.search(pattern, line)
            if match:
                data = match.groupdict()
                parentlist.append(data)

    # write data to a file
    with open("processed.txt", "w+") as p:
        # loop over the children in the list
        for child in parentlist:
            if child.get('country') is None:
                child["country"] = 'Local'

            # Build the string
            line_format = f"{child['date']},{child['time']},\'{child['num']},{child['country']},{child['etime']},{child['cost']}\n"
            # Write the string to the file
            print(f'Writing: {line_format}')
            p.write(line_format)


def read_pdf_and_write_to_txt(filepath):
    if filepath:
        # F-Strings can be used everywhere
        print(f'Filepath received: {filepath}')
        # parse the raw content
        raw_content = parser.from_file(filepath)

        # Filter false values like empty strings
        # Give it to a list
        process_content = list(filter(None, raw_content.get('content').split("\n")))

        with open("scraped.txt", "w+") as f:
            # Loop over the lines
            for line in process_content:
                # Process the line here to avoid DRY
                f.write(line.encode("ascii", "ignore").decode() + "\n")
            print("Wrote to file")

            # could add the PDF's in a folder loop through the filenames and store them in the last format needed

            # raw_get.get('content') => Is a Dictionary key the split is to split after linebreaks
            # The filter function will filter all empty or non-truthy content such as ''
            # Cast the filter function to the list

    # scraped_txt_file.close()


read_pdf_and_write_to_txt('res\\res2.pdf')
filter_to_file("scraped.txt")
