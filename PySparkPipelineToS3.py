# the following code is run in the PySpark prompt

from sparknlp.base import *
from sparknlp.annotator import *
from sparknlp.pretrained import PretrainedPipeline
import sparknlp
from pyspark.ml import Pipeline
import pyspark.sql.functions as f
from pyspark.sql.functions import col
from pyspark.sql import SparkSession

parDF1=spark.read.parquet("hdfs:///GoogleTrainingData/tcilen6wu42p3p6m3q5n22m53u.parquet")
parDF1.count()

parDF2=spark.read.parquet("hdfs:///CC-News-En-Titles-Only/CC-NEWS-20160827145159-00003_ENG.parquet")
parDF2.count()

parDF1 = parDF1.withColumn('index', f.monotonically_increasing_id())

trainDataset    = parDF1
predictDataset  = parDF2.withColumnRenamed('Title','title')

# splitting the dataset int 160k and 40k records for train/test
trainDataset = parDF1.sort('index').limit(160000)
testDataset = parDF1.sort('index', ascending = False).limit(40000)

trainDataset.groupBy("topic").count().orderBy(col("count").desc()).show()
testDataset.groupBy("topic").count().orderBy(col("count").desc()).show()


document_assembler = DocumentAssembler().setInputCol("title") .setOutputCol("document")

tokenizer = Tokenizer().setInputCols(["document"]) .setOutputCol("token")

bert_embeddings = BertEmbeddings().pretrained(name='small_bert_L4_256', lang='en') .setInputCols(["document",'token']).setOutputCol("embeddings")

embeddingsSentence = SentenceEmbeddings().setInputCols(["document", "embeddings"]) .setOutputCol("sentence_embeddings") .setPoolingStrategy("AVERAGE")

classsifierdl = ClassifierDLApproach().setInputCols(["sentence_embeddings"]).setOutputCol("class").setLabelColumn("topic").setMaxEpochs(10).setLr(0.001).setBatchSize(8).setEnableOutputLogs(True)#.setOutputLogsPath('logs')

bert_clf_pipeline = Pipeline(stages=[document_assembler,tokenizer,bert_embeddings,embeddingsSentence,classsifierdl])

# training the model - this may take a fairly long time
# for 5 files start time - 10:14am, end time -  10:22am
bert_clf_pipelineModel = bert_clf_pipeline.fit(trainDataset)

# make sanity check predictions
preds = bert_clf_pipelineModel.transform(testDataset)
preds_df = preds.select('topic','title','class.result')
preds_df.count()
preds_df.show(20)

# make predictions against CC-News-En dataset
preds = bert_clf_pipelineModel.transform(predictDataset)
preds_df = preds.select('topic','Title','class.result')
preds_df.count()
preds_df.show(20)

# export predictions to S3
preds_df.write.format('parquet').option('header','true').save("s3a://litter-box/fromHDFS/predictionsCCNews.parquet", mode='overwrite')