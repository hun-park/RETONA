TF_CPP_MIN_LOG_LEVEL=3

# convert keras model to frozen graph
keras_2_tf() {
  python keras_2_tf.py \
    --keras_hdf5 ${KERAS}/${K_MODEL} \
    --tf_ckpt    ${TFCKPT_DIR}/${TFCKPT}  
}

freeze() {
  freeze_graph \
    --input_meta_graph  ${TFCKPT_DIR}/${TFCKPT}.meta \
    --input_checkpoint  ${TFCKPT_DIR}/${TFCKPT} \
    --output_graph      ${FREEZE}/${FROZEN_GRAPH} \
    --output_node_names ${OUTPUT_NODE} \
    --input_binary      true
}

echo "-----------------------------------------"
echo "CONVERTING KERAS MODEL TO TF CHECKPOINT.."
echo "-----------------------------------------"

rm -rf ${TFCKPT_DIR}
mkdir -p ${TFCKPT_DIR}
keras_2_tf 2>&1 | tee ${LOG}/${KERAS_LOG}

echo "-----------------------------------------"
echo "FINISHED KERAS MODEL CONVERSION"
echo "-----------------------------------------"

echo "-----------------------------------------"
echo "FREEZING THE GRAPH.."
echo "-----------------------------------------"

rm -rf ${FREEZE}
mkdir -p ${FREEZE}
freeze 2>&1 | tee ${LOG}/${FREEZE_LOG}

echo "-----------------------------------------"
echo "FREEZE GRAPH COMPLETED"
echo "-----------------------------------------"
