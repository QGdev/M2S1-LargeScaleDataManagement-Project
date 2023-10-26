#!/bin/bash

#
#   PIG benchmark runner
#       Parameters (in order):
#           - Destination bucket, where everything will be stored (gs://ermite-le-bucket/)
#           - Number of worker (2)
#           - Size of the worker disk (50)
#           - Size of the master disk (50)
#           - Project ID
#   
#   Example: sh pig.sh gs://ermite-le-bucket/ 2 50 50 largescaledataproject europe-west1 europe-west1-c
#

# about
# This bash script allows you to automatically create and delete a cluster while achieving a page rank on the Google Cloud Platform in the chosen technology (pig).
# To use it, simply choose the technology where it is requested in the settings section.


## constants

# project
StartedDate=$(date +"%H-%M-%S")

# bucket
BucketPath=$1
BucketPathOut=${BucketPath}out

# settings
WorkersNumber=$2
WorkersDiskSize=$3
MasterDiskSize=$4

ProjectName=$5

# cluster
ClusterName=ermite-le-cluster
Region=$6
Zone=$7

Pig=pig
PyPig=dataproc.py


# results
DirectoryResultName=PIG_${WorkersNumber}_${WorkersDiskSize}_${MasterDiskSize}_${Region}_${Zone}_${StartedDate}

## create the cluster
gcloud dataproc clusters create ${ClusterName} --enable-component-gateway --region ${Region} --zone ${Zone} --master-machine-type n1-standard-4 --master-boot-disk-size ${MasterDiskSize} --num-workers ${WorkersNumber} --worker-machine-type n1-standard-4 --worker-boot-disk-size ${WorkersDiskSize} --image-version 2.0-debian10 --project ${ProjectName}

## copy tech code
gsutil cp ${PyPig} ${BucketPath} # if some repetitions, hide this line because useless

## Clean out directory
gsutil rm -rf ${BucketPathOut}

## run
gcloud dataproc jobs submit ${Pig} --region ${Region} --cluster ${ClusterName} -f ${BucketPath}/${PyPig}

echo "END OF PROCESSING PART"

## delete cluster
gcloud dataproc clusters delete ${ClusterName} --region ${Region} --quiet

# create folder for this execution
mkdir ${DirectoryResultName}

# set the name of the out folder
gsutil mv ${BucketPathOut} ${BucketPath}${DirectoryResultName}

cd ${DirectoryResultName}
# copy the time file to local
gsutil cp ${BucketPath}time.json .
cd ..

