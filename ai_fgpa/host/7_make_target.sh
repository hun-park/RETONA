echo "-----------------------------------------"
echo "MAKE TARGET STARTED.."
echo "-----------------------------------------"


# remove previous results
rm -rf ${TARGET}

# copy target template to build folder
cp -ar ${TARGET_TEMPLATE} ${BUILD}
mv ${BUILD}/target_template ${TARGET}
echo "  Copied target template to target folder"


# copy elf to target folder
cp ${COMPILE}/*.xmodel ${TARGET}/model_dir/.
echo "  Copied xmodel file(s) to target folder"


mkdir -p ${TARGET}/data
cp -ar /workspace/proj/cnn/data ${TARGET}/data

echo "  Copied images to target folder"

echo "-----------------------------------------"
echo "MAKE TARGET COMPLETED"
echo "-----------------------------------------"

