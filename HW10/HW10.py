from collections import UserDict


class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []

    def add_num(self, phone):
        self.phones.append(phone)

    def change_num(self, position, phone):
        self.phones[position] = phone


class AddressBook(UserDict):
    def add_record(self, record):
        name = record.name.value
        self.data[name] = record


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
    return inner


def hello(*args):
    return """How can I help you?"""


@input_error
def help(*args):
    for key, values in COMMANDS.items():
        print(f"Command: {key}")
    return hello()


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
            "good bye": exit}


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
