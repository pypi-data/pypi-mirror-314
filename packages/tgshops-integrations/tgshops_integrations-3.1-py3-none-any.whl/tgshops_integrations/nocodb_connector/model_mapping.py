import json
import secrets
import importlib.util
from pathlib import Path

from tgshops_integrations.models.categories import CategoryModel, CategoryResponseModel, PaginationResponseModel
from tgshops_integrations.models.products import ExtraAttribute, ProductModel


# Helper function to load `config.py` dynamically
def load_config(config_path: str):
    """
    Dynamically load a config file from the provided path.
    """
    config_path = Path(config_path)
    if config_path.exists():
        spec = importlib.util.spec_from_file_location("config", config_path)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        return config
    else:
        raise FileNotFoundError(f"Configuration file not found at {config_path}")


# Initialize model mapping constants dynamically from config
def initialize_model_mapping(config_path: str):
    """
    Load and initialize global constants for model mapping from a config file.
    """
    global CATEGORY_IMAGE_FIELD, ID_FIELD, CATEGORY_NAME_FIELD, CATEGORY_PARENT_ID_FIELD, CATEGORY_PARENT_FIELD
    global CATEGORY_ID_OF_CATEGORY_FIELD, PRODUCT_NAME_FIELD, PRODUCT_DESCRIPTION_FIELD, PRODUCT_PRICE_FIELD
    global PRODUCT_CURRENCY_FIELD, PRODUCT_STOCK_FIELD, PRODUCT_CATEGORY_NAME_FIELD, PRODUCT_CATEGORY_ID_FIELD
    global PRODUCT_IMAGE_FIELD, PRODUCT_DISCOUNT_PRICE_FIELD, PRODUCT_CATEGORY_ID_LOOKUP_FIELD, PRODUCT_IMAGES_LOOKUP_FIELD
    global PRODUCT_REQUIRED_OPTIONS_FIELD, PRODUCT_CATEGORIES_EXTRA_OPTIONS_FIELD, PRODUCT_CATEGORIES_EXTRA_OPTION_NAMES_FIELD
    global PRODUCT_EXTRA_CHOICE_REQUIRED_FIELD, PRODUCT_ID_FIELD, PRODUCT_EXTERNAL_ID, PRODUCT_CHECKOUT_MODE
    global NEW_ID_FIELD, NOCODB_CHECKOUT_MODES

    config = load_config(config_path)

    CATEGORY_IMAGE_FIELD = config.CATEGORY_IMAGE_FIELD
    ID_FIELD = config.ID_FIELD
    CATEGORY_NAME_FIELD = config.CATEGORY_NAME_FIELD
    CATEGORY_PARENT_ID_FIELD = config.CATEGORY_PARENT_ID_FIELD
    CATEGORY_PARENT_FIELD = config.CATEGORY_PARENT_FIELD
    CATEGORY_ID_OF_CATEGORY_FIELD = config.CATEGORY_ID_OF_CATEGORY_FIELD

    PRODUCT_NAME_FIELD = config.PRODUCT_NAME_FIELD
    PRODUCT_DESCRIPTION_FIELD = config.PRODUCT_DESCRIPTION_FIELD
    PRODUCT_PRICE_FIELD = config.PRODUCT_PRICE_FIELD
    PRODUCT_CURRENCY_FIELD = config.PRODUCT_CURRENCY_FIELD
    PRODUCT_STOCK_FIELD = config.PRODUCT_STOCK_FIELD
    PRODUCT_CATEGORY_NAME_FIELD = config.PRODUCT_CATEGORY_NAME_FIELD
    PRODUCT_CATEGORY_ID_FIELD = config.PRODUCT_CATEGORY_ID_FIELD
    PRODUCT_IMAGE_FIELD = config.PRODUCT_IMAGE_FIELD
    PRODUCT_DISCOUNT_PRICE_FIELD = config.PRODUCT_DISCOUNT_PRICE_FIELD
    PRODUCT_CATEGORY_ID_LOOKUP_FIELD = config.PRODUCT_CATEGORY_ID_LOOKUP_FIELD
    PRODUCT_IMAGES_LOOKUP_FIELD = config.PRODUCT_IMAGES_LOOKUP_FIELD
    PRODUCT_REQUIRED_OPTIONS_FIELD = config.PRODUCT_REQUIRED_OPTIONS_FIELD
    PRODUCT_CATEGORIES_EXTRA_OPTIONS_FIELD = config.PRODUCT_CATEGORIES_EXTRA_OPTIONS_FIELD
    PRODUCT_CATEGORIES_EXTRA_OPTION_NAMES_FIELD = config.PRODUCT_CATEGORIES_EXTRA_OPTION_NAMES_FIELD
    PRODUCT_EXTRA_CHOICE_REQUIRED_FIELD = config.PRODUCT_EXTRA_CHOICE_REQUIRED_FIELD
    PRODUCT_ID_FIELD = config.PRODUCT_ID_FIELD
    PRODUCT_EXTERNAL_ID = config.PRODUCT_EXTERNAL_ID
    PRODUCT_CHECKOUT_MODE = config.PRODUCT_CHECKOUT_MODE
    NEW_ID_FIELD = config.NEW_ID_FIELD
    NOCODB_CHECKOUT_MODES = config.NOCODB_CHECKOUT_MODES


