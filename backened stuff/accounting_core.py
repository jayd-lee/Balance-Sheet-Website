import pandas as pd
import matplotlib.pyplot as plt
import requests
header = {'User-Agent': "mr.muffin235@gmail.com"}
companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=header)
T_list = companyTickers.json().values()
#symbol = input('Enter company ticker symbol: ').upper()
symbol = 'META'
for info in T_list:
    if symbol == info['ticker']:
        new = info['cik_str'] #if there is a match assign to a new variable
        cik = f'{new:010d}' #format the new variable with leading zeros

companyConcept = requests.get(
    (f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'), headers=header)

#print(companyConcept.json()['facts']['us-gaap'].keys())
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', 500)

def bs(account):
    df = pd.DataFrame(companyConcept.json()['facts']['us-gaap'][account]['units']['USD'])
    df.drop(columns=['end', 'accn', 'filed', 'fp', 'fy', 'form'], inplace=True)
    df.dropna(inplace=True)
    df = df[df['frame'].str.contains('Q4')]
    df.set_index('frame', inplace=True)
    print(df)
    #df.plot.bar()

bs('Assets')
bs('Liabilities')
bs('StockholdersEquity')

#plt.show()
