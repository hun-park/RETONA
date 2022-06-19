class message:
    MODE, RX_DEG, RX_ATT, TX_DEG, TX_ATT = 0, 0, 0, 0, 0
    def __init__(self, FILE):
        with open(FILE,"r") as f:
            receive = f.read()

        refined = receive.split(",")[1:]

        self.MODE = refined[refined.index("MO") + 1]
        if (self.MODE == '1'):
            self.RX_DEG  = [int(x) for x in refined[refined.index("RP") + 1:refined.index("RP") + 3]]
            self.TX_DEG  = [int(x) for x in refined[refined.index("TP") + 1:refined.index("TP") + 3]]

            self.RX_ATT  = int(refined[refined.index("RA") + 1])
            self.TX_ATT  = int(refined[refined.index("TA") + 1])
