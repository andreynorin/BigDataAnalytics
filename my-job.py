# my-job.py
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("my-job-py").getOrCreate()
sc = spark.sparkContext
rdd = sc.parallelize([1, 2, 3, 4])
res = rdd.map(lambda x: x**2).collect()
print(res)