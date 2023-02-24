conda activate vitis-ai-tensorflow

# folders
export BUILD=./build
export TARGET_TEMPLATE=./target_template
export TARGET=${BUILD}/target
export LOG=${BUILD}/logs
export TB_LOG=${BUILD}/tb_logs
export KERAS=${BUILD}/keras_model
export FREEZE=${BUILD}/freeze
export QUANT=${BUILD}/quantize
export COMPILE=${BUILD}/compile/
export TFCKPT_DIR=${BUILD}/tf_chkpt

# make the necessary folders
mkdir -p ${KERAS}
mkdir -p ${LOG}

# logs & results files
export TRAIN_LOG=train.log
export KERAS_LOG=keras_2_tf.log
export FREEZE_LOG=freeze.log
export EVAL_FR_LOG=eval_frozen_graph.log
export QUANT_LOG=quant.log
export COMP_LOG=compile.log

# Keras checkpoint file
export K_MODEL=k_model.h5

# TensorFlow files
export FROZEN_GRAPH=frozen_graph.pb
export TFCKPT=tf_float.ckpt

# network parameters
export INPUT_HEIGHT=35
export INPUT_WIDTH=35
export INPUT_CHAN=1
export INPUT_SHAPE=?,${INPUT_HEIGHT},${INPUT_WIDTH},${INPUT_CHAN}
export INPUT_NODE=input_1
export OUTPUT_NODE=softmax/Softmax
export NET_NAME=cnn

# training parameters
export EPOCHS=10
export BATCHSIZE=32
export LEARNRATE=0.001

# target board
export BOARD=ZCU102
export ARCH=/opt/vitis_ai/compiler/arch/DPUCZDX8G/${BOARD}/arch.json


# DPU mode - best performance with DPU_MODE = normal
export DPU_MODE=normal
#export DPU_MODE=debug
