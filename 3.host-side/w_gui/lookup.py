# wget https://bootstrap.pypa.io/pip/3.5/get-pip.py
# python3 get-pip.py
# pip install pandas feather-format
import pandas
import feather

PATH = "../w_board/"
FILE = "table"

lut_csv = pandas.read_csv(PATH + FILE + ".csv")
lut_csv.to_feather(PATH + FILE + ".feather")

self.table = pandas.read_feather(FILE + ".feather")