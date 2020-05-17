import pandas as pd
import nltk
from nltk.corpus import stopwords

df = pd.read_csv('/Users/jorgepontigo/text_mining_reliability/raw data/faults_systems.csv', header=0, sep=',',parse_dates = ['failure_date'], usecols=[0,1,2,3], dayfirst = True)

text = df["fault_name"]

cross = ""

for i in range(len(text)):
    cross = cross + (text[i])

tokenization = [t for t in cross.split()]

clean_tokenization = tokenization[:]

english_sw_up = [element.upper() for element in stopwords.words('english')]
spanish_sw_up = [element.upper() for element in stopwords.words('spanish')]
english_sw_low = [element.lower() for element in stopwords.words('english')]
spanish_sw_low = [element.lower() for element in stopwords.words('spanish')]

for token in tokenization:

    if token in english_sw_up:
        clean_tokenization.remove(token)

    elif token in spanish_sw_up:
        clean_tokenization.remove(token)

    elif token in english_sw_low:
        clean_tokenization.remove(token)

    elif token in spanish_sw_low:
        clean_tokenization.remove(token)

frequency = nltk.FreqDist(clean_tokenization)

frequency.plot(20,cumulative=False)

