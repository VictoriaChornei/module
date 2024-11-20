import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_name): #завантаження даних з файлу
    try:
        return pd.read_csv(file_name)
    except FileNotFoundError:
        print("Файл не знайдено! Створюється новий файл.")
        return pd.DataFrame(columns=["Ім'я клієнта", "Номер замовлення", "Дата замовлення", "Сума замовлення", "Статус"])

def save_data(df, file_name): #збереження даних у файл
    try:
        df.to_csv(file_name, index=False)
        print("Дані успішно збережено!")
    except Exception as e:
        print(f"Помилка збереження даних: {e}")

def add_order(df): #додавання замовлення
    try:
        name = input("Ім'я клієнта: ")
        order_number = int(input("Номер замовлення: "))
        order_date = input("Дата замовлення (рррр-мм-дд): ")
        order_sum = float(input("Сума замовлення: "))
        status = input("Статус (Виконано/В процесі): ")
        new_order = {"Ім'я клієнта": name, "Номер замовлення": order_number, "Дата замовлення": order_date,
                     "Сума замовлення": order_sum, "Статус": status}
        return pd.concat([df, pd.DataFrame([new_order])], ignore_index=True)
    except ValueError:
        print("Помилка: невірний формат даних.")
        return df

def edit_order(df): #редагування замовлення
    try:
        order_number = int(input("Введіть номер замовлення для редагування: "))
        if order_number in df['Номер замовлення'].values:
            idx = df[df['Номер замовлення'] == order_number].index[0]
            print("Редагування інформації для замовлення №", order_number)
            df.loc[idx, "Ім'я клієнта"] = input("Ім'я клієнта: ")
            df.loc[idx, "Дата замовлення"] = input("Дата замовлення (рррр-мм-дд): ")
            df.loc[idx, "Сума замовлення"] = float(input("Сума замовлення: "))
            df.loc[idx, "Статус"] = input("Статус (Виконано/В процесі): ")
            print("Замовлення оновлено!")
        else:
            print("Замовлення з таким номером не знайдено.")
    except ValueError:
        print("Помилка: невірний формат даних.")
    return df

def delete_order(df): #видалення замовлення 
    try:
        order_number = int(input("Введіть номер замовлення для видалення: "))
        if order_number in df['Номер замовлення'].values:
            df = df[df['Номер замовлення'] != order_number]
            print(f"Замовлення №{order_number} видалено.")
        else:
            print("Замовлення з таким номером не знайдено.")
    except ValueError:
        print("Помилка: номер замовлення повинен бути числом.")
    return df

def list_orders(df): 
    if df.empty:
        print("Список замовлень порожній.")
    else:
        print("\nСписок замовлень:")
        print(df)

def analyze_orders(df): #підрахунок кількості замовлень і сумарної вартості
    total_orders = len(df)
    total_sum = df["Сума замовлення"].sum()
    print(f"Загальна кількість замовлень: {total_orders}")
    print(f"Сумарна вартість замовлень: {total_sum}")

def analyze_by_status(df):
    print("Замовлення за статусами:")
    print(df['Статус'].value_counts())

def find_max_order(df): #пошук замовлень з найбільною сумою
    if df.empty:
        print("Список замовлень порожній.")
    else:
        max_order = df.loc[df['Сума замовлення'].idxmax()]
        print("Замовлення з найбільшою сумою:")
        print(max_order)


def visualize_status(df): #побудова кругової діаграми
    if df.empty:
        print("Список замовлень порожній.")
        return
    status_counts = df['Статус'].value_counts()
    plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%')
    plt.title("Частка виконаних та невиконаних замовлень")
    plt.show()

def visualize_dates(df): #побудова гістограми кількості замовлень за датами
    if df.empty:
        print("Список замовлень порожній.")
        return
    df['Дата замовлення'] = pd.to_datetime(df['Дата замовлення'], errors='coerce')
    orders_by_date = df['Дата замовлення'].value_counts().sort_index()
    orders_by_date.plot(kind='bar', title='Кількість замовлень за датами')
    plt.xlabel('Дата')
    plt.ylabel('Кількість замовлень')
    plt.show()

def main():
    file_name = "file.csv"
    data = load_data(file_name)

    while True:
        print("\nМеню:")
        print("1. Завантажити список замовлень")
        print("2. Зберегти список замовлень")
        print("3. Додати нове замовлення")
        print("4. Редагувати замовлення")
        print("5. Видалити замовлення")
        print("6. Вивести список замовлень")
        print("7. Аналіз кількості та вартості замовлень")
        print("8. Аналіз замовлень за статусом")
        print("9. Знайти замовлення з найбільшою сумою")
        print("10. Побудувати кругову діаграму")
        print("11. Побудувати гістограму за датами")
        print("12. Вийти")

        choice = input("Введіть номер операції: ")

        if choice == "1":
            data = load_data(file_name)
        elif choice == "2":
            save_data(data, file_name)
        elif choice == "3":
            data = add_order(data)
        elif choice == "4":
            data = edit_order(data)
        elif choice == "5":
            data = delete_order(data)
        elif choice == "6":
            list_orders(data)
        elif choice == "7":
            analyze_orders(data)
        elif choice == "8":
            analyze_by_status(data)
        elif choice == "9":
            find_max_order(data)
        elif choice == "10":
            visualize_status(data)
        elif choice == "11":
            visualize_dates(data)
        elif choice == "12":
            print("Програму завершено.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
