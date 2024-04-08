from collections import UserDict
from datetime import datetime, timedelta


class Field: #Базовий клас для полів запису.
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
    

class Name(Field): #Клас для зберігання імені контакту. Обов'язкове поле.
    def __init__(self, name=None):
        if name is None:
            raise ValueError
        super().__init__(name) # self.value = name


class Phone(Field): #Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
    def __init__(self, phone): 
        if len(phone) != 10: #лише 10 знаків 
            raise ValueError #в іншому випадку помилка
        super().__init__(phone) # self.value = phone

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Не вірний формат дати. Введіть DD.MM.YYYY")
        
class AddressBook(UserDict):
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.values():
            if record.birthday:
                birthday_date = record.birthday.value.date().replace(year=today.year)
                if birthday_date < today:
                    birthday_date = birthday_date.replace(year=today.year + 1)
                days_until_birthday = (birthday_date - today).days

                if 0 <= days_until_birthday <= 7:
                    if birthday_date.weekday() >= 5:
                        birthday_date += timedelta(days=(7 - birthday_date.weekday()))
                    upcoming_birthdays.append({
                        'name': record.name.value,
                        'congratulation_date': birthday_date.strftime("%Y.%m.%d")
                    })

        return upcoming_birthdays

class Record: #Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
    def __init__(self, name): # record = Record('Hanna')
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone): #додавання
        for p in self.phones:
            if p.value == phone: #'123' != 123
                return
        self.phones.append(Phone(phone))

    def add_birthday(args, book):
        name, birthday = args
        if name not in book:
            return f"No record found for {name}."
        try:
            book[name].birthday = Birthday(birthday)
            return f"Birthday added for {name}."
        except ValueError as e:
            return str(e)
        
    def show_birthday(args, book):
        name = args[0]
        if name not in book:
            return f"No record found for {name}."
        if not book[name].birthday:
            return f"No birthday found for {name}."
        return f"Birthday of {name}: {book[name].birthday.value.strftime('%d.%m.%Y')}"

    def birthdays(args, book):
        upcoming_birthdays = book.get_upcoming_birthdays()
        if not upcoming_birthdays:
            return "No upcoming birthdays."
        return "Upcoming birthdays: " + ", ".join(f"{user['name']} ({user['congratulation_date']})" for user in upcoming_birthdays)

    def remove_phone(self, phone): #видалення
        for p in self.phones:
            if p.value == phone: #'123' != 123
                self.phones.remove(p)
                return
        raise ValueError
    
    def edit_phone(self, old_phone, new_phone): #зміна
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValueError

    def find_phone(self, phone): #пошук
        for p in self.phones:
            if p.value == phone:
                return p
        raise ValueError
    
    def __str__(self):
        return f'Record(Name: {self.name} Phones: {self.phones})'
    
    def __repr__(self):
        return f'Record(Name: {self.name} Phones: {self.phones})'

class AddressBook(UserDict): #Клас для зберігання та управління записами.
    def add_record(self, record: Record): #додавання
        name = record.name.value
        self.data.update({name: record}) # {'Hanna': Record('Hanna')}

    def find(self, name): #пошук
        return self.get(name) # Record('Hanna')
    
    def delete(self, name): #видалення
        del self[name]

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, contacts))

        elif command == "change":
            print(change_contact(args, contacts))

        elif command == "phone":
            print(phone)

        elif command == "all":
            print(show_all(contacts))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

vova = Record('Vova')
vova.add_phone('9999999991')

addressBook = AddressBook()
addressBook.add_record(vova)

hanna = Record('Hanna')
hanna.add_phone('8888888888')

addressBook.add_record(hanna)

print(addressBook.find('Vova'))
print(addressBook.find('Hanna'))
