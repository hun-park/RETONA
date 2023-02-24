import gpio
import time
import argparse

def pinset(pinnum, iter):
  gpio.setup(pinnum, gpio.OUT)

  for i in range(iter):
    gpio.output(pinnum, gpio.HIGH)
    time.sleep(2.0)

  return

def main():
  # construct the argument parser and parse the arguments
  ap = argparse.ArgumentParser()  
  ap.add_argument('-n', '--pin_number', type=int, default=0, help='Number of pin. Default is 0')
  ap.add_argument('-i', '--iter_number', type=int, default=1, help='Number of iter. Default is 1')

  args = ap.parse_args()  

  pinset(args.pin_number, args.iter_number)

if __name__ == '__main__':
  main()