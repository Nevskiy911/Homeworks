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
        print(f"Command: {values}")


@input_error
def add(*args):
    phone_book[args[0]] = args[1]
    phones = args[1]
    name = args[0]
    if not phones:
        raise ValueError()
    return f"{name} phones: {phones} has added"


def show_all(*args):
    for k, v in phone_book.items():
        print(f"{k}: {v}")
    return hello()


@input_error
def phone(*args):
    for k, v in phone_book.items():
        if v in args:
            print(f"{k}: {v}")




def exit(*args):
    return "Good bye!"


def close(*args):
    return "Good bye!"


def good_bye(*args):
    return "Good bye!"


def no_command(*args):
    return "Unknown command, try again!"


COMMANDS = {help: "help",
            add: "add",
            exit: "exit",
            close: "close",
            good_bye: "good bye",
            show_all: "show all",
            phone: "phone",
            hello: "hello"}


def command_handler(text):
    for command, kword in COMMANDS.items():
        if text.startswith(kword):
            return command, text.replace(kword, "").strip()
    return no_command, None


def main():
    print(hello())
    while True:
        user_input = input(">>> ")
        command, data = command_handler(user_input)
        print(command(data))
        if command == exit or command == close or command == good_bye:
            break


if __name__ == "__main__":
    main()
