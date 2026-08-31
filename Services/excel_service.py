import pandas as pd

from Database.queries import tracking_code_exists

REQUIRED_COLUMNS = [
    "نام",
    "نام خانوادگی",
    "موبایل",
    "کد پیگیری",
    "شهر"
]


def read_excel(file_path):
    try:
        df = pd.read_excel(file_path, dtype=str)
        df.columns = df.columns.astype(str).str.strip()
        return df
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return None


def validate_columns(df):
    if df is None:
        return False

    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            return False

    return True


def select_required_columns(df):

    return df[REQUIRED_COLUMNS].copy()


def normalize_digits(value):
    value = str(value)

    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    english_digits = "0123456789"

    # نکته‌ی مهم: باید دو رشته‌ی جدا بدیم (مبدا، مقصد)
    translation_table = str.maketrans(persian_digits, english_digits)

    return value.translate(translation_table)


def validate_phone(phone):
    phone = normalize_digits(phone)

    if not phone.isdigit():
        return False

    if len(phone) != 11:
        return False

    return True


def validate_tracking_code(tracking_code):
    tracking_code = normalize_digits(tracking_code)

    if not tracking_code.isdigit():
        return False

    if len(tracking_code) != 24:
        return False

    return True


def validate_rows(df):
    valid_rows = []
    invalid_rows = []

    for index, row in df.iterrows():
        first_name = str(row["نام"]).strip()
        last_name = str(row["نام خانوادگی"]).strip()
        phone = normalize_digits(str(row["موبایل"]).strip())
        tracking_code = normalize_digits(str(row["کد پیگیری"]).strip())
        city = str(row["شهر"]).strip()

        if not first_name:
            invalid_rows.append(index)
            continue

        if not last_name:
            invalid_rows.append(index)
            continue

        if not validate_phone(phone):
            invalid_rows.append(index)
            continue

        if not validate_tracking_code(tracking_code):
            invalid_rows.append(index)
            continue

        if not city:
            invalid_rows.append(index)
            continue

        valid_rows.append({
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "tracking_code": tracking_code,
            "city": city
        })

    return valid_rows, invalid_rows


