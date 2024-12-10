"""Models."""

from typing import Literal

from pydantic import BaseModel, Field

DATE_REGEX = "[0-9]{2}/[0-9]{2}/[0-9]{4}|[0-9]{2}"


class Customer(BaseModel):
    """Customer model."""

    company_name: str = Field(serialization_alias="CompanyName")
    customer_source: str | None = Field(None, serialization_alias="CustomerSource")
    customer_type: str | None = Field(None, serialization_alias="CustomerType")
    invoice_notes: str | None = Field(None, serialization_alias="InvoiceNotes")
    main_email: str | None = Field(None, serialization_alias="MainEmail")
    sales_group: str | None = Field(None, serialization_alias="SalesGroup")
    tax_exempt: Literal[0, 1] | None = Field(None, serialization_alias="TaxExempt")
    tax_exempt_number: str | None = Field(None, serialization_alias="TaxExemptNumber")
    website: str | None = Field(None, serialization_alias="WebSite")
    custom_date_field_1: str | None = Field(None, pattern=DATE_REGEX, serialization_alias="CustomDateField01")
    custom_date_field_2: str | None = Field(None, pattern=DATE_REGEX, serialization_alias="CustomDateField02")
    custom_date_field_3: str | None = Field(None, pattern=DATE_REGEX, serialization_alias="CustomDateField03")
    custom_date_field_4: str | None = Field(None, pattern=DATE_REGEX, serialization_alias="CustomDateField04")
    custom_field_1: str | None = Field(None, serialization_alias="CustomField01")
    custom_field_2: str | None = Field(None, serialization_alias="CustomField02")
    custom_field_3: str | None = Field(None, serialization_alias="CustomField03")
    custom_field_4: str | None = Field(None, serialization_alias="CustomField04")
    custom_field_5: str | None = Field(None, serialization_alias="CustomField05")
    custom_field_6: str | None = Field(None, serialization_alias="CustomField06")
    customer_reminder_invoice_notes: str | None = Field(None, serialization_alias="CustomerReminderInvoiceNotes")
    billing_company: str | None = Field(None, serialization_alias="BillingCompany")
    billing_address01: str | None = Field(None, serialization_alias="BillingAddress01")
    billing_address02: str | None = Field(None, serialization_alias="BillingAddress02")
    billing_city: str | None = Field(None, serialization_alias="BillingCity")
    billing_state: str | None = Field(None, serialization_alias="BillingState")
    billing_zip: str | None = Field(None, serialization_alias="BillingZip")
    billing_country: str | None = Field(None, serialization_alias="BillingCountry")


class LocationDetail(BaseModel):
    """LocationDetail model."""

    color: str | None = Field(None, serialization_alias="Color")
    parameter_label: str | None = Field(None, serialization_alias="ParameterLabel")
    parameter_value: str | None = Field(None, serialization_alias="ParameterValue")
    text: str | None = Field(None, serialization_alias="Text")
    custom_field_1: str | None = Field(None, serialization_alias="CustomField01")
    custom_field_2: str | None = Field(None, serialization_alias="CustomField02")
    custom_field_3: str | None = Field(None, serialization_alias="CustomField03")
    custom_field_4: str | None = Field(None, serialization_alias="CustomField04")
    custom_field_5: str | None = Field(None, serialization_alias="CustomField05")


class Location(BaseModel):
    """Location model."""

    location: str | None = Field(None, serialization_alias="Location")
    total_colors: str | None = Field(None, serialization_alias="TotalColors")
    total_flashes: str | None = Field(None, serialization_alias="TotalFlashes")
    total_stitches: str | None = Field(None, serialization_alias="TotalStitches")
    design_code: str | None = Field(None, serialization_alias="DesignCode")
    custom_field_1: str | None = Field(None, serialization_alias="CustomField01")
    custom_field_2: str | None = Field(None, serialization_alias="CustomField02")
    custom_field_3: str | None = Field(None, serialization_alias="CustomField03")
    custom_field_4: str | None = Field(None, serialization_alias="CustomField04")
    custom_field_5: str | None = Field(None, serialization_alias="CustomField05")
    image_url: str | None = Field(None, serialization_alias="ImageURL")
    notes: str | None = Field(None, serialization_alias="Notes")
    location_details: list[LocationDetail] | None = Field(None, serialization_alias="LocationDetails")


