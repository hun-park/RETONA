import sys
import os
import argparse
import numpy as np
import tensorflow as tf
from progressbar import ProgressBar

# reduce TensorFlow messages in console
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# workaround for TF1.15 bug "Could not create cudnn handle: CUDNN_STATUS_INTERNAL_ERROR"
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

from tensorflow.keras.utils import to_categorical
import tensorflow.contrib.decent_q

def graph_eval(input_graph_def, graph, input_node, output_node, batchsize):

    input_graph_def.ParseFromString(tf.io.gfile.GFile(graph, "rb").read())

    # dataset    
    x_test = np.array(np.genfromtxt('/workspace/proj/cnn/data/x_test3.CSV', delimiter=','))[:,:]
    y_test = np.array(np.loadtxt('/workspace/proj/cnn/data/y_test3.CSV', delimiter=','))
    y_test = to_categorical(y_test)

    # resize and normalize
    x_test = np.reshape(x_test,[-1, 35, 35, 1])
    x_test = x_test.astype(np.int8) / 700

    total_batches = int(len(x_test)/batchsize)

    tf.import_graph_def(input_graph_def,name = '')

    # Get input placeholders & tensors
    images_in = tf.compat.v1.get_default_graph().get_tensor_by_name(input_node+':0')
    labels = tf.compat.v1.placeholder(tf.int32,shape = [32,25])

    # get output tensors
    logits = tf.compat.v1.get_default_graph().get_tensor_by_name(output_node+':0')
    predicted_logit = tf.argmax(input=logits, axis=1, output_type=tf.int32)
    ground_truth_label = tf.argmax(labels, 1, output_type=tf.int32)

    # Define the metric and update operations
    tf_metric, tf_metric_update = tf.compat.v1.metrics.accuracy(labels=ground_truth_label,
                                                                predictions=predicted_logit,
                                                                name='acc')

    with tf.compat.v1.Session() as sess:
        progress = ProgressBar()
        
        sess.run(tf.compat.v1.initializers.global_variables())
        sess.run(tf.compat.v1.initializers.local_variables())

        # process all batches
        for i in progress(range(0,total_batches)):

            # fetch a batch from validation dataset
            x_batch, y_batch = x_test[i*batchsize:i*batchsize+batchsize], \
                               y_test[i*batchsize:i*batchsize+batchsize]

            # Run graph for accuracy node
            feed_dict={images_in: x_batch, labels: y_batch}
            acc = sess.run(tf_metric_update, feed_dict)

        print ('Graph accuracy with validation dataset: {:1.4f}'.format(acc))

    return



def main():

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()

    ap.add_argument('--graph',
                    type=str,
                    default='./quantize_results/quantize_eval_model.pb',
                    help='graph file (.pb) to be evaluated.')
    ap.add_argument('--input_node',
                    type=str,
                    default='Reshape',
                    help='input node.')
    ap.add_argument('--output_node',
                    type=str,
                    default='dense_1/BiasAdd',
                    help='output node.')
    ap.add_argument('-b', '--batchsize',
                    type=int,
                    default=1,
                    help='Evaluation batchsize, must be integer value. Default is 1')  
    ap.add_argument('--gpu',
                    type=str,
                    default='0',
                    help='gpu device id.')

    args = ap.parse_args()  

    print('\n------------------------------------')
    print('TensorFlow version : ',tf.__version__)
    print(sys.version)
    print('------------------------------------')
    print ('Command line options:')
    print (' --graph      : ', args.graph)
    print (' --input_node : ', args.input_node)
    print (' --output_node: ', args.output_node)
    print (' --batchsize  : ', args.batchsize)
    print (' --gpu        : ', args.gpu)
    print('------------------------------------\n')


    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu
    input_graph_def = tf.Graph().as_graph_def()
    graph_eval(input_graph_def, args.graph, args.input_node, args.output_node, args.batchsize)


if __name__ ==  "__main__":
    main()
