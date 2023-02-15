from collections import UserDict


class Field:
    pass


class Name(Field):
    def __init__(self, name):
        self.name = name


class Phone(Field):
    def __init__(self, phone):
        self.phone = phone


class Record:
    phones = []

    def __init__(self, name):
        self.name = name

    def change_phone(self, phone):
        self.phones = phone

    def del_phone(self, ind):
        self.phones.pop(ind)


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record[0]] = record


book = AddressBook({})


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except ValueError as val:
            print(f"{args[0][:-1]} is not a correct number")
        except KeyError as key:
            print(f"{args[0][1]} is not your contact or telephone is incorrect")
        except IndexError as ind:
            print("You entered an invalid command")

    return wrapper


@input_error
def hello_handler(*args):
    if len(args[0]) != 1:
        raise IndexError
    print("How can I help you?")


@input_error
def add_handler(*args):
    if len(args[0]) < 2:
        raise IndexError
    elif len(args[0]) > 2:
        name = Name(args[0][1])
        phone = []
        for i in range(len(args[0]) - 2):
            phone.append(Phone(args[0][i + 2]))
        record = Record(name)
        record.phones = phone
    else:
        name = Name(args[0][1])
        record = Record(name)
    book[record.name.name] = record


@input_error
def show_handler(*args):
    if len(args[0]) != 2:
        raise IndexError
    print("Your contacts")
    for val in book.data.values():
        print(f"{val.name.name}: {list(map(lambda x: x.phone, val.phones))}")


@input_error
def phone_handler(*args):
    if len(args[0]) != 2:
        raise IndexError
    if args[0][1] not in book.data.keys():
        raise KeyError
    else:
        phone_list = list(map(lambda x: x.phone, book.data[args[0][1]].phones))
        for i in phone_list:
            print(i)


@input_error
def change_handler(*args):
    if args[0][1] not in book.data.keys():
        raise KeyError
    else:
        new_phone = []
        for i in range(len(args[0]) - 2):
            new_phone.append(Phone(args[0][i + 2]))
        change_record = book.data[args[0][1]]
        change_record.change_phone(new_phone)
        book[change_record.name.name] = change_record


@input_error
def del_handler(*args):
    if args[0][1] not in book.data.keys():
        raise KeyError
    else:
        if args[0][2] in list(map(lambda x: x.phone, book.data[args[0][1]].phones)):
            phone_list = list(map(lambda x: x.phone, book.data[args[0][1]].phones))
            new_record = book.data[args[0][1]]
            new_record.del_phone(phone_list.index(args[0][2]))
            book[new_record.name.name] = new_record
        else:
            raise KeyError


@input_error
def exit_handler(*args):
    if len(args[0]) > 2:
        raise IndexError
    print("Good bye!")
    return "Good bye!"


COMMANDS = {
    "hello": hello_handler,
    "change": change_handler,
    "add": add_handler,
    "phone": phone_handler,
    "show": show_handler,
    "close": exit_handler,
    "exit": exit_handler,
    "good": exit_handler,
    "delete": del_handler,
}


def get_handler(handler):
    return COMMANDS[handler]


def main():
    print(
        """
Hello, I am assistant-bot. My commands: \n
hello
add ...
change ...
phone ...
delete ...
show all
close/exit/good bye 
"""
    )
    while True:
        handler = input("Введіть команду: ")
        command_list = handler.lower().split(" ")
        event_handler_list = handler.split(" ")
        if handler == ".":
            break
        event_handler = get_handler(command_list[0])
        end_flag = event_handler(event_handler_list)
        if end_flag == "Good bye!":
            break
        else:
            continue


if __name__ == "__main__":
    main()
