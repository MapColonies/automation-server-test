#!/bin/bash

export DEV_MODE=true # on dev environment some tests not working
export BEST_LAYER=http://10.28.11.95:8080/service?REQUEST=GetMap&SERVICE=WMS&LAYERS=combined_layers
export OUTPUT_EXPORT_PATH=/mnt/outputs
export DEBUG_LOGS=1 # delete this env to see only info+ level logs without debug
export SERVICES_URL=http://10.28.11.49
export FILE_LOGS=1
export LOGS_OUTPUT=/tmp/mc_logs

#S3 configuration
export S3_EXPORT_STORAGE_MODE=TRUE
export S3_ACCESS_KEY=raster
export S3_SECRET_KEY=rasterPassword
export S3_END_POINT=http://10.28.11.123:9000/minio/
export S3_BUCKET_NAME=mapping-images
export S3_DOWNLOAD_DIR=/tmp


mkdir -p "/tmp/mc_logs"

echo "Start local running of test"
pytest server_automation/tests/test_exporter_tool.py
echo $?