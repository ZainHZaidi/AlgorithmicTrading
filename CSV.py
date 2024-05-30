import csv

with open('dat.csv', 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile, delimiter = " ", quotechar = ", ")


    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
