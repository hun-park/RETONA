# import tensorflow as tf
# converter = tf.lite.TFLiteConverter.from_saved_model("/workspace/proj/cnn/build/saved")
# converter.optimizations = [tf.lite.Optimize.DEFAULT]
# tflite_quant_model = converter.convert()

import tensorflow as tf
import numpy as np

def representative_data_gen():
  for input_value in tf.data.Dataset.from_tensor_slices(x_train).batch(1).take(100):
    yield [input_value]

x_train = np.array(np.loadtxt('/workspace/proj/cnn/data/x_train3.CSV', delimiter=','))
x_train = np.reshape(x_train,[-1, 35, 35, 1])
x_train = x_train.astype(np.int8) / 700

converter = tf.lite.TFLiteConverter.from_saved_model("/workspace/proj/cnn/build/saved")
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_data_gen

# Ensure that if any ops can't be quantized, the converter throws an error
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
# converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8, tf.lite.OpsSet.SELECT_TF_OPS]
# converter.allow_custom_ops=True

# Set the input and output tensors to uint8 (APIs added in r2.3)
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8

tflite_model_quant = converter.convert()

open("/workspace/proj/cnn/build/quantize/q_model.tlite", "wb").write(tflite_model_quant)