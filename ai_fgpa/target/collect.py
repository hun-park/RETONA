import numpy as np

unit_collect = 25 * 7
end          = 0

def collect(file_path):
    global end
    end += unit_collect
    data = np.array(np.genfromtxt(file_path, delimiter=','))[0:end]
    if (len(data) < 1225):
        print("Collect data...")
        return False

    else:
        print("Collect data is done")
        return True

def main():
    collect('data/test.csv')

if __name__ == '__main__':
  main()