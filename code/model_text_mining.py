import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
from fuzzywuzzy import fuzz

df = pd.read_csv('/Users/jorgepontigo/text_mining_reliability/raw data/faults_systems.csv', header=0, sep=',',parse_dates = ['failure_date'], usecols=[0,1,2,3,4], dayfirst = True)

df2 = pd.read_csv('/Users/jorgepontigo/text_mining_reliability/raw data/mode_faults.csv', header=0, sep=',', usecols=[0,1], dayfirst = True)

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

df["fault_name"]= df['fault_name'].apply( lambda x: ' '.join([word for word in x.split() if word not in english_sw_up]))

df["fault_name"]= df['fault_name'].apply( lambda x: ' '.join([word for word in x.split() if word not in spanish_sw_up]))

df["fault_name"]= df['fault_name'].apply( lambda x: ' '.join([word for word in x.split() if word not in english_sw_low]))

df["fault_name"]= df['fault_name'].apply( lambda x: ' '.join([word for word in x.split() if word not in spanish_sw_low]))

df['fault_name'] = df['fault_name'].str.upper()

df["fault_name"] = df.fault_name.str.replace(r"\bFOUND\b", ' ', regex=True)\
                    .str.replace(r"\bFAULT\b", "")\
                    .str.replace(r"\bPROBLEM\b", "")\
                    .str.replace(r"\bproblem\b", "")\
                    .str.replace(r"\bDefect\b", "")\
                    .str.replace(r"\bPERFORM\b", "")\
                    .str.replace(r"\bMAINTENANCE\b", "")\
                    .str.replace(r"\bDISPLAYED\b", "")\
                    .str.replace(r"\bDAILY\b", "")\
                    .str.replace(r"\bFAULT\b", "")\
                    .str.replace(r"\bCHECK\b", "")\
                    .str.replace(r"\bPROBLEM\b", "")\
                    .str.replace(r"\bPOSITION\b", "")\
                    .str.replace(r"\bREPORTA\b", "")\
                    .str.replace(r"\bMSG\b", "")\
                    .str.replace(r"\bDEFECT\b", "")\
                    .str.replace(r"\bTEMPERATURA\b", "")\
                    .str.replace(r"\bINSPECTION\b", "")\
                    .str.replace(r"\bDUE\b", "")

df = df.reset_index(drop=True)
df2 = df2.reset_index(drop=True)
df3 = df.merge(df2, on=['system'], how='left', indicator=False)
df3['match'] = 0
df4 = df3

for i in range(len(df3)):
    df4['match'][i] = fuzz.ratio(df3['fault_name'][i], df3['mode_fault'][i])

df4['RN'] = df4.sort_values(['match'], ascending=[False]) \
             .groupby(['id_failure', 'fault_name']) \
             .cumcount() + 1

df5 = df4[(df4.RN == 1)]
df5.to_csv('export.csv', encoding='utf-8')

df5 = df5.drop(['RN', 'id_failure', 'failure_date', 'system', 'Machine'], axis=1)
print(df5)

