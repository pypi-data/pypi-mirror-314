from .services import (BomHeaderService, BomLinesService,
                       CustomerLedgerEntryService,
                       CustomerService,
                       GeneralLedgerEntriesService,
                       GeneralLedgerService,
                       ILEOriginEntriesService,
                       ItemLedgerEntryService, ItemService,
                       LocationService,
                       SalesInvoiceLinesService,
                       SalesInvoiceService,
                       SalesOrderLinesService,
                       VendorLedgerEntryService, VendorService)
from .session import BusinessCentralSession


class BusinessCentralClient:
    """
    A client class to interact with various Business Central API services.
    """

    def __init__(self, username: str, password: str, base_url: str) -> None:
        """
        Initialize the BusinessCentralClient.
        :param username: API username.
        :param password: API password.
        :param base_url: Base URL of the Business Central API.
        """
        self.session = BusinessCentralSession(username=username, password=password, base_url=base_url)
        self._initiate_services()

    def _initiate_services(self) -> None:
        """ Initiate all services """
        self.customers = CustomerService(self.session)
        self.customer_ledger_entries = CustomerLedgerEntryService(self.session)
        self.vendors = VendorService(self.session)
        self.vendor_ledger_entries = VendorLedgerEntryService(self.session)
        self.items = ItemService(self.session)
        self.item_ledger_entries = ItemLedgerEntryService(self.session)
        self.general_ledgers = GeneralLedgerService(self.session)
        self.general_ledger_entries = GeneralLedgerEntriesService(self.session)
        self.sales_invoices = SalesInvoiceService(self.session)
        self.sales_invoice_lines = SalesInvoiceLinesService(self.session)
        self.ile_origin_entries = ILEOriginEntriesService(self.session)
        self.sales_order_lines = SalesOrderLinesService(self.session)
        self.locations = LocationService(self.session)
        self.bom_headers = BomHeaderService(self.session)
        self.bom_lines = BomLinesService(self.session)

    def __str__(self) -> str:
        """
        String representation of the client.
        :return: The base URL of the Business Central API.
        """
        return f"BusinessCentralClient connected to {self.session.base_url}"
