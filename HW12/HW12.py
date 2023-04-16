from collections import UserDict
from datetime import datetime
import pickle

class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    pass


class Birthday(Field):

    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return self.__value.strftime("%Y.%m.%d")
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, '%Y.%m.%d').date()
        except ValueError as e:
            return "The data format should be like this: <<< yyyy.mm.dd >>>"

    def __repr__(self) -> str:
        return self.__value.strftime('%Y.%m.%d')


class Record:

    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = [phone] if phone else []
        self.birthday = birthday

    def add_num(self, phone):
        self.phones.append(phone)

    def add_birth(self, value: Birthday):
        self.birthday = value

    def change_num(self, name, phone):
        self.phones.append(phone)

    def days_to_birthday(self):
        if self.birthday:
            birth = self.birthday.value
            result = birth.replace(year=datetime.now().year) - datetime.now().date()
            if result.days > 0:
                return f"To birthday {self.name} {result.days} days"
            return "Birthday has already passed"
        return "Birthday not set"


class AddressBook(UserDict):
    counter = 2

    def records(self, contact):
        self.counter = contact

    def __iter__(self):
        self.count = 0
        return self.data

    def __next__(self):
        if self.count > self.counter:
            raise StopIteration
        else:
            self.count += 1
            self.data

    def add_record(self, record):
        name = record.name.value
        self.data[name] = record

    def get_record_by_name(self, name):
        return self.data.get(name, None)
    

class CustomIterator:
    def __init__(self, counter=1):
        self.counter = counter

    def __iter__(self):
        return AddressBook(self)


phone_book = AddressBook()


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params. Try again"
        except KeyError:
            return "Not enough user name or phone number. Try again"
        except ValueError:
            return "Not enough user name or phone number. Try again"
        except TypeError:
            return "Incorrect data type"
        except AttributeError:
            return "Incorrect attribute"
    return inner


def hello(*args):
    return """How can I help you?"""


@input_error
def help(*args):
    for key, values in COMMANDS.items():
        print(f"Command: {key}")
    return hello()


@input_error
def add_birthday(*args):
    data = args[0].split()
    name = Name(data[0])
    birthday = Birthday(data[1])
    rec = phone_book.data.get(name.value)
    if rec:
        rec.add_birth(birthday)
        return f"{name.value} birthday has added with {birthday} day"
    return f"No contact wit name {name}"

@input_error
def add(*args):
    data = args[0].split()
    name = Name(data[0])
    phone = Phone(data[1])
    rec = Record(name)
    rec.add_num(phone)
    phone_book.add_record(rec)

    return f"{name.value} phones list has added with {phone.value} number"


@input_error
def change(*args):
    data = args[0].split()
    name = Name(data[0])
    phone = Phone(data[1])
    rec = phone_book[name.value]
    rec.change_num(name, phone)

    return f"{name} number has been changed for number: {phone}"


def show_all(*args):
    phones_lst = []
    if len(phone_book.data) == 0:
        return "There are no contacts in the phone book yet!"
    for k, v in phone_book.data.items():
        rec = phone_book.data[k]
        phones_lst.append(f"{k}: {', '.join(str(num) for num in rec.phones)}")
    return "\n".join([f"{item}" for item in phones_lst])


@input_error
def phone(*args):
    name = args[0]
    if name in phone_book.data:
        for k, v in phone_book.data.items():
            rec = phone_book.data[k]
            if name == k:
                return f"{k}: {', '.join(str(num) for num in rec.phones)}"
    raise KeyError


def birthday(*args):
    name = args[0]
    rec = phone_book.data.get(name)
    if rec:
        return rec.days_to_birthday()
    return f"No contact wit name {name}"

def exit(*args):
    return "Good bye!"


@input_error
def no_command(*args):
    return "Unknown command, try again!"


COMMANDS = {"help": help,
            "add": add,
            "new number": change,
            "show all": show_all,
            "phones": phone,
            "hello": hello,
            "exit": exit,
            "close": exit,
            "good bye": exit,
            "birthday": birthday,
            "birth": add_birthday}


def command_handler(text):
    for command, kword in COMMANDS.items():
        if text.startswith(command):
            return kword, text.replace(command, "").strip()
    return no_command, phone_book


def main():
    print(hello())
    while True:
        user_input = input(">>> ")
        command, data = command_handler(user_input)
        print(command(data))

        with open('data.bin', 'wb') as f:
            bytes = pickle.dump(phone_book, f)
            print(bytes)
        with open('data.bin', 'rb') as f:
            data = pickle.load(f)
            print(data)

        if user_input in ["exit", "close", "good bye"]:
            break

if __name__ == "__main__":
    main()
