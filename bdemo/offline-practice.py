#offline bandit simulation

import pandas as pd
import numpy as np
from scipy.stats import beta

import pyspark.sql.functions as F
from pyspark.sql.types import *


schema = StructType([StructField('d1', StringType(), True),
                     StructField('weights', DoubleType(), True)])


# Use pandas_udf to define a Pandas UDF
@F.pandas_udf(schema, F.PandasUDFType.GROUPED_MAP)
# Input/output are both a pandas.DataFrame
def weights(df):
    # ggereate a final dataframe from the weights to match output schema
    result_df = pd.DataFrame(
        {'d1': df['d1'], 'weights': final_weights})
    return result_df
