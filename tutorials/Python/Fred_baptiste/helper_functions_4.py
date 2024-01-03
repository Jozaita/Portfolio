import csv
from datetime import datetime
from functools import reduce

def read_file(file_name,*,delimiter=",",quotechar='"',include_header=True):
    with open(file_name) as f:
        rows = csv.reader(f,delimiter=",",quotechar='"')
        if not include_header:
            next(f)
        yield from rows

def parse_date(value,*,fmt="%Y-%m-%dT%H:%M:%SZ"):
    return datetime.strptime(value,fmt)


def check_ssn(global_zip):
    return reduce(lambda x,y: x==y,global_zip)