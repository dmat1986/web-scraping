import requests
import pandas as pd
from bs4 import BeautifulSoup

'''
Scrapes Winnipeg public school data from 
https://www.winnipegsd.ca/page/9258/school-directory-a-z. 
It reads the table containing the information into a Pandas DataFrame, 
cleans the data, splits the data into different columns where necessary, 
and handles special cases that arise from inconsistencies in the 
source code. Finally, it outputs the data into a TSV file
'''

def Winnipeg_schools() -> None:
    schools = "https://www.winnipegsd.ca/page/9258/school-directory-a-z"
    soup = BeautifulSoup(requests.get(schools).content, "html.parser")

    #Load the data into a DataFrame
    df = pd.read_html(str(soup))[0]

    #Drop rows where all values are missing 
    #and drop the unnamed columns from table
    df = df.dropna(how="all", axis=0).drop(columns=["Unnamed: 0", "Unnamed: 3"])

    df["City"] = 'Winnipeg'

    df["Province"] = 'Manitoba'

    #Get the postal code from the address
    df["Postal Code"] = df["Address"].str.extract(r"(.{3} .{3})$")

    #Remove "school contact information" and "T:" from each cell in
    #the contact column
    df["Contact"] = (
        df["Contact"]
        .str.replace(r"T:\s*", "", regex=True)
        .str.replace("School Contact Information", "")
        .str.strip()
    )

    #Remove the postal code from the cells in the address column
    df["Address"]= (
        df["Address"]
        .str.replace(r"(.{3} .{3})$","",regex=True)
        )

    #Get website URL for each school from the second column
    df["Website"] = [
        #Handle the inconsistency in the source code 
        #for 'Keewatin Prairie Community School' row where the entire URL
        #is given, instead of just the slug
        f'https://www.winnipegsd.ca{a["href"]}'
        if "http" not in a["href"]
        else a["href"]
        #Target the <a> tag in the 2nd child of the 'td' element - i.e. the 
        #2nd column - within the body of the table, and loop through it
        for a in soup.select("tbody td:nth-child(2) a")
    ]

    df.to_csv("LocalLogic.tsv", sep = "\t",index=False)

if __name__ == '__main__':
    Winnipeg_schools()
