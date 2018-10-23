import pandas as pd
from Levenshtein import distance
from collections import defaultdict
import unicodedata
import sys

in_csv = sys.argv[1]

df = pd.read_csv(in_csv)

def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

def remove_special_characters(line):
    line= unicodeToAscii(line)
    characters = 'abcdefghijklmnopqrstuvwxyz1234567890 '

    removed = []
    aux = ''
    i = 0
    for c in (line):
        if c in characters:
            aux += c
            i += 1
        else:
            removed.append(i)

    return aux, removed


distanceToCorrected = defaultdict(lambda: {})
for row in df.loc[:,["Corrected","Original"]].values:

    distanceToCorrected[row[0]]["original"] = distance(remove_special_characters(row[0].lower())[0],
                                                       remove_special_characters(row[1].lower())[0])

for row in df.loc[:,["Corrected","Transformed"]].values:

    distanceToCorrected[row[0]]["transformed"] = distance(remove_special_characters(row[0].lower())[0],
                                                          remove_special_characters(row[1].lower())[0])

numTransformedIsGreater = 0
numTransformedIsLess = 0

averageOriginal = 0
averageTransformed = 0

for key,val in distanceToCorrected.items():
    if val["original"]<val["transformed"]:
        print(key)
        numTransformedIsGreater+=1

    if val["original"]>val["transformed"]:
        
        numTransformedIsLess+=1
        
    averageOriginal+= val["original"]
    averageTransformed+= val["transformed"]
    
print(numTransformedIsLess,
      numTransformedIsGreater,
      averageOriginal/len(distanceToCorrected),
      averageTransformed/len(distanceToCorrected),)
