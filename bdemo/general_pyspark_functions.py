from datetime import datetime
import os
import matplotlib.pytplot as plt


### Date functions #############
def str_to_date(str_date):
    return datetime.strptime(str_date, "%Y%m%d").date()

def date_to_str(date_obj):
    return date_obj.strftime("%Y%m%d")


def daterange(date1, date2):
    x = []
    for n in range(int((date2 - date1).days) + 1):
        x.append(date_to_int(date1 + timedelta(n)))
    return x

##### Getting list of file names in a S3 directory ############
def list_files(path, profile = None):
    if not path.endswith("/"):
        raise Exception("not handled...")
    command = 'aws s3 ls %s' % path
    if profile is not None:
        command = 'aws --profile %s s3 ls %s' % (profile, path)
    result = os.popen(command)
    _r = result.read().strip().split('\n')
    _r = [path + i.strip().split(' ')[-1] for i in _r]
    files = [os.path.basename(f[:-1]) for f in _r]
    return files


##### make histogram plot using pandas dataframe in pyspark ##########
plt.figure()
plt.clf()

plt.subplot(111)
(pdf.col.hist(
    bins=np.linspace(0,150,50),
    label='label',
    normed=False,
    alpha=0.5))
plt.legend()
plt.title('Title', loc='left')
plt.subplots_adjust(hspace=0.5)


############### Generate pairs from sequence data ####################
from itertools import combinations
import pyspark.sql.functions as F

def co_pairs(x):
    pairs = list(set(list(combinations(x[0], 2))))
    pairs = [i for i in pairs if i[0]!=i[1]]
    return pairs

seq_df = df.groupby('u').agg(F.collect_list('i').alias('ii'))\
            .where(F.col(ii) > n).select('u', F.concat_ws(' ', col('ii')).alias('jj'))

seq_df = seq_df.withColumn('sp', F.split('jj', '\s+'))
seq_rdd = seq_df.select('sp').rdd.map(tuple)
pairs_rdd = seq_rdd.map(co_pairs).flatMap(lambda x: x)
pairs_df = pairs.map(lambda x: (x[0], x[1])).toDF('t1', 't2')
g_pairs = pairs_df.groupBy('t1', 't2').agg(F.count('t1'))\
                .filter(F.col('t1') != F.col('t2'))

##### logger format #################
log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=log_fmt)
logger = logging.getLogger(__name__)


#####
