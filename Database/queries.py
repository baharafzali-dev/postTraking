import psycopg2
from schema import db_url



def get_connection():

    conn = psycopg2.connect(db_url)

    conn.row_factory = psycopg2.Row

    return conn



def tracking_code_exists(tracking_code):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
        SELECT id
        FROM shipments
        WHERE tracking_code = ?
    ''', (tracking_code,))

    result = cur.fetchone()

    conn.close()

    return result is not None


def add_shipment(
    first_name,
    last_name,
    phone,
    tracking_code,
    shipment_date,
    city
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
        INSERT INTO shipments (
            first_name,
            last_name,
            phone,
            tracking_code,
            shipment_date,
            city
        )
        VALUES (%s, %s, %s, %s, %s ,%s)
    ''', (
        first_name,
        last_name,
        phone,
        tracking_code,
        shipment_date,
        city
    ))

    conn.commit()
    conn.close()


def search_shipments(
    first_name,
    last_name,
    phone
):

    conn = get_connection()
    cur = conn.cursor()
    
    print("SEARCH:")
    print("first_name:", repr(first_name))
    print("last_name:", repr(last_name))
    print("phone:", repr(phone))
    
    cur.execute("""
        SELECT *
        FROM shipments
        WHERE first_name = ?
        AND last_name = ?
        AND phone = ?
        ORDER BY id DESC
    """, (
        first_name,
        last_name,
        phone
    ))

    results = cur.fetchall()
    
    print("RESULTS:", len(results))

    for result in results:
        print(dict(result))

    conn.close()

    return results


def get_shipment_by_id(shipment_id):
    
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute('''
        SELECT * 
        FROM shipments
        WHERE id = ?
    ''',(shipment_id,))
    
    result = cur.fetchone()
    
    conn.close()
    
    return result