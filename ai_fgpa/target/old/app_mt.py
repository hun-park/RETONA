from ctypes import *
from typing import List
import numpy as np
import vart
import xir
import threading
import time
import argparse

seperator = "========================================"

def preprocess_fn(train_path):
    '''
    train data pre-processing.
    input arg: path of train data csv file
    return: numpy array
    '''
    # from CSV
    x_train = np.array(np.genfromtxt(train_path, delimiter=','))[:,:]

    # resize and normalize
    x_train = np.reshape(x_train,[-1, 35, 35, 1])
    x_train = x_train.astype(np.int8) / 700

    train_set = x_train

    return train_set


def get_child_subgraph_dpu(graph: "Graph") -> List["Subgraph"]:
    assert graph is not None, "'graph' should not be None."
    root_subgraph = graph.get_root_subgraph()
    assert (root_subgraph is not None), "Failed to get root subgraph of input Graph object."
    if root_subgraph.is_leaf:
        return []
    child_subgraphs = root_subgraph.toposort_child_subgraph()
    assert child_subgraphs is not None and len(child_subgraphs) > 0
    return [
        cs
        for cs in child_subgraphs
        if cs.has_attr("device") and cs.get_attr("device").upper() == "DPU"
    ]


def runDPU(id,start,dpu,trains):

    '''get tensor'''
    inputTensors = dpu.get_input_tensors()
    outputTensors = dpu.get_output_tensors()
    input_ndim = tuple(inputTensors[0].dims)
    output_ndim = tuple(outputTensors[0].dims)

    batchSize = input_ndim[0]

    n_of_trains = len(trains)
    count = 0
    write_index = start
    while count < n_of_trains:
        if (count+batchSize<=n_of_trains):
            runSize = batchSize
        else:
            runSize=n_of_trains-count

        '''prepare batch input/output '''
        outputData = []
        inputData = []
        inputData = [np.empty(input_ndim, dtype=np.float32, order="C")]
        outputData = [np.empty(output_ndim, dtype=np.float32, order="C")]

        '''init input train data to input buffer '''
        for j in range(runSize):
            imageRun = inputData[0]
            imageRun[j, ...] = trains[(count + j) % n_of_trains].reshape(input_ndim[1:])

        '''run with batch '''
        job_id = dpu.execute_async(inputData,outputData)
        dpu.wait(job_id)

        '''store output vectors '''
        for j in range(runSize):
            out_q[write_index] = np.argmax((outputData[0][j]))
            write_index += 1
        count = count + runSize


def app(train_path,label_path,class_path,threads,model):

    runTotal = len(preprocess_fn(train_path))

    global out_q
    out_q = [None] * runTotal

    g = xir.Graph.deserialize(model)
    subgraphs = get_child_subgraph_dpu(g)
    all_dpu_runners = []
    for i in range(threads):
        all_dpu_runners.append(vart.Runner.create_runner(subgraphs[0], "run"))

    ''' preprocess images '''
    print('Pre-processing',runTotal,'train data...')
    trains  = preprocess_fn(train_path)
    labels  = np.array(np.loadtxt(label_path, delimiter=','))
    classes = np.array(np.loadtxt(class_path, delimiter=','))

    '''run threads '''
    print('Starting',threads,'threads...')
    threadAll = []
    start=0
    for i in range(threads):
        if (i==threads-1):
            end = len(trains)
        else:
            end = start+(len(trains)//threads)
        in_q = trains[start:end]
        t1 = threading.Thread(target=runDPU, args=(i,start,all_dpu_runners[i], in_q))
        threadAll.append(t1)
        start=end

    time1 = time.time()
    for x in threadAll:
        x.start()
    for x in threadAll:
        x.join()
    time2 = time.time()
    timetotal = time2 - time1

    fps = float(runTotal / timetotal)
    print("Throughput=%.2f fps, total frames = %.0f, time=%.4f seconds" %(fps, runTotal, timetotal))
    print(seperator)

    ''' post-processing '''
    correct = 0
    wrong = 0
    print('output buffer length:',len(out_q))
    for i in range(len(out_q)):
        prediction = classes[out_q[i]]
        ground_truth = labels[i]
        if (ground_truth==prediction):
            correct += 1
            print('Correct:%d, Prediction:%d, Ground_truth:%d' %(correct,prediction,ground_truth))
        else:
            wrong += 1
            print('Correct:%d, Prediction:%d, Ground_truth:%d' %(wrong,prediction,ground_truth))
    accuracy = correct/len(out_q)
    print(seperator)
    print('Correct:%d, Wrong:%d, Accuracy:%.4f' %(correct,wrong,accuracy))

    return



# only used if script is run as 'main' from command line
def main():

  # construct the argument parser and parse the arguments
  ap = argparse.ArgumentParser()  
  ap.add_argument('-d', '--train_path', type=str, default='data/x_train3.csv',    help='Path to train. Default is ./data/x_train3.csv')
  ap.add_argument('-l', '--label_path', type=str, default='data/y_train3.csv',    help='Path to label. Default is ./data/y_train3.csv')
  ap.add_argument('-c', '--class_path', type=str, default='data/class.csv',       help='Path to class. Default is ./data/class.csv') 
  ap.add_argument('-t', '--threads',    type=int, default=1,                      help='Number of threads. Default is 1')
  ap.add_argument('-m', '--model',      type=str, default='model_dir/cnn.xmodel', help='Path of xmodel. Default is ./model_dir/cnn.xmodel')

  args = ap.parse_args()  
  
  print ('Command line options:')
  print (' --train_path : ', args.train_path)
  print (' --label_path : ', args.label_path)
  print (' --class_path : ', args.class_path)
  print (' --threads    : ', args.threads)
  print (' --model      : ', args.model)

  app(args.train_path,args.label_path,args.class_path,args.threads,args.model)

if __name__ == '__main__':
  main()
