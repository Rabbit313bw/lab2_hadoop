#!/bin/bash

CONTAINER_NAME=namenode
NAME_FILE=data.parquet
LOCAL_FILE=data/$NAME_FILE
CONTAINER_PATH=./tmp/$NAME_FILE
HDFS_PATH=/$NAME_FILE
BLOCK_SIZE_MB=64
BUFFER_SIZE=4096

# Размер блока в байтах
BLOCK_SIZE_BYTES=$((BLOCK_SIZE_MB * 1024 * 1024))

echo "Check $CONTAINER_NAME running..."
if ! docker ps | grep -q "$CONTAINER_NAME"; then
  echo "Container $CONTAINER_NAME not running"
  exit 1
fi

echo "Copy $LOCAL_FILE into container..."
docker cp "$LOCAL_FILE" "$CONTAINER_NAME:$CONTAINER_PATH"

echo "Load parquet in HDFS with blocksize ${BLOCK_SIZE_MB}MB..."
docker exec -it "$CONTAINER_NAME" hdfs dfs -Ddfs.blocksize="$BLOCK_SIZE_BYTES" -Dio.file.buffer.size="$BUFFER_SIZE" -put -f "$CONTAINER_PATH" "$HDFS_PATH"

echo "List files in HDFS:"
docker exec -it "$CONTAINER_NAME" hdfs dfs -ls /

echo "Blocks info:"
docker exec -it "$CONTAINER_NAME" hdfs fsck "$HDFS_PATH" -files -blocks -locations
