# compile
compile() {
  
  vai_c_tensorflow \
    --frozen_pb  ${QUANT}/quantize_eval_model.pb \
    --arch       ${ARCH} \
    --output_dir ${COMPILE} \
    --net_name   ${NET_NAME} \
    --options    "{'mode':'${DPU_MODE}'}" \
    --quant_info
}

echo "-----------------------------------------"
echo "COMPILE STARTED.."
echo "-----------------------------------------"

rm -rf ${COMPILE}
mkdir -p ${COMPILE}
compile 2>&1 | tee ${LOG}/${COMP_LOG}

echo "-----------------------------------------"
echo "COMPILE COMPLETED"
echo "-----------------------------------------"
