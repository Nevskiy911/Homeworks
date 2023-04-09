from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    pass


class Birthday:
    def __init__(self, birthday):
        self.__birthday = None
        self.birthday = birthday

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday):
        try:
            self.__birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
        except ValueError as e:
            return "The data format should be like this: <<< dd.mm.yy >>>"

    def __repr__(self) -> str:
        return self.birthday.strftime('%Y-%m-%d')



class Record:
    def __init__(self, name, birthday: Birthday = None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        self.birthdays = []

    def add_num(self, phone):
        self.phones.append(phone)

    def add_birth(self, birth: Birthday):
        self.birthdays.append(birth) 

    def change_num(self, position, phone):
        self.phones[position] = phone

    def days_to_birthday(self):
        if self.birthday:
            birth = self.birthday.birthday
            result = datetime(datetime.now().year, birth.month, birth.day) - datetime.now()
            if result.days > 0:
                return result.days
            return "Birthday has already passed"
        return "Birthday not found"


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
    rec = Record(name)
    rec.add_birth(birthday)
    phone_book.add_record(rec)

    return f"{name.value} birthday has added with {birthday} day"

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
    rec.change_num(0, phone)

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
    rec = phone_book.data.get(args[0])
    if rec:
        return rec.days_to_birthday()
    return f'There is no contacts in the phonebook with name {args[0]}'


def exit(*args):
    return "Good bye!"


@input_error
def no_command(*args):
    return "Unknown command, try again!"


COMMANDS = {"help": help,
            "add": add,
            "change": change,
            "show all": show_all,
            "phone": phone,
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
        if user_input in ["exit", "close", "good bye"]:
            break


if __name__ == "__main__":
    main()
