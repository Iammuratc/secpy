from secpy.utils.financials import get_income_statement_keys, get_balance_sheet_keys, get_cash_flow_keys
from secpy.financials.utils import get_financial_dicts 

def get_financials(client, ticker):
    """
    Get income statement in quarterly steps. 
    The forms can be 10-K (annual) or 10-Q (quarterly).
    Since annual reports sum up the values for a whole year, the quarterly results are 
    calculated by subtracting the previous three quarterly values from the annual values.
    Parameters
    ----------
    client : SECPyClient
        your client
    ticker : str
        ticker. E.g., AMZN
    Returns
    -------
    financials : dict of dict
        Income_statement, balance_sheet and cash_flow. Quarterly values only.
    """

    financials = {}
    company_facts = client.company_facts()#.__dict__.keys()
    company_facts_for_ticker = company_facts.get_company_facts_for_ticker(ticker)

    company_taxonomies = company_facts_for_ticker.taxonomies.us_gaap.__dict__#us_gaap.Assets.units.USD[0].value

    # Gets the most recent value of Assets (reported in USD) for MSFT 
    # msft.get_concept(taxonomy="us_gaap", fact="Assets").get_unit("USD")[0].value
    # Alternatively, this is statement to the previous
    # msft.taxonomies.us_gaap.Assets.units.USD[0].value
    # my_dict = msft.taxonomies.us_gaap.__dict__#us_gaap.Assets.units.USD[0].value
    # print(my_dict.keys())

    income_statement_keys = get_income_statement_keys()
    # exception_keys will not go through annual-quarter replacement
    income_exception_keys=['WeightedAverageNumberOfSharesOutstandingBasic', 'WeightedAverageNumberOfDilutedSharesOutstanding']
    income_statement, all_end_dates = get_financial_dicts(
        company_taxonomies=company_taxonomies,
        fact_keys=income_statement_keys,
        replace_annual_exception_keys=income_exception_keys
        )
    financials['income_statement'] = income_statement

    balance_sheet_keys = get_balance_sheet_keys()
    balance_sheet, _ = get_financial_dicts(
        company_taxonomies=company_taxonomies,
        fact_keys=balance_sheet_keys,
        )
    financials['balance_sheet'] = balance_sheet
    
    cash_flow_keys = get_cash_flow_keys()
    cash_flow, _ = get_financial_dicts(
        company_taxonomies=company_taxonomies,
        fact_keys=cash_flow_keys
    )
    financials['cash_flow'] = cash_flow

    return financials, all_end_dates
                # income_statement[key][f"{start} - {end}"] = [value,fy,fp,form,filed]
                # if stated_form == form:
                # if stated_form == '10-Q':
                # print(f"----{stated_form}----{key}----")
                # print(fp)
                # print(start)
                # print(end)
                # print(value)
                # income_statement[key][f"{start} - {end}"] = [value,accn,frame,stated_form]
                    # income_statement[key][end] = [value,start] # [value,ind,start,stated_form] # [value,fy,fp,form,filed]
                # elif stated_form == '10-K':
                #     print('-----------')
                #     print(end)
                    # if there are three quarterly values before the current annual value, subtract them
                        # previous_quarterly_sum = 0
                        # for ind_sub in range(ind-3,ind):
                        #     print(ind_sub)
                        #     print(units_dict[units_key][ind_sub].value)
                        #     previous_quarterly_sum += units_dict[units_key][ind_sub].value
                        # print("{:.3e}".format(value))
                        # value = value - previous_quarterly_sum
                        # print("{:.3e}".format(previous_quarterly_sum))
                        # print("{:.3e}".format(value))
                        # print('-----------')
