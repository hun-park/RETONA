import numpy as np

def calib_input(iter):
  # from CSV
  x_train = np.array(np.loadtxt('/workspace/proj/cnn/data/x_train3.CSV', delimiter=','))

  # resize and normalize
  x_train = np.reshape(x_train,[-1, 35, 35, 1])
  x_train = x_train.astype(np.int8) / 700

  train_set = x_train

  return {"input_1": train_set}