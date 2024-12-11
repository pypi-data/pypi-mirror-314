import pandas as pd

from .session import BusinessCentralSession


class BaseService:
    """
    Base class for interacting with Business Central API endpoints.
    Each subclass should define the SERVICE_NAME for the respective API endpoint.
    """

    SERVICE_NAME = ""

    def __init__(self, session: BusinessCentralSession) -> None:
        """
        Initialize the service with a session.
        :param session: An instance of BusinessCentralSession.
        """

        if not self.SERVICE_NAME:
            raise ValueError("SERVICE_NAME must be defined in the subclass.")
        self.session = session

    def get_data(self, filters: str = "", columns: dict = None, as_dataframe: bool = False) -> list | pd.DataFrame:
        """
        Fetch data from the API endpoint with optional filters and column selection.
        :param filters: OData filter string for query conditions.
        :param columns: Dict of column names to select.
        :param as_dataframe: Return results as a pandas DataFrame if True, otherwise as a list.
        :return: List or DataFrame of fetched data.
        """

        return self.session.fetch_data(
            service_name=self.SERVICE_NAME,
            filters=filters, columns=columns,
            as_dataframe=as_dataframe
        )

    def get_sample(self, as_dataframe: bool = False) -> list | pd.DataFrame:
        """
        Fetch a sample of data from the API endpoint.
        :param as_dataframe: Return results as a pandas DataFrame if True, otherwise as a list.
        :return: List or DataFrame of sample data.
        """

        return self.get_data(filters="?$top=10", as_dataframe=as_dataframe)


class CustomerService(BaseService):
    SERVICE_NAME = "customers_list"


class CustomerLedgerEntryService(BaseService):
    SERVICE_NAME = "Customer_Ledger_entry_API"


class VendorService(BaseService):
    SERVICE_NAME = "vendors"


class VendorLedgerEntryService(BaseService):
    SERVICE_NAME = "VendorLedgerEntries"


class ItemService(BaseService):
    SERVICE_NAME = "items_list"


class ItemLedgerEntryService(BaseService):
    SERVICE_NAME = "ILE_Consumption"


class GeneralLedgerService(BaseService):
    SERVICE_NAME = "Chart_of_Accounts"


class GeneralLedgerEntriesService(BaseService):
    SERVICE_NAME = "gl_entries"


class SalesInvoiceService(BaseService):
    SERVICE_NAME = "PostedSalesInvoice"


class SalesInvoiceLinesService(BaseService):
    SERVICE_NAME = "posted_sales_invoice_lines"


class ILEOriginEntriesService(BaseService):
    SERVICE_NAME = "ile_origin_detail"


class SalesOrderLinesService(BaseService):
    SERVICE_NAME = "sales_lines"


class LocationService(BaseService):
    SERVICE_NAME = "locations_master"


class BomHeaderService(BaseService):
    SERVICE_NAME = "ProductionBOMHeader"


class BomLinesService(BaseService):
    SERVICE_NAME = "ProductionBOMLines"
