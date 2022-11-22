#!/usr/bin/env python3

# take inputDir and outputDir as params

import sys
import os
import glob
import subprocess
import json
import numpy as np
import pandas as pd

# parse passed in args
inputDir  = sys.argv[1]
outputDir = sys.argv[2]

# change pwd
print("script called with inputDir:", inputDir)
print("script called with outputDir:", outputDir)

os.chdir(inputDir)
inputFiles = glob.glob('*.json')

for fileName in inputFiles:
    print("Processing:", fileName)
    os.chdir(inputDir)

    fileNameNoExt   = fileName.split('.')[0]
    parquetFileName = fileNameNoExt +'.parquet'
    
    data = []
    with open(fileName, 'r', encoding="utf8") as f:
        
        data = f.readlines()
        data = [json.loads(item)['Item'] for item in data]

        for i in range(len(data)):
            for key in data[i].keys():
                data[i][key] = data[i][key]["S"]

        df = pd.DataFrame(data)
        df = df[['topic','title']]

        print(df.isnull().sum())
        df = df.dropna()
        os.chdir(outputDir)
        df.to_parquet(parquetFileName)
