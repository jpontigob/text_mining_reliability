import pandas as pd
import nltk
from nltk.corpus import stopwords

df = pd.read_csv('/Users/jorgepontigo/text_mining_reliability/raw data/faults_systems.csv', header=0, sep=',',parse_dates = ['failure_date'], usecols=[0,1,2,3], dayfirst = True)

text = df["fault_name"]

cross = ""

for i in range(len(text)):
    cross = cross + (text[i])

tokens = [t for t in cross.split()]

clean_tokens = tokens[:]

sr = stopwords.words('english')

for token in tokens:

    if token in stopwords.words('english'):

        clean_tokens.remove(token)

freq = nltk.FreqDist(clean_tokens)

for key,val in freq.items():

    print (str(key) + ':' + str(val))
    
freq.plot(20,cumulative=False)