class Design(BaseModel):
    """Design model."""

    design_name: str | None = Field(None, serialization_alias="DesignName")
    external_design_id: str | None = Field(None, serialization_alias="ExtDesignID")
    design_id: int | None = Field(None, serialization_alias="id_Design")
    design_type_id: int | None = Field(None, serialization_alias="id_DesignType")
    artist_id: int | None = Field(None, serialization_alias="id_Artist")
    for_product_color: str | None = Field(None, serialization_alias="ForProductColor")
    thread_break: str | None = Field(None, serialization_alias="ThreadBreak")
    vendor_design_id: str | None = Field(None, serialization_alias="VendorDesignID")
    custom_field_1: str | None = Field(None, serialization_alias="CustomField01")
    custom_field_2: str | None = Field(None, serialization_alias="CustomField02")
    custom_field_3: str | None = Field(None, serialization_alias="CustomField03")
    custom_field_4: str | None = Field(None, serialization_alias="CustomField04")
    custom_field_5: str | None = Field(None, serialization_alias="CustomField05")
    locations: list[Location] | None = Field(None, serialization_alias="Locations")


class LinesOEItem(BaseModel):
    """LinesOEItem model."""

    part_number: str | None = Field(None, serialization_alias="PartNumber")
    color: str | None = Field(None, serialization_alias="Color")
    description: str | None = Field(None, serialization_alias="Description")
    size: str | None = Field(None, serialization_alias="Size")
    quantity: int | None = Field(None, serialization_alias="Qty")
    price: float | None = Field(None, serialization_alias="Price")
    product_class_id: int | None = Field(None, serialization_alias="id_ProductClass")
    custom_field_1: str | None = Field(None, serialization_alias="CustomField01")
    custom_field_2: str | None = Field(None, serialization_alias="CustomField02")
    custom_field_3: str | None = Field(None, serialization_alias="CustomField03")
    custom_field_4: str | None = Field(None, serialization_alias="CustomField04")
    custom_field_5: str | None = Field(None, serialization_alias="CustomField05")
    name_first: str | None = Field(None, serialization_alias="NameFirst")
    name_last: str | None = Field(None, serialization_alias="NameLast")
    line_item_notes: str | None = Field(None, serialization_alias="LineItemNotes")
    work_order_notes: str | None = Field(None, serialization_alias="WorkOrderNotes")
    design_id_block: str | None = Field(None, serialization_alias="DesignIDBlock")
    external_design_id_block: str | None = Field(None, serialization_alias="ExtDesignIDBlock")
    external_ship_id: str | None = Field(None, serialization_alias="ExtShipID")


class Note(BaseModel):
    """Note model."""

    note: str = Field(serialization_alias="Note")
    type_: (
        Literal[
            "Notes On Order",
            "Notes To Art",
            "Notes To Purchasing",
            "Notes To Subcontract",
            "Notes To Production",
            "Notes To Receiving",
            "Notes To Shipping",
            "Notes To Accounting",
            "Notes On Customer",
        ]
        | None
    ) = Field(None, serialization_alias="Type")


class Payment(BaseModel):
    """Payment model."""

    date_payment: str = Field(serialization_alias="date_Payment")
    account_number: str | None = Field(None, serialization_alias="AccountNumber")
    amount: int = Field(serialization_alias="Amount")
    auth_code: str | None = Field(None, serialization_alias="AuthCode")
    credit_card_company: str | None = Field(None, serialization_alias="CreditCardCompany")
    gateway: str | None = Field(None, serialization_alias="Gateway")
    response_code: str | None = Field(None, serialization_alias="ResponseCode")
    response_reason_code: str | None = Field(None, serialization_alias="ResponseReasonCode")
    response_reason_text: str | None = Field(None, serialization_alias="ResponseReasonText")
    status: Literal["success"] = Field(serialization_alias="Status")


