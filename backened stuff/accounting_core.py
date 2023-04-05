import pandas as pd
import matplotlib.pyplot as plt
import requests
header = {'User-Agent': "mr.muffin235@gmail.com"}
companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=header)
T_list = companyTickers.json().values()
symbol = 'AMZN'
for info in T_list:
    if symbol == info['ticker']:
        new = info['cik_str'] #if there is a match assign to a new variable
        cik = f'{new:010d}' #format the new variable with leading zeros

companyConcept = requests.get(
    (f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'), headers=header)

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', 500)
pd.options.display.float_format = '{:.2e}'.format
years = [str(yr) for yr in range(2008, 2023)]

keysDf = pd.DataFrame(companyConcept.json()['facts']['us-gaap'])
core_list = ['Assets', 'Liabilities', 'StockholdersEquity']
def core(account):
    #for account in accounts_list:
    first = keysDf.get(account)
    if first is None:
        nullDf = pd.DataFrame({'year': years, account: ['empty' for r in range(len(years))]})
        nullDf = nullDf.fillna(0)
        nullDf = nullDf.set_index('year')
        #print(nullDf)
        return (nullDf)
    else:
        df = pd.DataFrame(companyConcept.json()['facts']['us-gaap'][account]['units']['USD'])
        df.drop(columns=['end', 'accn', 'filed', 'fp', 'fy', 'form'], inplace=True)
        df.dropna(inplace=True)
        df = df[df['frame'].str.contains('Q4')]
        df = df.rename(columns={'val': account, 'frame': 'year'})
        df['year'] = df['year'].str[2:6]
        df[account] = df[account].astype(float)
        df = df.set_index('year')
        #print(df)
        return df
        #df.plot.bar()

x = core('Assets')
y = core('Liabilities')
z = core('StockholdersEquity')

#df2 = pd.merge(x, z, on='year', how='inner')
#plt.show()