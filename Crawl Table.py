#import libraries BeautifulSoup, csv, urllib.request
import bs4 as bs
import urllib.request
import csv


def input_url():
    #try to open the url using urllib if true return the url
    flag = 0

    while (flag == 0):
        try:
            url = input("Enter URL: ")
            urllib.request.urlopen(url)
            flag = 1
        except ValueError:
            print("Sorry, the url entered by you is not correct")
            continue
    return(url)


def input_table_number(tables_in_page):
    while True:
        table_number = int(input("Enter Table :"))
        if(table_number>tables_in_page):
            print("Table number you want to export doesnot exist on page")
            continue
        elif(table_number <=0):
            print("Please enter valid table number")
            continue
        else:
            break
    return(table_number-1)

def write_table_to_csv(url,output_csv,table_number,tables):
    out_file = open(output_csv,'w') #open the csv in which user want tables to be written
    csvwriter = csv.writer(out_file)
    table_rows = tables[table_number].find_all('tr') #find all table rows in ith table
    for tr in table_rows:
    	td = tr.find_all('td') or tr.find_all('th') #append table data to td if the tag is td(table data) or th(table header)
    	row = [i.text for i in td] # extract text from table data(remove tags)
    	print(row) #print the data to terminal
    	csvwriter.writerow(row)#write the data to csv


def main():
    #Check if the url entered by user is correct or not
    #Keep asking for correct url untill the url is valid
    url = input_url()
    source = urllib.request.urlopen(url) #open url using urllib
    soup = bs.BeautifulSoup(source,'lxml') #convert the url in htmltags using beautifulsoup

    #calculate number of tables on current page
    tables = soup.find_all('table')
    tables_in_page = len(tables)

    #Check if the table_number entered by user is correct or not
    #table_number should be a positive integer and less than total tables on age
    table_number = input_table_number(tables_in_page)

    #prompt user to enter the table name in which he wants data to be exported
    output_csv = input("Enter Output (CSV) filename: ")

    #write data to table
    write_table_to_csv(url,output_csv,table_number,tables)

main()
