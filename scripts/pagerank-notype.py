#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
#   This python script has been updated in order to fit our needs
#

"""
This is an example implementation of PageRank. For more conventional use,
Please refer to PageRank implementation provided by graphx

Example Usage:
bin/spark-submit examples/src/main/python/pagerank.py data/mllib/pagerank_data.txt 10
"""
import os
import re
import sys
import time
from operator import add
from typing import Iterable, Tuple

from pyspark.resultiterable import ResultIterable
from pyspark.sql import SparkSession


# removed typing for compatibility with Spark 3.1.3
# typing ok with spark 3.3.0

def computeContribs(urls, rank):
    """Calculates URL contributions to the rank of other URLs."""
    num_urls = len(urls)
    for url in urls:
        yield (url, rank / num_urls)


def parseNeighbors(urls):
    """Parses a urls pair string into urls pair."""
    parts = re.split(r'\s+', urls)
    return parts[0], parts[2]


if __name__ == "__main__":

    if len(sys.argv) != 6:
        print("Usage: pagerank <file> <iterations> <destination> <data_out_file_name> <time_out_file_name>", file=sys.stderr)
        sys.exit(-1)

    #   Checks if provided file already exists
    #       For results
    if os.path.exists(sys.argv[4]):
        print(f'The file {sys.argv[4]} already exists.')
        sys.exit(-1)
    else:
        result_file = open(sys.argv[4], 'a')

    #       For time measurment
    if os.path.exists(sys.argv[5]):
        print(f'The file {sys.argv[5]} already exists.')
        sys.exit(-1)
    else:
        time_file = open(sys.argv[5], 'a')

    print("WARN: This is a naive implementation of PageRank and is given as an example!\n" +
            "Please refer to PageRank implementation provided by graphx",
            file=sys.stderr)

    # Initialize the spark context.
    spark = SparkSession\
        .builder\
        .appName("PythonPageRank")\
        .getOrCreate()

    # Loads in input file. It should be in format of:
    #     URL         neighbor URL
    #     URL         neighbor URL
    #     URL         neighbor URL
    #     ...
    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])

    # Loads all URLs from input file and initialize their neighbors.
    links = lines.map(lambda urls: parseNeighbors(urls)
                      ).distinct().groupByKey().cache()

    # Loads all URLs with other URL(s) link to from input file and initialize ranks of them to one.
    ranks = links.map(lambda url_neighbors: (url_neighbors[0], 1.0))

    print("###   TIME MEASUREMENT START   ###")
    start_time = time.time_ns()

    times = [0 for _ in range(int(sys.argv[2]))]

    # Calculates and updates URL ranks continuously using PageRank algorithm.
    for iteration in range(int(sys.argv[2])):
        # Calculates URL contributions to the rank of other URLs.
        contribs = links.join(ranks).flatMap(lambda url_urls_rank: computeContribs(
            # type: ignore[arg-type]
            url_urls_rank[1][0], url_urls_rank[1][1]
        ))

        # Re-calculates URL ranks based on neighbor contributions.
        ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * 0.85 + 0.15)

        times[iteration] = time.time_ns()

    end_time = time.time_ns()
    print("###   TIME MEASUREMENT END   ###")

    #   Write time measurment result
    time_file.write("START_TIME\n")
    time_file.write(f'{start_time}\n')
    time_file.write("END_TIME\n")
    time_file.write(f'{end_time}\n')
    time_file.write("TIME\n")
    time_file.write(f'{end_time - start_time}\n')
    for i in range(int(sys.argv[2])):
        time_file.write(f'TIME_ITERATION_{i}\n')
        time_file.write(f'{times[i]}\n')
    time_file.close()

    # Collects all URL ranks and dump them to console.
    for (link, rank) in ranks.collect():
        line = f'{link} has rank: {rank}.'
        print(line)
        result_file.write(f'{line}\n')

    result_file.close()
    spark.stop()

    # Push files into the bucket
    os.system(f'gsutil cp {sys.argv[4]} {sys.argv[3]}/{sys.argv[4]}')
    os.system(f'gsutil cp {sys.argv[5]} {sys.argv[3]}/{sys.argv[5]}')
