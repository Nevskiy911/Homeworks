phone_book = {"fireprotection": "101",
              "police": "102",
              "medicall": "103"}


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
        print (f"Command: {key}")
    return hello()

@input_error
def add(*args):
    data = args[0].split(" ")
    name = data[0].strip()
    phone = data[1].strip()
    phone_book[name] = phone
    return f"{name} phones: {phone} has added"

@input_error
def change(*args):
    data = args[0].split(" ")
    name = data[0].strip()
    num = data[1].strip()
    if name in phone_book.keys():
        phone_book[name] = num
    return f"{name} number has been changed for number: {num}"

def show_all(*args):
    for k, v in phone_book.items():
        print(f"{k}: {v}")
    return hello()

@input_error
def phone(*args):
    for k, v in phone_book.items():
        if v in args:
            return f"{k}: {v}"

def exit(*args):
    return "Good bye!"

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
    return no_command, None

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
