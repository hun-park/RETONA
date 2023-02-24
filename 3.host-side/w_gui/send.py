PATH = "../w_gui/"
FILE = "input"

message = [
    "MO","1",
    "RP","45,35",
    "RA","10",
    "TP","30,35",
    "TA","10"
]
with open(PATH + FILE,"w") as f:
    for word in message:
        f.write("," + word)