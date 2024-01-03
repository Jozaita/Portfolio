import csv
from collections import namedtuple
from itertools import islice
import csv
from contextlib import contextmanager
####Constants
## Namedtuple names
files = 'personal_info.csv','cars.csv'

####

class CtxManager():
    def __init__(self,fname,):
        self.fname = fname

    def __enter__(self):
        #Create the iterator
        self._f = open(self.fname,mode="r")
        sample = self._f.read(2000)
        dialect = csv.Sniffer().sniff(sample)
        self._f.seek(0)
        self._reader = csv.reader(self._f,dialect)
        self._nt = namedtuple('Data', map(lambda x: x.lower(),next(self._reader)))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._f.close()
        return False

    def __iter__(self):
        return self

    def __next__(self):
        if self._f.closed:
            raise StopIteration
        else:
            return self._nt(*next(self._reader))

ctx = CtxManager(fname=files[1])
with ctx as file_iterator:
    for row in islice(file_iterator,0,4):
        #print(row)
        pass


@contextmanager
def fileparser(fname):
    file = open(fname,mode="r")
    try:
        sample = file.read(2000)
        dialect = csv.Sniffer().sniff(sample)
        file.seek(0)
        reader = csv.reader(file, dialect)
        nt = namedtuple('Data', map(lambda x: x.lower(), next(reader)))
        yield (nt(*row) for row in reader)
    finally:
        file.close()

with fileparser('cars.csv') as f:
    print(f)
    for row in f:
        print(row)