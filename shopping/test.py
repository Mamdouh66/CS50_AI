import csv

# Convert months to numbers
months = {
    'Jan': 0,
    'Feb': 1,
    'Mar': 2,
    'Apr': 3,
    'May': 4,
    'Jun': 5,
    'Jul': 6,
    'Aug': 7,
    'Sep': 8,
    'Oct': 9,
    'Nov': 10,
    'Dec': 11
}

# Reading from file
with open('shopping.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    evidence_list = []
    labels_list = []

    next(csv_reader)

    for line in csv_reader:
        print(line)
