# import gpio as GPIO
import time
# @issue add multi-thread
import threading
import collect
import inference

# variable for represent state (or case)
case        = 'A'
# variable for represent initial phase (pi, theta)
init_status = (0,0)
# variable for represent current phase (pi, theta)
cur_status  = init_status
# variable for represent whether collect data is done
# True  : collect data is done
# False : collect data is yet
clct_status = False
# variable for represent data path
data_path   = 'data/test/test16.csv'
# variable for represent class path
class_path  = 'data/class.csv'
# variable for represent model path
model       = 'model_dir/cnn.xmodel'
# variable for represent number of threads
threads     = 1
# variable for represent system clock
total_clk   = 0
# variable for represent unit time during system
unit_time   = 0.5

class phase:
    unit_deg        = 5
    pi_low, pi_high = 0, 175
    th_low, th_high = 0, 175

    def __init__(self, file_path):
        f = open(file_path, 'r')
        lines = f.readlines()
        self.bits = {}
        self.logs = {}
        for line in lines:
            word = line.split(',')
            pi, theta = int(word[0]), int(word[1])
            bit_array = (word[2], word[3], word[4], word[5], word[6], word[7][:-1])
            self.bits[(pi, theta)] = bit_array
        f.close
    
    def fromstatus(self, cur_status):
        return cur_status[0], cur_status[1]

    def keep(self, cur_time, cur_status):
        self.logs[cur_time] = cur_status

    def phaseshift(self, cur_status, increase):
        cur_pi, cur_th = self.fromstatus(cur_status)
        if increase:
            if cur_th < self.th_high:
                next_pi, next_th = cur_pi, cur_th + self.unit_deg
            else:
                next_pi, next_th = (cur_pi + self.unit_deg) if cur_pi < self.pi_high else self.pi_low, self.th_low
        else:
            if cur_th > self.th_low:
                next_pi, next_th = cur_pi, cur_th - self.unit_deg
            else:
                next_pi, next_th = (cur_pi - self.unit_deg) if cur_pi > self.pi_low else self.pi_high, self.th_high
        next_status = [next_pi, next_th]
        return next_status


def loop():
    global case
    global cur_status
    global clct_status
    global data_path
    global class_path
    global total_clk
    # en = GPIO.setup(pin=357,mode=GPIO.IN)
    PHASE.keep(total_clk, cur_status)
    total_clk += 1
    # en = GPIO.setup(pin=357,mode=GPIO.IN)
    en = True if total_clk == 160 else False

    if (en):
        case = 'B'

    if (case == 'A'):
        time.sleep(unit_time)
        # move next phase
        cur_status  = PHASE.phaseshift(cur_status, True)
        cur_pi, cur_th = PHASE.fromstatus(cur_status)
        print('[CLK:%3d] case A) Enable:%d, Collect:%d, [PI:%3d, THETA:%3d], Control Bits:%s' %(total_clk,en,clct_status,cur_pi,cur_th,PHASE.bits[(cur_pi,cur_th)]))
        # return control_bits for move next phase
        return PHASE.bits[(cur_pi,cur_th)]

    elif (case == 'B'):
        time.sleep(unit_time)
        # collect process returns boolean clct_status
        clct_status = collect.collect(data_path)
        # move next phase
        cur_status = PHASE.phaseshift(cur_status, False)
        cur_pi, cur_th = PHASE.fromstatus(cur_status)
        print('[CLK:%3d] case A) Enable:%d, Collect:%d, [PI:%3d, THETA:%3d], Control Bits:%s' %(total_clk,en,clct_status,cur_pi,cur_th,PHASE.bits[(cur_pi,cur_th)]))
        # if collect data is done
        # case C : inference
        # if collect data is yet
        # case B : collect data
        if (clct_status):
            case = 'C'
            clct_status = False
        else:
            case = 'B'
        # return control_bits for move next phase
        return PHASE.bits[(cur_pi,cur_th)]

    elif (case == 'C'):
        time.sleep(unit_time)
        # inference to hot time
        hot_time = inference.inference(data_path,class_path,threads,model)
        # hash log data from hot time for move next phase
        cur_status = PHASE.logs[hot_time]
        cur_pi, cur_th = PHASE.fromstatus(cur_status)
        print("log at [%3d]: %s" %(hot_time, PHASE.logs[hot_time]))
        print('[CLK:%3d] case A) Enable:%d, Collect:%d, [PI:%3d, THETA:%3d], Control Bits:%s' %(total_clk,en,clct_status,cur_pi,cur_th,PHASE.bits[(cur_pi,cur_th)]))
        case = 'A'
        # return control_bits for move next phase
        return PHASE.bits[(cur_pi,cur_th)]

def main():
    # generator.py makes csv control_bits file
    global PHASE
    PHASE = phase('data/control_bits.csv')

    while(1):
        loop()

if __name__ == '__main__':
    main()