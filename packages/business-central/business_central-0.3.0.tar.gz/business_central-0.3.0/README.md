Example Usage:

```python
from business_central.client import BusinessCentralClient

username = "<username>"
password = "<password>"
base_url = "<base_url>"

client = BusinessCentralClient(username=username, password=password, base_url=base_url)

# CUSTOMER SERVICES
customers = client.customers.get_data(as_dataframe=True)
customer_ledger_entries = client.customer_ledger_entries.get_data(as_dataframe=True)

# VENDOR SERVICES
vendors = client.vendors.get_data(as_dataframe=True)
vendor_ledger_entries = client.vendor_ledger_entries.get_data(as_dataframe=True)

# ITEM SERVICES
items = client.items.get_data(as_dataframe=True)
item_ledger_entries = client.item_ledger_entries.get_data(as_dataframe=True)
ile_origin_entries = client.ile_origin_entries.get_data(as_dataframe=True)

# GENERAL LEDGER SERVICES
general_ledgers = client.general_ledgers.get_data(as_dataframe=True)
general_ledger_entries = client.general_ledger_entries.get_data(as_dataframe=True)

# SALES INVOICE SERVICES
sales_invoices = client.sales_invoices.get_data(as_dataframe=True)
sales_invoice_lines = client.sales_invoice_lines.get_data(as_dataframe=True)

# SALES ORDER SERVICES
sales_order_lines = client.sales_order_lines.get_data(as_dataframe=True)
locations = client.locations.get_data(as_dataframe=True)

# PRODUCTION BOM SERVICES
bom_headers = client.bom_headers.get_data(as_dataframe=True)
bom_lines = client.bom_lines.get_data(as_dataframe=True)
```