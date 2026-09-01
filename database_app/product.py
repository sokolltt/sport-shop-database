from db import get_connection


def get_products():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                p.product_id,
                p.name,
                p.brand,
                p.price,
                s.company_name,
                p.category_id,
                p.article
            FROM product p
            JOIN supplier s
                ON p.supplier_id = s.supplier_id
            ORDER BY p.product_id;
        """)

        products = cursor.fetchall()
        return products

    finally:
        cursor.close()
        connection.close()


def add_product(name, brand, price, supplier_id, category_id, article):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO product
                (name, brand, price, supplier_id, category_id, article)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (
            name,
            brand,
            price,
            supplier_id,
            category_id,
            article
        ))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def update_product(
    product_id,
    name,
    brand,
    price,
    supplier_id,
    category_id,
    article
):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE product
            SET name = %s,
                brand = %s,
                price = %s,
                supplier_id = %s,
                category_id = %s,
                article = %s
            WHERE product_id = %s;
        """, (
            name,
            brand,
            price,
            supplier_id,
            category_id,
            article,
            product_id
        ))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def delete_product(product_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE FROM product
            WHERE product_id = %s;
        """, (product_id,))

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