import numpy as np

def get_financial_dicts(company_taxonomies,fact_keys,replace_annual_exception_keys=None):
    """
    Set financial dicts (e.g., balance_sheet)
    Parameters
    ----------
    company_taxonomies : SECPyClient.company_facts
        Company facts.
    fact_keys : list
        List of financial keys, e.g., Assets, LiabilitiesCurrent
    # replace_annual : bool
    #     Calculate the 10-Q equivalent of 10-K reports
    replace_annual_exception_keys : bool
        These key indices will not be affected by replace_annual. E.g., EPS has the same value in 10-Q and 10-K reports, but income not.
    Returns
    -------
    financial_dicts : dict of dict
        For example, income_statement, balance_sheet and cash_flow
    all_end_dates : list
        All the end dates in financial
    """
    financial_dicts = {}

    if replace_annual_exception_keys is None:
        replace_annual_exception_keys = list(company_taxonomies.keys()).copy()
    all_end_dates=[]
    for key in company_taxonomies.keys():
        if key in fact_keys:
            financial_dicts[key] = {}
            units_dict = company_taxonomies[key].units.__dict__
            units_key = list(units_dict.keys())[0] # units_key in [USD, shares, USD_shares]
            # print(f"-------{key}-----------")
            for ind in range(len(units_dict[units_key])):
                start = units_dict[units_key][ind].start
                end = units_dict[units_key][ind].end
                value = units_dict[units_key][ind].value
                stated_form = units_dict[units_key][ind].form

                all_end_dates.append(end)

                financial_dicts[key][end] = [value,start,stated_form,ind] # [value,ind,start,stated_form] # [value,fy,fp,form,filed]
            # 10-K report values are for a whole year
            # Calculate their quarterly values by subtracting previous three quarterly values
            if key not in replace_annual_exception_keys:
                financial_dicts[key] = replace_annual_values(financial_dicts[key])
    return financial_dicts, sorted(set(all_end_dates))


def replace_annual_values(financial_dict):
    """
    Find previous quarters of the annual reports
    Parameters
    ----------
    financial_dict : dict
        Equivalent to financial_dicts[key] at secpy/financials/utils/get_financial_dicts
    Returns
    -------
    financial_dict : dict
        Removed 10-K values with their corresponding 10-Q values
    """
    
    financial_dict_quarterly = {key: values for key,values in financial_dict.items() if values[-2] != '10-K'}
    financial_dict_annual = {key: values for key,values in financial_dict.items() if values[-2] == '10-K'}
    financial_dict_annual_replaced = {}
    for key_a, values_a in financial_dict_annual.items():
        end_a = key_a
        value_a,start_a,stated_form_a,ind_a = values_a
        value_subtracted = value_a
        # If start_a does not exist, retrieve it from end_a
        # start_a = retrieve_start_from_end(start_a,end_a)
        start_in_days_a = get_date_in_days(start_a)
        end_in_days_a = get_date_in_days(end_a)
        for key_q, values_q in financial_dict_quarterly.items():
            end_q = key_q
            value_q,start_q,stated_form_q,ind_q = values_q
            # start_q = retrieve_start_from_end(start_q,end_q)
            start_in_days_q = get_date_in_days(start_q)
            end_in_days_q = get_date_in_days(end_q)
            if (start_in_days_q >= start_in_days_a) and (end_in_days_q <= end_in_days_a):
                value_subtracted -= value_q
        financial_dict_annual_replaced[key_a] = [value_subtracted,start_a,f"{stated_form_a}_processed",ind_a]
    financial_dict_annual_replaced.update(financial_dict_quarterly)
    return financial_dict_annual_replaced  
    

def filter_earlier_values_from_financial(financial_dicts,start_year):
    """
    Remove later values from nested dicts.
    Parameters
    ----------
    financial_dicts : dict
        Nested dicts.
    Returns
    -------
    financial_filtered : dict
        Filtered out nested dict
    """

    financial_filtered = {key:{} for key in financial_dicts.keys()}
    start = f"{start_year}-01-01"
    start_in_days = get_date_in_days(start)

    for key, financial_dict in financial_dicts.items():
        for end, values in financial_dict.items():
            if get_date_in_days(end) >= start_in_days:
                financial_filtered[key][end] = values
    return financial_filtered

def filter_earlier_values_from_list(date_list,start_year):
    """
    Remove later values from nested dicts.
    Parameters
    ----------
    date_list : list
        financial list.
    Returns
    -------
    date_list_filtered : list
        Filtered out list
    """
    start = f"{start_year}-01-01"
    start_in_days = get_date_in_days(start)
    date_list_filtered = []
    for date in date_list:
        if get_date_in_days(date) >= start_in_days:
            date_list_filtered.append(date)

    return date_list_filtered

def get_date_in_days(date):
    year, month, days = np.array(date.split('-')).astype(int)
    date_in_days = year*365+month*30+days
    return date_in_days


def get_days_in_date(total_days):
    years = total_day // 365
    months = (total_day - years*365)//30
    days = total_day - year*365-month*30
    days_in_date = f"{years}-{months}-{days}"
    return days_in_date

def retrieve_start_from_end(start_date, end_date, ):
    if start_date == None:
        year, month, days = np.array(end_date.split('-')).astype(int)
        start_date = f"{year-1}-{month}-{days}"
    return start_date


# fy = units_dict[units_key][ind].fiscal_year
# fp = units_dict[units_key][ind].fiscal_period
# accn = units_dict[units_key][ind].accn
# frame = units_dict[units_key][ind].frame
# filed = units_dict[units_key][ind].filed
