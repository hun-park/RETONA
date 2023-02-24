import numpy as np
import tensorflow as tf
import os
import sys
import argparse
from cnn import cnn

# Silence TensorFlow messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# workaround for TF1.15 bug "Could not create cudnn handle: CUDNN_STATUS_INTERNAL_ERROR"
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

DIVIDER = '-----------------------------------------'

def train(input_height,input_width,input_chan,batchsize,epochs,keras_hdf5,tboard):

    # from CSV
    x_train = np.array(np.loadtxt('/workspace/proj/cnn/data/x_train3.CSV', delimiter=','))
    y_train = np.array(np.loadtxt('/workspace/proj/cnn/data/y_train3.CSV', delimiter=','))
    x_test = np.array(np.genfromtxt('/workspace/proj/cnn/data/x_test3.CSV', delimiter=','))[:,:]
    y_test = np.array(np.loadtxt('/workspace/proj/cnn/data/y_test3.CSV', delimiter=','))

    # resize and normalize
    x_train = np.reshape(x_train,[-1, 35, 35, 1])
    x_test = np.reshape(x_test,[-1, 35, 35, 1])
    x_train = x_train.astype(np.int8) / 700
    x_test = x_test.astype(np.int8) / 700

    model = cnn((input_height,input_width,input_chan), len(np.unique(y_train)), 4, 2, 64, 0.2)

    # prints a layer-by-layer summary of the network
    print('\n'+DIVIDER)
    print(' Model Summary')
    print(DIVIDER)
    print(model.summary())

    '''
    Callbacks
    '''
    chkpt_call = tf.keras.callbacks.ModelCheckpoint(filepath=keras_hdf5,
                                 monitor='val_acc',
                                 verbose=1,
                                 save_best_only=True)

    '''
    Optimizer
    '''

    # loss function for one-hot vector
    # model.compile(optimizer='adam',
    #             loss='categorical_crossentropy',
    #             metrics=['accuracy'])

    # loss function for integer
    model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

    model.fit(x_train, y_train, validation_split=0.2, epochs=epochs, callbacks=[chkpt_call], verbose=1)
    # tf.saved_model.save(model, "/workspace/proj/cnn/build/saved/")

    print('\n'+DIVIDER)
    print(' Evaluate model accuracy with validation set..')
    print(DIVIDER)

    '''
    Evaluation
    '''

    scores = model.evaluate(x=x_test, y=y_test, batch_size=batchsize, verbose=0)
    print ('Evaluation Loss    : ', scores[0])
    print ('Evaluation Accuracy: ', scores[1])

    return

def run_main():
    
    print('\n'+DIVIDER)
    print('Keras version      : ',tf.keras.__version__)
    print('TensorFlow version : ',tf.__version__)
    print(sys.version)
    print(DIVIDER)

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('-ih', '--input_height',
                    type=int,
                    default='35',
    	            help='Input image height in pixels.')
    ap.add_argument('-iw', '--input_width',
                    type=int,
                    default='35',
    	            help='Input image width in pixels.')
    ap.add_argument('-ic', '--input_chan',
                    type=int,
                    default='1',
    	            help='Number of input image channels.')
    ap.add_argument('-b', '--batchsize',
                    type=int,
                    default=32,
    	            help='Training batchsize. Must be an integer. Default is 32.')
    ap.add_argument('-e', '--epochs',
                    type=int,
                    default=10,
    	            help='number of training epochs. Must be an integer. Default is 10.')
    ap.add_argument('-kh', '--keras_hdf5',
                    type=str,
                    default='./model.hdf5',
    	            help='path of Keras HDF5 file - must include file name. Default is ./model.hdf5')
    ap.add_argument('-tb', '--tboard',
                    type=str,
                    default='./tb_logs',
    	            help='path to folder for saving TensorBoard data. Default is ./tb_logs.')    
    args = ap.parse_args()


    print(' Command line options:')
    print ('--input_height : ',args.input_height)
    print ('--input_width  : ',args.input_width)
    print ('--input_chan   : ',args.input_chan)
    print ('--batchsize    : ',args.batchsize)
    print ('--epochs       : ',args.epochs)
    print ('--keras_hdf5   : ',args.keras_hdf5)
    print ('--tboard       : ',args.tboard)
    print(DIVIDER)

    train(args.input_height,args.input_width,args.input_chan,args.batchsize,args.epochs,args.keras_hdf5,args.tboard)

if __name__ == '__main__':
    run_main()
