import psycopg2
from analytics import (
    get_expensive_products,
    get_suppliers_by_product_count
)
from supplier import get_suppliers, add_supplier, update_supplier, delete_supplier
from product import get_products, add_product, update_product, delete_product


def show_suppliers():
    suppliers = get_suppliers()

    print("\nСписок поставщиков:")
    print("-" * 80)

    for supplier in suppliers:
        print(
            f"ID: {supplier[0]} | "
            f"Компания: {supplier[1]} | "
            f"Контактное лицо: {supplier[2]} | "
            f"Телефон: {supplier[3]}"
        )

    print("-" * 80)

def analytics_menu():
    while True:
        print("\n=== Аналитические запросы ===")
        print("1. Товары дороже указанной цены")
        print("2. Поставщики с заданным количеством товаров")
        print("0. Назад")

        choice = input("Выберите действие: ")

        if choice == "1":
            try:
                min_price = float(
                    input("Введите минимальную цену: ")
                )

                products = get_expensive_products(min_price)

                if not products:
                    print("Товары не найдены.")
                else:
                    print("\nРезультаты:")

                    for product in products:
                        print(
                            f"Название: {product[0]} | "
                            f"Бренд: {product[1]} | "
                            f"Цена: {product[2]} | "
                            f"Поставщик: {product[3]} | "
                            f"Артикул: {product[4]}"
                        )

            except ValueError:
                print("Ошибка: цена должна быть числом.")

        elif choice == "2":
            try:
                min_count = int(
                    input("Введите минимальное количество товаров: ")
                )

                suppliers = get_suppliers_by_product_count(min_count)

                if not suppliers:
                    print("Поставщики не найдены.")
                else:
                    print("\nРезультаты:")

                    for supplier in suppliers:
                        print(
                            f"Компания: {supplier[0]} | "
                            f"Контактное лицо: {supplier[1]} | "
                            f"Количество товаров: {supplier[2]}"
                        )

            except ValueError:
                print("Ошибка: количество должно быть целым числом.")

        elif choice == "0":
            break

        else:
            print("Неверный выбор.")

def supplier_menu():
    while True:
        print("\n=== Работа с поставщиками ===")
        print("1. Показать поставщиков")
        print("2. Добавить поставщика")
        print("3. Изменить поставщика")
        print("4. Удалить поставщика")
        print("0. Назад")

        choice = input("Выберите действие: ")

        if choice == "1":
            show_suppliers()


        elif choice == "2":
            company_name = input("Название компании: ")
            contact_person = input("Контактное лицо: ")
            phone = input("Телефон: ")
            try:
                add_supplier(company_name, contact_person, phone)
                print("Поставщик успешно добавлен.")

            except psycopg2.errors.UniqueViolation:
                print(
                    "Поставщик с таким названием компании "
                    "уже существует."
                )

            except Exception as error:
                print(f"Ошибка при добавлении поставщика: {error}")

        elif choice == "3":
            supplier_id = int(input("ID поставщика: "))
            company_name = input("Новое название компании: ")
            contact_person = input("Новое контактное лицо: ")
            phone = input("Новый телефон: ")

            update_supplier(
                supplier_id,
                company_name,
                contact_person,
                phone
            )

            print("Поставщик успешно изменён.")



        elif choice == "4":
            try:
                supplier_id = int(input("ID поставщика: "))
                deleted = delete_supplier(supplier_id)
                if deleted:
                    print("Поставщик успешно удалён.")
                else:
                    print("Поставщик с таким ID не найден.")

            except ValueError:
                print("Ошибка: ID поставщика должен быть числом.")

            except psycopg2.errors.ForeignKeyViolation:
                print(
                    "Нельзя удалить поставщика: "
                    "с ним связаны товары."
                )

            except Exception as error:
                print(f"Ошибка при удалении поставщика: {error}")

        elif choice == "0":
            break

        else:
            print("Некорректный пункт меню.")


def show_products():
    products = get_products()

    print("\nСписок товаров:")
    print("-" * 120)

    for product in products:
        print(
            f"ID: {product[0]} | "
            f"Название: {product[1]} | "
            f"Бренд: {product[2]} | "
            f"Цена: {product[3]} | "
            f"Поставщик: {product[4]} | "
            f"Категория: {product[5]} | "
            f"Артикул: {product[6]}"
        )

    print("-" * 120)


def product_menu():
    while True:
        print("\n=== Работа с товарами ===")
        print("1. Показать товары")
        print("2. Добавить товар")
        print("3. Изменить товар")
        print("4. Удалить товар")
        print("0. Назад")

        choice = input("Выберите действие: ")

        if choice == "1":
            show_products()

        elif choice == "2":
            try:
                name = input("Название товара: ")
                brand = input("Бренд: ")
                price = float(input("Цена: "))
                supplier_id = int(input("ID поставщика: "))
                category_id = int(input("ID категории: "))
                article = input("Артикул: ")

                add_product(
                    name,
                    brand,
                    price,
                    supplier_id,
                    category_id,
                    article
                )

                print("Товар успешно добавлен.")

            except ValueError:
                print("Ошибка: цена и идентификаторы должны быть числами.")

            except psycopg2.errors.UniqueViolation:
                print("Товар с таким артикулом уже существует.")

            except psycopg2.errors.ForeignKeyViolation:

                print(
                    "Ошибка: указанный поставщик или категория "
                    "не существуют."
                )

            except Exception as error:
                print(f"Ошибка при добавлении товара: {error}")


        elif choice == "3":
            try:

                product_id = int(input("ID товара: "))
                name = input("Новое название товара: ")
                brand = input("Новый бренд: ")
                price = float(input("Новая цена: "))
                supplier_id = int(input("ID поставщика: "))
                category_id = int(input("ID категории: "))
                article = input("Новый артикул: ")

                update_product(
                    product_id,
                    name,
                    brand,
                    price,
                    supplier_id,
                    category_id,
                    article
                )

                print("Товар успешно изменён.")

            except ValueError:
                print("Ошибка: цена и идентификаторы должны быть числами.")

            except psycopg2.errors.UniqueViolation:
                print("Товар с таким артикулом уже существует.")

            except psycopg2.errors.ForeignKeyViolation:
                print(
                    "Ошибка: указанный поставщик или категория "
                    "не существуют."
                )

            except Exception as error:
                print(f"Ошибка при изменении товара: {error}")



        elif choice == "4":
            try:
                product_id = int(input("ID товара: "))
                deleted = delete_product(product_id)

                if deleted:
                    print("Товар успешно удалён.")

                else:
                    print("Товар с таким ID не найден.")

            except ValueError:
                print("Ошибка: ID товара должен быть числом.")

            except Exception as error:
                print(f"Ошибка при удалении товара: {error}")

        elif choice == "0":
            break

        else:
            print("Некорректный пункт меню.")


def main():
    while True:
        print("\n=== Главное меню ===")
        print("1. Работа с поставщиками")
        print("2. Работа с товарами")
        print("3. Аналитические запросы")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            supplier_menu()

        elif choice == "2":
            product_menu()

        elif choice == "3":
            analytics_menu()

        elif choice == "0":
            print("Программа завершена.")
            break

        else:
            print("Некорректный пункт меню.")


if __name__ == "__main__":
    main()
