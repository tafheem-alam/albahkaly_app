import frappe
from frappe.model.document import Document


class KYCRequest(Document):
    pass


def sync_to_customer(doc, method=None):

    # Mandatory check
    if not doc.entity_name__full_legal_name_ or not doc.customer_type:
        frappe.throw(
            "Full Legal Name and Customer Type are mandatory for Customer creation"
        )

    # 🔍 DUPLICATION CHECK
    existing_customer = frappe.db.exists(
        "Customer",
        {
            "customer_name": doc.entity_name__full_legal_name_,
            "customer_type": doc.customer_type,
        }
    )

    if existing_customer:
        frappe.throw(
            f"Customer already exists: <b>{existing_customer}</b>"
        )

    # ✅ Create Customer
    customer = frappe.new_doc("Customer")
    #frappe.msgprint(f"customer {customer}")
    
    customer.customer_name = doc.entity_name__full_legal_name_
    customer.customer_type = doc.customer_type

    FIELD_MAP = {
        "entity_name": "customer_name",
        "entity_name__full_legal_name__arabic": "custom_entity_name__full_legal_name__arabic",
        "unified_registration_number": "custom_unified_registration_number",
        "activities": "custom_activities",
        "trade_brand_name": "custom_trade_brand_name",
        "vat_number": "custom_vat_number",
        "entity_type": "custom_entity_type",
        "commercial_registration_cr": "custom_commercial_registration_cr",
        "cr_expiry_date": "custom_cr_expiry_date",

        "building_number": "custom_building_number",
        "street_name": "custom_street_name",
        "region": "custom_region",
        "city": "custom_city",
        "postal_code": "custom_postal_code",
        "additional_number": "custom_additional_number",
        "unit_number":"custom_unit_number",
        "short_national_address": "custom_short_national_address",
		
        "name1": "custom_name",
        "id": "custom_id",
        "nationality": "custom_nationality",
        "job": "custom_job",
        "mobile_number":"custom_mobile_number",
        "email":"custom_email",
		"mobile": "custom_mobile",

        "department": "custom_department",
        "name_of_responsible_person": "custom_name_of_responsible_person",
        "finance_email_for_invoicing": "custom_finance_email_for_invoicing",
        
        "department_2": "custom_department_2",
        "name_of_responsible_person_2": "custom_name_of_responsible_person_2",
        "finance_email_for_invoicing_2": "custom_finance_email_for_invoicing_2",
		"email_2": "custom_email_2",
        "mobile_number_2": "custom_mobile_number_2",		

        "expected_shipments_monthly_import": "custom_expected_shipments_monthly_import",
        "expected_shipments_monthly_export": "custom_expected_shipments_monthly_export",
        "delivery_locations__in_ksa_": "custom_delivery_locations_in_ksa",
        "shipment_type": "custom_shipment_type",		
        
        "warehouse_city": "custom_warehouse_city",
        "district": "custom_district",
        "remarks": "custom_comments",
    }
	
    ATTACH_FIELD_MAP = {
    "commercial_register_cr_": "custom_commercial_register_cr_",
    "identities_of_authorized_signatories": "custom_identities_of_authorized_signatories",
    "vat_registration_certificate": "custom_vat_registration_certificate",
    "national_address": "custom_customer_national_address",
    "busniess_licenses": "custom_busniess_licenses",
}

    # Copy fields
    for kyc_field, customer_field in FIELD_MAP.items():
        if doc.get(kyc_field) is not None:
            customer.set(customer_field, doc.get(kyc_field))

    for kyc_field, customer_field in ATTACH_FIELD_MAP.items():
        if doc.get(kyc_field):
            customer.set(customer_field, doc.get(kyc_field))
            
    value = doc.get("delivery_locations_in_ksa")
    
    #frappe.msgprint(f"Value{value}")
    
    if value is not None:
        customer.set("custom_delivery_locations_in_ksa", str(value))

    customer.insert(ignore_permissions=True)

    frappe.msgprint(
        f"Customer <b>{customer.name}</b> created successfully from KYC Request"
    )
