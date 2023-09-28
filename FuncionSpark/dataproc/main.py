'''


'''


from pyspark.sql.types import StructType, StringType
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.streaming import DataStreamWriter

PROJECT_NAME = 'spark'

SPARK = SparkSession.builder.getOrCreate()


RAW_DATA_PATH = f"gs://raw-data-{PROJECT_NAME}"
OUTPUT_DATA_PATH = f"gs://output-{PROJECT_NAME}"


SCHEMA = StructType() \
    .add('Name', StringType()) \
    .add('Phone', StringType()) \
    .add('Email', StringType())
    

def extract_data() -> DataFrame:
    return (
        SPARK
        .readStream
        .schema(SCHEMA)
        .option("sep", ",")
        .option("header", "true")
        .csv(f"{RAW_DATA_PATH}/data")
    )
    
    
def load_data(df:DataFrame) -> DataStreamWriter:
    return (
        df
        .writeStream
        .format("delta")
        .option("checkpointLocation",f"{OUTPUT_DATA_PATH}/CLIENTS/DATA/_checkpoint")
        .trigger(once=True) # procesa un microbatch. Desde el ultimo el checkpoint hasta el momento actual
        .outputMode("append")
    )


def execute():
    extract = extract_data()
    load = load_data(extract).start(f"{OUTPUT_DATA_PATH}/CLIENTS/DATA")
    load.awaitTermination()
    
    
    
if __name__ == "__main__":
    execute()
