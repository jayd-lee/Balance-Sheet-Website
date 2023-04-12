
import pandas as pd
import requests
import numpy as np

from django.shortcuts import render

# Create your views here.




header = {'User-Agent': "mr.muffin235@gmail.com"}
companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=header)
T_list = companyTickers.json().values()
#symbol = input('Enter company ticker symbol: ').upper()

pd.options.display.float_format = '{:.0f}'.format
pd.set_option('display.max_columns', None)

def stock_view(request):

    
    query_dict = request.GET
    query = query_dict.get('q')

    # API calls

    symbol = query.upper()
    for info in T_list:
        if symbol == info['ticker']:
            new = info['cik_str'] #if there is a match assign to a new variable
            cik = f'{new:010d}' #format the new variable with leading zeros

    companyConcept = requests.get(
        (f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'), headers=header)


    def bs(account):
        df_list = companyConcept.json()['facts']['us-gaap'][account]
        df = pd.DataFrame(df_list['units']['USD'])
        df_final = df[(df['fp'] == 'FY') & (df['form'] == '10-K')] #gets only the rows with 'form' == 10-K, and etc
        df_final = df_final.drop_duplicates('end') #drops duplicate 'end'
        df_final = df_final.drop_duplicates('val') #drops duplicate 'val'
        
        df_final = df_final.drop(columns=['accn', 'filed', 'fp', 'fy', 'frame', 'form',]) #drop columns that arent needed
        df_final = df_final.set_index('end') #sets index to fy
        df_final.columns = [account]

        return df_final
        
    try:
        assets = bs('Assets')
    except:
        assets = pd.DataFrame(np.nan, index=['2020-12-31'], columns=['assets'])

    try:
        liabilities = bs('Liabilities')
    except:
        liabilities = pd.DataFrame(np.nan, index=['2020-12-31'], columns=['liabilites'])

        
    try:
        stock_holder_equity = bs('StockholdersEquity')
    except:
        try:
            stock_holder_equity = bs('StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest')
        except:
            stock_holder_equity = pd.DataFrame(np.nan, index=['2020-12-31'], columns=['stockholdersequity'])
    



    result = pd.merge(pd.merge(assets, liabilities, left_index=True, right_index=True, how='outer'),
                    stock_holder_equity, left_index=True, right_index=True, how='outer')

    result = result.sort_index(ascending=False).T#sorts the index from latest year to oldest year


    context = {
        'Assets': assets,
        'Liabilities': liabilities,
        'StockholdersEquity': stock_holder_equity,
        'result': result.to_html()
        }


    return render(request, 'stock_info/stock_info.html', context=context)


