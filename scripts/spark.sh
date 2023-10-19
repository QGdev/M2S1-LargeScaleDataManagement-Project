#!/bin/bash

#
#   SPARK benchmark runner
#       Parameters (in order):
#           - Destination bucket, where everything will be stored (gs://ermite-le-bucket/)
#           - Data source, where the data will be pulled out (gs://public_lddm_data/small_page_links.nt)
#           - Number of worker (2)
#           - Size of the worker disk (50)
#           - Size of the master disk (50)
#           - Project ID
#   
#   Example: sh run.sh gs://ermite-le-bucket/ gs://public_lddm_data/small_page_links.nt 2 50 50 largescaledataproject europe-west1 europe-west1-c
#

# about
# This bash script allows you to automatically create and delete a cluster while achieving a page rank on the Google Cloud Platform in the chosen technology (spark).
# To use it, simply choose the technology where it is requested in the settings section.


## constants

# project
StartedDate=$(date +"%H-%M-%S")

# bucket
BucketPath=$1
BucketPathOut=${BucketPath}out
BucketData=$2

# settings
WorkersNumber=$3
WorkersDiskSize=$4
MasterDiskSize=$5

ProjectName=$6

# cluster
ClusterName=ermite-le-cluster
Region=$7
Zone=$8

Spark=pyspark
PySpark=pagerank-notype.py


# results
DirectoryResultName=SPARK_${WorkersNumber}_${WorkersDiskSize}_${MasterDiskSize}_${Region}_${Zone}_${StartedDate}

## create the cluster
gcloud dataproc clusters create ${ClusterName} --enable-component-gateway --region ${Region} --zone ${Zone} --master-machine-type n1-standard-4 --master-boot-disk-size ${MasterDiskSize} --num-workers ${WorkersNumber} --worker-machine-type n1-standard-4 --worker-boot-disk-size ${WorkersDiskSize} --image-version 2.0-debian10 --project ${ProjectName}

## copy tech code
gsutil cp ${PySpark} ${BucketPath} # if some repetitions, hide this line because useless

## Clean out directory
gsutil rm -rf ${BucketPathOut}

## run
StartRuntime=$(date +%s%N)
gcloud dataproc jobs submit ${Spark} --region ${Region} --cluster ${ClusterName} ${BucketName}pagerank-notype.py  -- ${BucketData} 3
EndRuntime=$(date +%s%N)

echo "END OF PROCESSING PART"

# create folder for this execution
mkdir ${DirectoryResultName}

# copy the result from bucket to local disk
gsutil cp -r ${BucketPathOut} ${DirectoryResultName}

cd ${DirectoryResultName}

# Generate operation duration file
[ -f duration_results.txt ] && rm duration_results.txt
touch duration_results.txt
echo "START_TIME" >> duration_results.txt
echo ${StartRuntime} >> duration_results.txt
echo "END_TIME" >> duration_results.txt
echo ${EndRuntime} >> duration_results.txt
echo "TIME" >> duration_results.txt
echo `expr $EndRuntime - $StartRuntime` >> duration_results.txt

cd ..

## delete cluster
gcloud dataproc clusters delete ${ClusterName} --region ${Region} --quiet
