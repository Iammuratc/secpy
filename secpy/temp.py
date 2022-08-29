# import secpy
from secpy_client import SECPyClient
# import inspect
# print(inspect.getfile(SECPyClient.__class__))

client = SECPyClient("<YOUR USER-AGENT>")

# CompanyFactsEndpoint
company_facts = client.company_facts()

msft = company_facts.get_company_facts_for_ticker("MSFT")
# print(msft.taxonomies.us_gaap.__dict__.keys())

# print(msft.get_statement_history().get_statements_for_date_range(start_date="2017/01/01", end_date="2022/01/01",date_format="%Y/%m/%d"))
# for value in msft.taxonomies.__dict__.values():
# 	print(value.__dict__.keys()) 

# assets = msft.get_concept(taxonomy="us_gaap", fact="Assets").get_unit("USD")#[0].value
# for asset in assets:
	# print(asset.fiscal_year)
	# print(asset.value)
	# break

# statements = msft.get_statement_history().get_statements_for_date_range(start_date="2017/01/01", end_date="2022/01/01",date_format="%Y/%m/%d")
# for statement in statements:
# 	print(statement.accn)

# Instantiate and call download_bulk_data() or any other public method to download bulk submissions zip file
# bulk_submissions = client.bulk_company_facts()
# bulk_submissions.download_bulk_data()
# bulk_submissions.get_data_for_ticker_from_archive("MSFT")
