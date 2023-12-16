
from collections import UserDict
from classes import AddressBook, Record
from classes import Field, Name, Phone, Birthday


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return 'Name is not in contacts. Give me user name please'
        except ValueError:
            return 'Give me name and phone please'
        except IndexError:
            return 'Contact not found  Give me name and phone please'
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


@input_error
def add_contact(args, book):
    name, phone = args
    phone_field = Phone(phone)

    if phone_field.invalid:
        return "Phone number must be 10 digits"

    if book.find(name):
        record = book.find(name)
        record.add_phone(phone)
    else:
        new_record = Record(name)
        new_record.add_phone(phone)
        book.add_record(new_record)
    return "Contact added."


@input_error
def change_contact(args, book):
    name, phone = args

    if book.find(name):
        phone_field = Phone(phone)

        if phone_field.invalid:
            return "Phone number must be 10 digits."

        record = book.find(name)
        record.edit_phone(record.phones[0].value, phone_field.value)
        return "Contact updated."
    else:
        return f"{name} not found."


@input_error
def get_contact_phone(args, book):

    name = args[0]
    record = book.find(name)
    if record:
        phone = record.phones[0].value
        return phone if phone else f"Phone number for '{name}' not found."
    else:
        return f"{name} not found."


@input_error
def show_all(contacts):
    if len(contacts) == 0:
        return "No contacts."
    res = ""
    for k,v in contacts.items():
        res = res + f"Contact {k} {v}."
    return res


@input_error
def add_birthday(args, book):
    name, birthday = args
    if book.find(name):
        try:
            record = book.find(name)
            record.add_birthday(birthday)
            return "Birthday added."
        except ValueError:
            return "Invalid date format. Please use DD.MM.YYYY "
    else:
        return f"{name} not found."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return str(record.birthday) if record.birthday else "N/A"
    else:
        return f"Contact '{name}' not found."


@input_error
def birthdays(book):
    birthday_data = book.get_birthdays_per_week()
    if not birthday_data:
        return "No  birthdays  on next week."

    result = "Birthdays next week:\n"
    for day, names in birthday_data.items():
        result += f"{day}: {', '.join(names)}\n"

    return result


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
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
            print(get_contact_phone(args, book))
        elif command == "all":
            print(show_all(book))
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
