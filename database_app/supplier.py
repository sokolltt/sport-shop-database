from db import get_connection


def get_suppliers():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT supplier_id, company_name, contact_person, phone
        FROM supplier
        ORDER BY supplier_id;
    """)

    suppliers = cursor.fetchall()

    cursor.close()
    connection.close()

    return suppliers


def add_supplier(company_name, contact_person, phone):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO supplier (company_name, contact_person, phone)
            VALUES (%s, %s, %s);
        """, (company_name, contact_person, phone))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def update_supplier(supplier_id, company_name, contact_person, phone):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE supplier
        SET company_name = %s,
            contact_person = %s,
            phone = %s
        WHERE supplier_id = %s;
    """, (company_name, contact_person, phone, supplier_id))

    connection.commit()

    cursor.close()
    connection.close()


def delete_supplier(supplier_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE FROM supplier
            WHERE supplier_id = %s;
        """, (supplier_id,))

        if cursor.rowcount == 0:
            connection.rollback()
            return False

        connection.commit()
        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()