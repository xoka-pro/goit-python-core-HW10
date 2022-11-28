from collections import UserDict


class AddressBook(UserDict):
    """
    Клас AddressBook, який успадковується від UserDict,
    та ми потім додамо логіку пошуку за записами до цього класу.

    * AddressBook реалізує метод add_record, який додає Record у self.data."""

    def add_record(self, record):
        self.data[record.name.value] = record


class Field:
    """Клас Field, який буде батьківським для всіх полів,
    у ньому потім реалізуємо логіку загальну для всіх полів"""
    pass


class Name(Field):
    """Клас Name, обов'язкове поле з ім'ям."""

    def __init__(self, value):
        self.value = value


class Phone(Field):
    """Клас Phone, необов'язкове поле з телефоном
    та таких один запис (Record) може містити кілька."""

    def __init__(self, phone):
        self.value = phone


class Record(Field):
    """Клас Record, який відповідає за логіку додавання/видалення/редагування
    необов'язкових полів та зберігання обов'язкового поля Name.

    * Записи Record у AddressBook зберігаються як значення у словнику.
    В якості ключів використовується значення Record.name.value.
    * Record зберігає об'єкт Name в окремому атрибуті.
    * Record зберігає список об'єктів Phone в окремому атрибуті.
    * Record реалізує методи для додавання/видалення/редагування об'єктів Phone."""

    def __init__(self, name, phone=None):
        self.name = Name(name)
        if phone:
            self.phones = [Phone(phone)]
        else:
            self.phones = []

    def add(self, phone):
        self.phones.append(Phone(phone))

    def change(self, old_phone, new_phone):
        for el in self.phones:
            if el.value == old_phone:
                el.value = new_phone

    def del_phone(self, phone):
        for elem in self.phones:
            if elem.value == phone:
                self.phones.remove(elem)


contacts = AddressBook()


def input_error(func):
    """ Errors handler """
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError as error:
            return f'No name in contacts. Error: {error}'
        except IndexError as error:
            return f'Sorry, not enough params for command. Error: {error}'
        except ValueError as error:
            return f'Give me name and phone, please. Error: {error}'
        except TypeError as error:
            return f'Not enough arguments. Error: {error}'
    return wrapper


def hello() -> str:
    return f'How can I help you?'


def goodbye():
    print(f'Good bye!')
    quit()


@input_error
def add(*args) -> str:
    """
    "add ...". За цією командою бот зберігає у пам'яті (у словнику, наприклад) новий контакт.
    Замість ... користувач вводить ім'я та номер телефону, обов'язково через пробіл.
    """

    name, number, *_ = args
    if name in contacts:
        return f'This contact already exist'
    contacts.update({name: number})
    return f'Contact add successfully'


@input_error
def change(*args) -> str:
    """
    "change ..." За цією командою бот зберігає в пам'яті новий номер телефону існуючого контакту.
    Замість ... користувач вводить ім'я та номер телефону, обов'язково через пробіл.
    """

    name, number, *_ = args
    if name in contacts:
        contacts.update({name: number})
    else:
        return f'No contact "{name}"'
    return f'Contact change successfully'


@input_error
def del_phone(name) -> str:

    if name in contacts:
        contacts.pop(name)
    else:
        return f'No contact "{name}"'
    return f'Contact deleted successfully'


@input_error
def phone_func(*args) -> str:
    """
    "phone ...." За цією командою бот виводить у консоль номер телефону для зазначеного контакту.
    Замість ... користувач вводить ім'я контакту, чий номер треба показати.
    """

    name = args[0]
    if contacts.get(name):
        return '\t{:>20} : {:<12} '.format(name, contacts.get(name))
    else:
        return f'No contact "{name}"'


@input_error
def show_all() -> str:
    """
    "show all". За цією командою бот виводить всі збереженні контакти з номерами телефонів у консоль.
    """

    result = []
    for name, numbers in contacts.items():
        result.append('\t{:>20} : {:<12} '.format(name, numbers))
    if len(result) < 1:
        return f'Contact list is empty'
    return '\n'.join(result)


def hlp(*args) -> str:
    return f'Known commands: hello, help, add, change, phone, show all, delete, good bye, close, exit.'


def parser(msg: str):
    """ Parser and handler AIO """
    command = None
    params = []

    operations = {
        'hello': hello,
        'h': hlp,
        'help': hlp,
        'add': add,
        'change': change,
        'phone': phone_func,
        'show all': show_all,
        'good bye': goodbye,
        'close': goodbye,
        'exit': goodbye,
        'delete': del_phone,
    }

    for key in operations:
        if msg.lower().startswith(key):
            command = operations[key]
            msg = msg.lstrip(key)
            for item in filter(lambda x: x != '', msg.split(' ')):
                params.append(item)
            return command, params
    return command, params


def main():
    """ Main function - all interaction with user """
    print(hello())
    while True:
        msg = input("Input command: ")
        command, params = parser(msg)
        if command:
            print(command(*params))
        else:
            print(f'Sorry, unknown command, try again. Type "h" for help.')


if __name__ == '__main__':
    main()
