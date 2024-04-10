from collections import UserDict
from datetime import datetime, timedelta


class Field: 
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
    

class Name(Field): 
    def __init__(self, name=None):
        if name is None:
            raise ValueError
        super().__init__(name)


class Phone(Field): 
    def __init__(self, phone): 
        if len(phone) != 10:
            raise ValueError
        super().__init__(phone)
        self.__phone = None
        self.phone = phone

class Birthday(Field):
    def __init__(self, value):
        try:
            super().__init__(value)
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
            
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        

class Record: 
    def __init__(self, name): 
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone): 
        for p in self.phones:
            if p.value == phone:
                return
        self.phones.append(Phone(phone))

    def remove_phone(self, phone): 
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError
    
    def edit_phone(self, old_phone, new_phone): 
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValueError

    def find_phone(self, phone): 
        for p in self.phones:
            if p.value == phone:
                return p
        raise ValueError
    
    #add birthday
    
    def __str__(self):
        return f'Record(Name: {self.name} Phones: {self.phones})'
    
    def __repr__(self):
        return f'Record(Name: {self.name} Phones: {self.phones})'


class AddressBook(UserDict): 
    def add_record(self, record: Record): 
        name = record.name.value
        self.data.update({name: record}) 

    def find(self, name): 
        return self.get(name) 
    
    def delete(self, name): 
        del self[name]

    def find_next_weekday(d, weekday: int):                                                 # Function for determining next 7 days
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return d + timedelta(days=days_ahead)

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
    
def input_error_phone(func):                                                                         # Creation decorator for contact functions
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:                                                                          # Processing of ValueError
            return "Wrong Input format! Please, enter Name and 10 digit format Phone Number"
        except KeyError:                                                                              # Processing of KeyError
            return "Record is missing."
        except IndexError:                                                                                # Processing of IndexError
            return "Please, Enter Name"
    return inner

def input_error_birthday(func):                                                                             # Creation decorator for birthday functions
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:                                                                          # Processing of ValueError
            return "Wrong Input format! Please, enter Name and use date format: DD.MM.YYYY."
    return inner
    
@input_error_phone
def parse_input(user_input):                                                                # Function for creating commands and arguments
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error_phone
def add_contact(args, book: AddressBook):                                                        # Function for adding contact to dict
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error_phone
def change_contact(args, book: AddressBook):                         # Function for changing existing contact
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        phone = record.find_phone(old_phone)
        if phone:
            record.edit_phone(old_phone, new_phone)
            message = "Phone number was changed."
        else:
            message = "Phone was not found."
            pass
    elif record is None:
        message = "Contact is missing."
    return message

@input_error_phone       
def show_phone(args, book: AddressBook):                             # Function for showing existing contact by username
    name, *_ = args
    record = book.find(name)
    if record:
        return record.phones
    else:
        return "Contact is missing."

@input_error_birthday
def add_birthday(args, book: AddressBook):                          # Function for adding birthday for contact 
    name, birthday, *_ = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday was added."
    else:
        return "Contact is mising."
    
@input_error_phone
def show_birthday(args, book: AddressBook):                     # Function for showing contact's birthday
    name, *_ = args
    record = book.find(name)
    if record:
        return record.birthday
    else:
        return "Contact is missing"
    
def birthdays(book: AddressBook):                               # Function for showing upcoming birthdays taht will be next week
    return book.get_upcoming_birthdays()

def main():                                                 # main function for output result
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
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(book)
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
