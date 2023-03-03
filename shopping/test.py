import csv

# Convert months to numbers
months = {
    'Jan': 0,
    'Feb': 1,
    'Mar': 2,
    'Apr': 3,
    'May': 4,
    'June': 5,
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

    non_neumirc_evidence_list = []
    evidence_list = []
    labels_list = []

    next(csv_reader)

    for line in csv_reader:
        non_neumirc_evidence_list.append(line[:-1:])
        labels_list.append(1 if line[-1:][0] == "TRUE" else 0)

    for evidence in non_neumirc_evidence_list:
        temp = []
        ints = [0, 2, 4, 11, 12, 13, 14]
        floats = [1, 3, 5, 6, 7, 8, 9]
        temp.append(int(evidence[0]))
        temp.append(float(evidence[1]))
        temp.append(int(evidence[2]))
        temp.append(float(evidence[3]))
        temp.append(int(evidence[4]))
        temp.append(float(evidence[5]))
        temp.append(float(evidence[6]))
        temp.append(float(evidence[7]))
        temp.append(float(evidence[8]))
        temp.append(float(evidence[9]))
        temp.append(int(months[evidence[10]]))  # Months
        temp.append(int(evidence[11]))
        temp.append(int(evidence[12]))
        temp.append(int(evidence[13]))
        temp.append(int(evidence[14]))
        temp.append(1 if evidence[15] == "Returning_Visitor" else 0)  # V_Type
        temp.append(1 if evidence[16] == "TRUE" else 0)  # Weekend
        evidence_list.append(temp)
