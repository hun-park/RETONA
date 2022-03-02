# quantize
quantize() {
  
  echo "Making calibration CSV.."  

  vai_q_tensorflow --version

  # quantize
  vai_q_tensorflow quantize \
    --input_frozen_graph ${FREEZE}/${FROZEN_GRAPH} \
		--input_fn           data_input_fn.calib_input \
		--output_dir         ${QUANT} \
	  --input_nodes        ${INPUT_NODE} \
		--output_nodes       ${OUTPUT_NODE} \
		--input_shapes       ${INPUT_SHAPE} \
		--calib_iter         10
}

echo "-----------------------------------------"
echo "QUANTIZE STARTED.."
echo "-----------------------------------------"

rm -rf ${QUANT} 
mkdir -p ${QUANT}
quantize 2>&1 | tee ${LOG}/${QUANT_LOG}


echo "-----------------------------------------"
echo "QUANTIZE COMPLETED"
echo "-----------------------------------------"
