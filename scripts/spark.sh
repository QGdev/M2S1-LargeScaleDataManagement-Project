#!/bin/bash

#
#   SPARK benchmark runner
#       Parameters (in order):
#           - Destination bucket, where everything will be stored (gs://ermite-le-bucket/)
#           - Data source, where the data will be pulled out (gs://public_lddm_data/small_page_links.nt)
#           - Number of worker (2)
#           - Size of the worker disk (50)
#           - Size of the master disk (50)
#           - Number of iterations (3)
#           - Project ID
#   
#   Example: sh run.sh gs://ermite-le-bucket/ gs://public_lddm_data/small_page_links.nt 2 50 50 3 largescaledataproject europe-west1 europe-west1-c
#

# about
# This bash script allows you to automatically create and delete a cluster while achieving a page rank on the Google Cloud Platform in the chosen technology (spark).
# To use it, simply choose the technology where it is requested in the settings section.


## constants

# project
StartedDate=$(date +"%H-%M-%S")

# bucket
BucketPath=$1
BucketData=$2

# settings
WorkersNumber=$3
WorkersDiskSize=$4
MasterDiskSize=$5

ProjectName=$7

# cluster
ClusterName=ermite-le-cluster
Region=$8
Zone=$9

Spark=pyspark
PySpark=pagerank-notype.py
NbIterations=$6

# files names
TimeGlobalFile=duration_results_global.txt
TimeFile=duration_results.txt
DataOutFile=data_out.txt

# results
DirectoryResultName=PYSPARK_${WorkersNumber}_${WorkersDiskSize}_${MasterDiskSize}_${Region}_${Zone}_${StartedDate}
BucketPathOut=${BucketPath}${DirectoryResultName}

## create the cluster
gcloud dataproc clusters create ${ClusterName} --enable-component-gateway --region ${Region} --zone ${Zone} --master-machine-type n1-standard-4 --master-boot-disk-size ${MasterDiskSize} --num-workers ${WorkersNumber} --worker-machine-type n1-standard-4 --worker-boot-disk-size ${WorkersDiskSize} --image-version 2.0-debian10 --project ${ProjectName}

## copy tech code
gsutil cp ${PySpark} ${BucketPath} # if some repetitions, hide this line because useless

## Clean out directory
gsutil rm -rf ${BucketPathOut}

## run
StartRuntime=$(date +%s%N)
gcloud dataproc jobs submit ${Spark} --region ${Region} --cluster ${ClusterName} ${BucketName}pagerank-notype.py  -- ${BucketData} ${NbIterations} ${BucketPathOut} ${DataOutFile} ${TimeFile}
EndRuntime=$(date +%s%N)

echo "END OF PROCESSING PART"

# create folder for this execution
mkdir ${DirectoryResultName}

# copy the result from bucket to local disk
echo ${BucketPathOut}
echo ${DirectoryResultName}
gsutil cp -r ${BucketPathOut}/* ${DirectoryResultName}

cd ${DirectoryResultName}

# Generate operation duration file
[ -f ${TimeGlobalFile} ] && rm ${TimeGlobalFile}
touch ${TimeGlobalFile}
echo "START_TIME" >> "${TimeGlobalFile}"
echo ${StartRuntime} >> "${TimeGlobalFile}"
echo "END_TIME" >> "${TimeGlobalFile}"
echo ${EndRuntime} >> "${TimeGlobalFile}"
echo "TIME" >> "${TimeGlobalFile}"
echo `expr $EndRuntime - $StartRuntime` >> "${TimeGlobalFile}"

cd ..

## delete cluster
gcloud dataproc clusters delete ${ClusterName} --region ${Region} --quiet
