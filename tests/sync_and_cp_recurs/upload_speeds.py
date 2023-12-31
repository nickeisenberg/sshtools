from tqdm import tqdm
from sshtools.transfer.aws import fast_upload, fast_download, sync, cp_recursive
import os
import time
import os
import boto3
import json


#--------------------------------------------------
# get the access and secret keys to the aws account
#--------------------------------------------------
with open("/home/nicholas/.credentials/password.json") as oj:
    pw = json.load(oj)
ACCESS_KEY = pw['aws_ACCESS_KEY_nick']
SECRET_ACCESS_KEY = pw['aws_SECRET_ACCESS_KEY_nick']
session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    profile_name="nick",
    region_name="us-west-1"
)
#--------------------------------------------------

#--------------------------------------------------
# delete and remake the folder for testing
#--------------------------------------------------
s3_res = session.resource('s3')
bucket = s3_res.Bucket('sshtools-demo-bucket')
_ = bucket.objects.filter(Prefix="imgs/").delete()
bucket.put_object(Key="imgs/")
#--------------------------------------------------


#-------------------------------------------------- 
# copy_dir testing.
#-------------------------------------------------- 
source_dir = "/home/nicholas/Datasets/celebA/img64_100"
num_b = sum([os.stat(os.path.join(source_dir, f)).st_size for f in os.listdir(source_dir)])
save_dir = "s3://sshtools-demo-bucket/imgs"
profile = "nick"

log_file = "/home/nicholas/Tmp/update.log"
sync(
    source_dir, save_dir, profile, generate_logfile_to=log_file
)

cp_recursive(
    source_dir, save_dir, profile
)


#-------------------------------------------------- 
# fast_upload and fast_download testing
#-------------------------------------------------- 
# source_dir = "/home/nicholas/Datasets/CelebA/img_align_celeba_10000"
source_dir = "/home/nicholas/Datasets/CelebA/batched"
bucketname = 'speed-demo-bucket'
s3dir = 'imgs'
filelist = [os.path.join(source_dir, f) for f in os.listdir(source_dir)]
totalsize = sum([os.stat(f).st_size for f in filelist])
print(totalsize / 1e6)

with tqdm(
    desc='upload', ncols=60, total=totalsize, unit='B', unit_scale=1
) as pbar:
    fast_upload(
        session, 
        bucketname, 
        s3dir, 
        filelist, 
        pbar, 
        workers=10
    )


s3_res = session.resource('s3')
bucketname = 'speed-demo-bucket'
bucket = s3_res.Bucket(bucketname)
bucket_objects = [
    x.key 
    for x in bucket.objects.filter(Prefix="imgs/") 
    if x.key.endswith('zip')
]
object_sizes = [
    x.size 
    for x in bucket.objects.filter(Prefix="imgs/") 
    if x.key.endswith('zip')
]
totalsize = sum(object_sizes)
localdir = "/home/nicholas/Datasets/CelebA/ret"
len(bucket_objects)


with tqdm(
    desc='download', ncols=60, total=totalsize, unit='B', unit_scale=1
) as pbar:
    fast_download(
        session, 
        bucketname, 
        bucket_objects, 
        localdir, 
        pbar, 
        workers=20
    )
