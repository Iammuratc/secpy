from sec_api import XbrlApi

API_KEY = '13ca837999e3dab4b9cc2b0f5f5b3ebd19062ccd266490233e198f366ae72925'

xbrlApi = XbrlApi(API_KEY)
url_10k_aapl = 'https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/aapl-20220924.htm'

aapl_xbrl_json = xbrlApi.xbrl_to_json(htm_url=url_10k_aapl)

print('--------------------------------------------------------------------')
print("Keys of income statement dictionary in XBRL from Apple's 10-K filing")
print('--------------------------------------------------------------------')
print(*list(aapl_xbrl_json['StatementsOfIncome'].keys()), sep='\n')

print('--------------------------------------------------------------------')
print("Keys of balance sheet dictionary in XBRL from Apple's 10-K filing")
print('--------------------------------------------------------------------')
print(*list(aapl_xbrl_json['BalanceSheets'].keys()), sep='\n')


print('--------------------------------------------------------------------')
print("Keys of cash flow dictionary in XBRL from Apple's 10-K filing")
print('--------------------------------------------------------------------')
print(*list(aapl_xbrl_json['StatementsOfCashFlows'].keys()), sep='\n')