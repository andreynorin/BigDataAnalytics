#! /bin/bash

echo "Downloading data Google Training Data from S3"

mkdir GoogleTrainingData
cd GoogleTrainingData/
aws s3 cp s3://litter-box/GoogleNewsProcessed/ .  --recursive

echo "Adding Google Training Data to HDFS"

hdfs dfs -mkdir hdfs:///GoogleTrainingData
hdfs dfs -put * hdfs:///GoogleTrainingData

cd ..

echo "Downloading CC-News-Titles from S3"
mkdir CC-News-En-Titles-Only
cd CC-News-En-Titles-Only
aws s3 cp s3://litter-box/CC-News-En-Titles-Only/ . --recursive

echo "Adding CC-News-En-Titles only to HDFS"
hdfs dfs -mkdir hdfs:///CC-News-En-Titles-Only
hdfs dfs -put * hdfs:///CC-News-En-Titles-Only
hdfs dfs -mkdir hdfs:///PredictionResults

echo "Displaying results"
ls -lh
hdfs dfs -ls /
