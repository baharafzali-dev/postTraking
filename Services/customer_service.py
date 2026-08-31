from Database.queries import (
    search_shipments,
    get_shipment_by_id
)


def find_customer_shipments(
    first_name,
    last_name,
    phone
):
    
    return search_shipments(
        first_name,
        last_name,
        phone
    )
    
def get_customer_shipment(shipment_id):
    
    return get_shipment_by_id(
        shipment_id
    )
    
def format_shipment_message(shipment):

    return (
        "📦 مرسوله شما:\n\n"
        f"👤 نام و نام خانوادگی: "
        f"{shipment['first_name']} {shipment['last_name']}\n"
        f"📱 شماره تماس: {shipment['phone']}\n\n"
        f"📍 به مقصد: {shipment['city']}\n\n"
        f"🔖 کد پیگیری: `{shipment['tracking_code']}`\n"
        f"📅 تاریخ: {shipment['shipment_date']}\n\n"
        "رهسپار شد.\n\n"
        "جهت رهگیری مرسوله پستی ابتدا با انتخاب گزینه "
        "کپی کردن کد پیگیری بزنید و سپس از طریق "
        "دکمه زیر وارد سایت پست شوید و سایر "
        "اطلاعات مربوط به مرسوله خود را پیگیری کنید."
    )