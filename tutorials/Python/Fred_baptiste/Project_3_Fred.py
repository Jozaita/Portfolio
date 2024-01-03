from collections import namedtuple
import datetime

def clean_data(row):
    return row.strip("\n").replace(" ","_").split(",")

def cast_date(date):
    return datetime.datetime.strptime(date,"%m/%d/%Y")

def cast_datatypes(row):
    new_row = []
    datatypes = [int,
                 str,
                 str,
                 str,
                 cast_date,
                 int,
                 str,
                 str,
                 str]
    return (dtype(item_row) for dtype,item_row in zip(datatypes,row))

file = 'nyc_parking_tickets_extract.csv'

with open(file) as f:
    headings = next(f).strip("\n").replace(" ","_").split(",")
    tickets = namedtuple("tickets", headings)

def file_iterator(file):
    with open(file) as f:
        next(f)
        yield from f

def parse_data():

    for raw_row in file_iterator(file):
        row = clean_data(raw_row)
        row = cast_datatypes(row)
        yield tickets(*row)

dict_violations = {}
for f in parse_data():
    try:
        dict_violations[f.Vehicle_Make] = dict_violations[f.Vehicle_Make] + 1
    except KeyError:
        dict_violations[f.Vehicle_Make] = 1


from collections import defaultdict
def violation_sorted():
    dict_v = defaultdict(int)
    for f in parse_data():
        dict_v[f.Vehicle_Make] += 1

    return {make:cnt for make,cnt in sorted(dict_violations.items(),key=lambda x:x[1],reverse=True)}


for key,value in violation_sorted().items():
    print(f"{key};{value}")


