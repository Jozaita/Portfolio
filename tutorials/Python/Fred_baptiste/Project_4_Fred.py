import itertools

from helper_functions_4 import *
from collections import namedtuple
from itertools import chain,compress,groupby
### Constants
## Files
filenames = "personal_info.csv","employment.csv","vehicles.csv","update_status.csv"
## Parsers
personal_parser = str,str,str,str,str
employment_parser = str,str,str,str
vehicle_parser = str,str,str,int
update_status_parser = str,parse_date,parse_date

## Namedtuple names
nt_names = 'Personal_info','Employment','Vehiches','Update_status'
file_parsers = personal_parser,employment_parser,vehicle_parser,update_status_parser

## Field Inclusion /Exclusion
personal_fields_compress = [True,True,True,True,True]
employment_fields_compress = [True,True,True,False]
vehicle_fields_compress = [False,True,True,True]
update_status_fields_compress = [False,True,True]
compress_fields = personal_fields_compress, employment_fields_compress,\
    vehicle_fields_compress, update_status_fields_compress
###

def file_iterator(filename,nt_name,file_parser):
    file = read_file(filename)
    nt_class = namedtuple(nt_name,next(file))
    for row in file:
        yield nt_class(*(func(item) for func, item in zip(file_parser, row)))

def reunite_iterators(filenames,nt_names,file_parsers,compress_fields):
    compress_fields = tuple(chain.from_iterable(compress_fields))
    field_names = compress(itertools.chain.from_iterable(next(read_file(file)) for file in filenames),compress_fields)
    Data = namedtuple("Data",field_names)
    global_zip = zip(*(file_iterator(filename,nt_name,file_parser)
                    for filename,nt_name,file_parser in zip(filenames,nt_names,file_parsers)))
    merged_iterable = (chain.from_iterable(iterable) for iterable in global_zip)
    for row in merged_iterable:
        compressed_row = compress(row,compress_fields)
        yield Data(*compressed_row)



def search_date(iterator,key):
    yield from filter(key,iterator)




data = search_date(reunite_iterators(filenames,nt_names,file_parsers,compress_fields),lambda x: x.last_updated > datetime(2017,1,3))

def group_data(filenames,nt_names,file_parsers,compress_fields,key,gender):
    data = search_date(reunite_iterators(filenames, nt_names, file_parsers, compress_fields),
                       lambda x: x.last_updated > datetime(2017, 1, 3))
    data_f = (row for row in data if row.gender == gender)
    sorted_data_f = sorted(data_f, key=key)
    groups_f = itertools.groupby(sorted_data_f, key=key)
    groups_f_counts = ((item[0], len(list(item[1]))) for item in groups_f)
    return sorted(groups_f_counts,key=lambda x: x[1],reverse=True)

key = lambda x:x.vehicle_make
results_m = group_data(filenames,nt_names,file_parsers,compress_fields,key,"Male")
results_f = group_data(filenames,nt_names,file_parsers,compress_fields,key,"Female")

s




