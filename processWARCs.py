#!/usr/bin/env python3

# take inputDir and outputDir as params

import sys
import os
import glob
import subprocess
import json
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from numpy import int64
from warcio.archiveiterator import ArchiveIterator

# parse passed in args
inputDir  = sys.argv[1]
outputDir = sys.argv[2]

# change pwd
print("script called with inputDir:", inputDir)
print("script called with outputDir:", outputDir)


# change pwd to inputDir and enumerate files into a list
os.chdir(inputDir)
path = os.getcwd()
print("changed path to:",path)

# add all WARC files to inputFiles list
inputFiles = glob.glob('*warc*')


def build_titles_df():
    
    print("Generating dataframe")
    df = pd.DataFrame(columns=(['Title']))
    
    with open(fileName, 'rb') as stream:
            recordCounter = 0
            for record in ArchiveIterator(stream):
                    if record.rec_type == 'response':
                        payload_content = record.raw_stream.read()
                        soup             = BeautifulSoup(payload_content, 'html.parser')
                        if (soup.title is not None):
                            title = soup.title.string
                            df.loc[recordCounter] = [title]

                    recordCounter += 1

    df.head()
    df.to_parquet(parquetFilePath)



# process files in the list
for fileName in inputFiles:

    os.chdir(inputDir)
    fileNameNoExt       = fileName.split('.')[0]
    parquetFileName     = fileNameNoExt +'.parquet'
    parquetFilePath     = os.path.join(path, outputDir, parquetFileName)

    print("Processing file:",fileName)
    print("Output file name will be:", parquetFilePath)
    build_titles_df()

print("Processing complete.")