




```python

from typing import List
import asyncio

from config import NocoDBConfig
from tgshops_integrations.middlewares.gateway import Gateway
from services.bitrix.client import BitrixClient

# Your credentials are here and source of the target table
NOCODB_HOST = NocoDBConfig.HOST
NOCODB_API_KEY = NocoDBConfig.API_KEY
SOURCE=NocoDBConfig.source_table

async def main():

    # Here is your client to upload data from your service
    bitrixService=BitrixClient()

    # Products have to be in a according to the ProductModel
        # class ProductModel(BaseModel):
            # id: Optional[str]
            # external_id: Optional[str]
            # category: Optional[List[str]]
            # category_name: Optional[List[str]]
            # name: str
            # description: Optional[str]
            # price: Optional[float]
            # final_price: Optional[float]
            # currency: Optional[str]
            # stock_qty: int
            # orders_qty: int = Field(0, hidden_field=True)
            # created: datetime = Field(default=datetime.now, hidden_field=True)
            # updated: datetime = Field(default=datetime.now, hidden_field=True)
            # preview_url: List[str] = []
            # extra_attributes: List[ExtraAttribute] = []

    bitrix_product_list=await bitrixService.get_crm_product_list()

    NocoGateway = Gateway(NOCODB_HOST=NOCODB_HOST,NOCODB_API_KEY=NOCODB_API_KEY)
    
    # Example how to clean your table
    # await NocoGateway.load_data(SOURCE=SOURCE)
    # await NocoGateway.delete_all_products()


    # In order to obtain data from the table need to call load data, to obtain it for further comparation
    await NocoGateway.load_data(SOURCE=SOURCE)
    # Initializes any missing categories
    await NocoGateway.category_manager.update_categories(external_products=bitrix_product_list)

    # Creates or updates the products
    await NocoGateway.update_products(external_products=bitrix_product_list)


asyncio.run(main())





```