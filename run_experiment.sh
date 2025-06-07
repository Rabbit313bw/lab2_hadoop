#!/bin/bash


cd datanode_1
bash run_container.sh
bash upload_to_hdfs.sh
bash run_spark.sh
docker-compose down

cd ../datanode_3
bash run_container.sh
bash upload_to_hdfs.sh
bash run_spark.sh
docker-compose down

cd ../
python3 collect_results.py
