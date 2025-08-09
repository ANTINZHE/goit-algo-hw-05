def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command"
        except KeyError:
            return "Contact not found."
    return inner

def parse_input(user_input):
    """ Функція розбиття введеного рядку """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    """ Функція додавання контакту """
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    """ Функція зміни контакту """
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    return "Contact not found."

@input_error
def show_phone(args, contacts):
    """ Функція відображення телефону """
    name = args[0] # Якщо не ввести args, то виведе помилку IndexError

    if name in contacts:
        return contacts[name]
    else:
        return "Contact not found."

@input_error
def show_all(contacts):
    """ Функція відображення усіх контактів """
    return contacts

def main():
    """ Головна функція """
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        # Використав match, так як це зрозуміліше ніж if elif else :)
        match command:
            case "close" | "exit":
                print("Good bye!")
                break
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(args, contacts))
            case "change":
                print(change_contact(args, contacts))
            case "phone":
                print(show_phone(args, contacts))
            case "all":
                print(show_all(contacts))
            case _:
                print("Invalid command.")

if __name__ == "__main__":
    main()