def get_pagination_info(page_info: dict) -> PaginationResponseModel:
    """
    Parses pagination information into a model.
    """
    return PaginationResponseModel(
        total_rows=page_info['totalRows'],
        page=page_info['page'],
        page_size=page_info['pageSize'],
        is_first_page=page_info['isFirstPage'],
        is_last_page=page_info['isLastPage']
    )


def parse_category_data(data: dict) -> CategoryResponseModel:
    """
    Parses raw category data into a structured model.
    """
    preview_url = data.get(CATEGORY_IMAGE_FIELD, [{}])[0].get("url", "") if data.get(CATEGORY_IMAGE_FIELD) else ""
    return CategoryResponseModel(
        id=str(data[ID_FIELD]),
        name=data.get(CATEGORY_NAME_FIELD, ""),
        parent_category=str(data.get(CATEGORY_PARENT_ID_FIELD, 0)),
        preview_url=preview_url,
    )


def dump_category_data(data: CategoryModel) -> dict:
    """
    Converts a CategoryModel into a dictionary suitable for API calls.
    """
    return {
        CATEGORY_NAME_FIELD: data.name,
        CATEGORY_PARENT_FIELD: data.parent_category,
        CATEGORY_IMAGE_FIELD: [
            {"url": data.preview_url, "title": f"{secrets.token_hex(6)}.jpeg", "mimetype": "image/jpeg"}
        ]
    }


def dump_product_data(data: ProductModel) -> dict:
    """
    Converts a ProductModel into a dictionary suitable for API calls.
    """
    preview_url = [
        {"url": image_url, "title": f"{secrets.token_hex(6)}.jpeg", "mimetype": "image/jpeg"}
        for image_url in data.preview_url
    ] if data.preview_url else []

    return {
        PRODUCT_NAME_FIELD: data.name,
        PRODUCT_DESCRIPTION_FIELD: data.description,
        PRODUCT_PRICE_FIELD: data.price,
        PRODUCT_CURRENCY_FIELD: data.currency,
        PRODUCT_STOCK_FIELD: data.stock_qty,
        PRODUCT_CATEGORY_NAME_FIELD: [data.category_name] if data.category_name else None,
        PRODUCT_CATEGORY_ID_FIELD: [{"Id": data.category}] if data.category else None,
        PRODUCT_IMAGE_FIELD: preview_url,
        PRODUCT_DISCOUNT_PRICE_FIELD: data.final_price
    }


