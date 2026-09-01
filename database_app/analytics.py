from db import get_connection


def get_expensive_products(min_price):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                p.name,
                p.brand,
                p.price,
                s.company_name,
                p.article
            FROM product p
            JOIN supplier s
                ON p.supplier_id = s.supplier_id
            WHERE p.price >= %s
            ORDER BY p.price DESC;
        """, (min_price,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_suppliers_by_product_count(min_count):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                s.company_name,
                s.contact_person,
                COUNT(p.product_id) AS product_count
            FROM supplier s
            JOIN product p
                ON s.supplier_id = p.supplier_id
            GROUP BY
                s.supplier_id,
                s.company_name,
                s.contact_person
            HAVING COUNT(p.product_id) >= %s
            ORDER BY product_count DESC;
        """, (min_count,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()