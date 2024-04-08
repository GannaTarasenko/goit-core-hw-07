from collections import UserDict

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


class Record: #Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
    def __init__(self, name): # record = Record('Hanna')
        self.name = Name(name)
        self.phones = list()

    def add_phone(self, phone): #додавання
        for p in self.phones:
            if p.value == phone: #'123' != 123
                return
        self.phones.append(Phone(phone))

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
      
vova = Record('Vova')
vova.add_phone('9999999991')

addressBook = AddressBook()
addressBook.add_record(vova)

hanna = Record('Hanna')
hanna.add_phone('8888888888')

addressBook.add_record(hanna)

print(addressBook.find('Vova'))
print(addressBook.find('Hanna'))