def dump_product_data_with_check(data: ProductModel, data_check: dict) -> dict:
    """
    Converts a ProductModel into a dictionary and validates categories.
    """
    preview_url = [
        {"url": image_url, "title": f"{secrets.token_hex(6)}.jpeg", "mimetype": "image/jpeg"}
        for image_url in data.preview_url
    ] if data.preview_url else []

    extra_data = {attr.name: attr.description for attr in data.extra_attributes}

    product_data = {
        PRODUCT_ID_FIELD: data.id,
        PRODUCT_EXTERNAL_ID: data.external_id,
        PRODUCT_NAME_FIELD: data.name,
        PRODUCT_DESCRIPTION_FIELD: data.description,
        PRODUCT_PRICE_FIELD: data.price,
        PRODUCT_CURRENCY_FIELD: data.currency,
        PRODUCT_STOCK_FIELD: data.stock_qty,
        PRODUCT_CATEGORY_NAME_FIELD: [data.product_properties] if data.product_properties else None,
        PRODUCT_CATEGORY_ID_FIELD: [{"Id": data_check[item]} for item in data.product_properties] if data.product_properties else None,
        PRODUCT_IMAGE_FIELD: preview_url,
        PRODUCT_CHECKOUT_MODE: NOCODB_CHECKOUT_MODES,
        PRODUCT_DISCOUNT_PRICE_FIELD: data.final_price,
    }

    if extra_data:
        product_data.update(extra_data)
    return product_data


async def parse_product_data(data: dict) -> ProductModel:
    """
    Parses raw product data into a ProductModel.
    """
    preview_url = [image['url'] for image in data.get(PRODUCT_IMAGE_FIELD, [])]

    # Dynamically add extra attributes
    extra_attributes = [
        ExtraAttribute(name=key, description=str(value))
        for key, value in data.items()
        if key not in {
            ID_FIELD, PRODUCT_NAME_FIELD, PRODUCT_DESCRIPTION_FIELD, PRODUCT_PRICE_FIELD, PRODUCT_CURRENCY_FIELD,
            PRODUCT_STOCK_FIELD, PRODUCT_CATEGORY_ID_FIELD, PRODUCT_IMAGE_FIELD, PRODUCT_CATEGORY_NAME_FIELD,
            PRODUCT_DISCOUNT_PRICE_FIELD, PRODUCT_CATEGORY_ID_LOOKUP_FIELD, PRODUCT_REQUIRED_OPTIONS_FIELD,
            PRODUCT_CATEGORIES_EXTRA_OPTIONS_FIELD, PRODUCT_CATEGORIES_EXTRA_OPTION_NAMES_FIELD,
            PRODUCT_EXTRA_CHOICE_REQUIRED_FIELD, "UpdatedAt", "CreatedAt"
        } and value is not None and isinstance(value, (str, int, float))
    ]

    product = ProductModel(
        id=str(data.get(ID_FIELD, data.get(NEW_ID_FIELD, ""))),
        external_id=data.get(PRODUCT_EXTERNAL_ID, ""),
        name=data.get(PRODUCT_NAME_FIELD, ""),
        description=data.get(PRODUCT_DESCRIPTION_FIELD, ""),
        price=data.get(PRODUCT_PRICE_FIELD, 0.0),
        final_price=data.get(PRODUCT_DISCOUNT_PRICE_FIELD, 0.0),
        currency=data.get(PRODUCT_CURRENCY_FIELD, "RUB"),
        stock_qty=data.get(PRODUCT_STOCK_FIELD, 0),
        preview_url=preview_url,
        category_name=data.get(PRODUCT_CATEGORY_NAME_FIELD, []),
        category=data.get(PRODUCT_CATEGORY_ID_LOOKUP_FIELD, []),
        extra_attributes=extra_attributes,
        extra_option_choice_required=bool(data.get(PRODUCT_EXTRA_CHOICE_REQUIRED_FIELD, [])),

        metadata=data
    )
    
    return product
