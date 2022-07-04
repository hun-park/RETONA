from preprocess import message
from translate import lookuptable
from inference import inference

# assume 1-channel
class signs:
    azimuth, elevation, magnitude = 0, 0, 0
    def update(self, degrees, magnitude):
        self.azimuth, self.elevation, self.magnitude = degrees[0], degrees[1], magnitude

# preprocess
msg = message("../w_gui/input")

# mode selection
rx_signs, tx_signs = signs(), signs()
if (msg.MODE):
    # ",MO,1" -> manual mode : bypass
    rx_signs.update(msg.RX_DEG, msg.RX_ATT)
    tx_signs.update(msg.TX_DEG, msg.TX_ATT)
else:
    # ",MO,0" -> auto mode : inference
    inference("data/test/test16.csv","data/class.csv",10,"model_dir/cnn.xmodel")

# translate
rx_cmd = lookuptable("../w_board/table").return_bits(rx_signs.azimuth, rx_signs.elevation).to_list()
tx_cmd = lookuptable("../w_board/table").return_bits(tx_signs.azimuth, tx_signs.elevation).to_list()

# send
print(rx_cmd)
print(tx_cmd)