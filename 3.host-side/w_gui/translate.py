import pandas

class lookuptable:
    table = 0
    def __init__(self, FILE):
        self.table = pandas.read_csv(FILE + ".csv")

    def return_bits(self, azimuth, elevation):
        index = int(4.2*azimuth + 0.2*elevation + 220)
        bits = self.table.iloc[index]
        return bits
