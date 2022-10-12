This is a Python3 script which scrapes Winnipeg public school data from https://www.winnipegsd.ca/page/9258/school-directory-a-z. It reads the table containing the information into a Pandas DataFrame, cleans the data, splits the data into different columns where necessary, and handles special cases that arise from inconsistencies in the source code. Finally, it outputs the data into a TSV file with the following fields:

- Name

- Street Address

- City

- Province

- Postal Code

- Phone Number

- Grades Offered

- Website

Python libraries used in the script:

- Requests

- Pandas

- BeautifulSoup