class ShippingAddress(BaseModel):
    """ShippingAddress model."""

    external_shipment_id: str | None = Field(None, serialization_alias="ExtShipID")

    shipping_method: str | None = Field(None, serialization_alias="ShipMethod")

    company: str | None = Field(None, serialization_alias="ShipCompany")
    address1: str | None = Field(None, serialization_alias="ShipAddress01")
    address2: str | None = Field(None, serialization_alias="ShipAddress02")
    city: str | None = Field(None, serialization_alias="ShipCity")
    state: str | None = Field(None, serialization_alias="ShipState")
    postal_code: str | None = Field(None, serialization_alias="ShipZip")
    country: str | None = Field(None, serialization_alias="ShipCountry")


class Attachment(BaseModel):
    """Attachment model."""

    medial_url: str | None = Field(None, serialization_alias="MediaURL")
    media_name: str | None = Field(None, serialization_alias="MediaName")
    link_url: str | None = Field(None, serialization_alias="LinkURL")
    link_note: str | None = Field(None, serialization_alias="LinkNote")
    link: Literal[0, 1] | None = Field(None, serialization_alias="Link")


class Order(BaseModel):
    """Order model."""

    api_source: str | None = Field(serialization_alias="APISource")
    external_order_id: str = Field(serialization_alias="ExtOrderID")
    external_source: str = Field(serialization_alias="ExtSource")
    external_customer_id: str | None = Field(None, serialization_alias="ExtCustomerID")
    external_customer_pref: str | None = Field(None, serialization_alias="ExtCustomerPref")
    date_order_placed: str | None = Field(None, pattern=DATE_REGEX, serialization_alias="date_OrderPlaced")
    date_order_requested_to_ship: str | None = Field(None, pattern=DATE_REGEX, serialization_alias="date_OrderRequestedToShip")
    date_order_drop_dead: str | None = Field(None, pattern=DATE_REGEX, serialization_alias="date_OrderDropDead")
    order_type_id: int | None = Field(None, serialization_alias="id_OrderType")
    sales_status_id: int | None = Field(None, serialization_alias="id_SalesStatus")
    employee_created_by: int | None = Field(None, serialization_alias="id_EmpCreatedBy")
    customer_id: int | None = Field(None, serialization_alias="id_Customer")
    contact_email: str | None = Field(None, serialization_alias="ContactEmail")
    contact_name_first: str | None = Field(None, serialization_alias="ContactNameFirst")
    contact_name_last: str | None = Field(None, serialization_alias="ContactNameLast")
    contact_phone: str | None = Field(None, serialization_alias="ContactPhone")
    customer_purchase_order: str | None = Field(None, serialization_alias="CustomerPurchaseOrder")
    customer_service_rep: str | None = Field(None, serialization_alias="CustomerSeviceRep")
    on_hold: Literal[0, 1] | None = Field(None, serialization_alias="OnHold")
    terms: str | None = Field(None, serialization_alias="Terms")
    discount_part_number: str | None = Field(None, serialization_alias="DiscountPartNumber")
    discount_part_description: str | None = Field(None, serialization_alias="DiscountPartDescription")
    cur_shipping: int | None = Field(None, serialization_alias="cur_Shipping")
    tax_total: int | None = Field(None, serialization_alias="TaxTotal")
    total_discounts: int | None = Field(None, serialization_alias="TotalDiscounts")
    customer: Customer | None = Field(None, serialization_alias="Customer")
    designs: list[Design] | None = Field(None, serialization_alias="Designs")
    line_items: list[LinesOEItem] | None = Field(None, serialization_alias="LinesOE")
    notes: list[Note] | None = Field(None, serialization_alias="Notes")
    payments: list[Payment] | None = Field(None, serialization_alias="Payments")
    addresses: list[ShippingAddress] | None = Field(None, serialization_alias="ShippingAddresses")
    attachments: list[Attachment] | None = Field(None, serialization_alias="Attachments")
