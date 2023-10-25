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
import json
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

    print(len(sys.argv))
    if len(sys.argv) < 6 or len(sys.argv) > 7:
        print("Usage: pagerank <file> <iterations> <destination> <data_out_file_name> <time_out_file_name> <top10_out_file_name[optionnal]>", file=sys.stderr)
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

    if len(sys.argv) >= 7:
        compute_top = True
        if os.path.exists(sys.argv[6]):
            print(f'The file {sys.argv[6]} already exists.')
            sys.exit(-1)
        else:
            top_file = open(sys.argv[6], 'a')
    else:
        compute_top = False

    print("WARN: This is a naive implementation of PageRank and is given as an example!\n" +
            "Please refer to PageRank implementation provided by graphx",
            file=sys.stderr)

    stats = {}
    results_json = {}
    results_top_json = {}

    stats['start_time'] = time.time_ns()

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
    
    # Calculates and updates URL ranks continuously using PageRank algorithm.
    for iteration in range(int(sys.argv[2])):
        # Calculates URL contributions to the rank of other URLs.
        contribs = links.join(ranks).flatMap(lambda url_urls_rank: computeContribs(
            # type: ignore[arg-type]
            url_urls_rank[1][0], url_urls_rank[1][1]
        ))

        # Re-calculates URL ranks based on neighbor contributions.
        ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * 0.85 + 0.15)

    results = ranks.collect()

    if (compute_top):
        results_top = ranks.takeOrdered(10, key=lambda x: -x[1])
    
    spark.stop()
    stats['end_time'] = time.time_ns()

    # Collects all URL ranks and dump them to console.
    for (link, rank) in results:
        results_json[link] = rank

    if (compute_top):
        for (link, rank) in results_top:
            results_top_json[link] = rank

    #   Write results
    result_file.write(json.dumps(results_json))
    result_file.close()

    if(compute_top):
        top_file.write(json.dumps(results_top_json))
        top_file.close()

    #   Write time measurment result
    stats['time'] = stats['end_time'] - stats['start_time']
    time_file.write(json.dumps(stats))
    time_file.close()

    # Push files into the bucket
    os.system(f'gsutil cp {sys.argv[4]} {sys.argv[3]}/{sys.argv[4]}')
    os.system(f'gsutil cp {sys.argv[5]} {sys.argv[3]}/{sys.argv[5]}')

    if (compute_top):
        os.system(f'gsutil cp {sys.argv[6]} {sys.argv[3]}/{sys.argv[6]}')