#!/bin/bash
set -x -e

echo -e 'export PYSPARK_PYTHON=/usr/bin/python3
export HADOOP_CONF_DIR=/etc/hadoop/conf
export SPARK_JARS_DIR=/usr/lib/spark/jars
export SPARK_HOME=/usr/lib/spark' >> $HOME/.bashrc && source $HOME/.bashrc

sudo python3 -m pip install awscli boto spark-nlp sklearn spark-sklearn

sudo yum install git -y
git clone https://github.com/andreynorin/BigDataAnalytics.git
cd BigDataAnalytics/
chmod +x emr-stage-data-files-in-hdfs.sh
./emr-stage-data-files-in-hdfs.sh

spark-submit --master yarn --deploy-mode cluster PySparkPipelineToS3.py

set +x
exit 0