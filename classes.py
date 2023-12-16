from collections import UserDict
from collections import defaultdict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            self.invalid = True
            self.value = value
        else:
            self.invalid = False
            super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            day, month, year = map(int, value.split("."))
            if day < 1 or day > 31 or month < 1 or month > 12:
                raise ValueError("Invalid date format")
            self.value = datetime(year, month, day).date()
        except (ValueError, TypeError):
            raise ValueError("Invalid date format")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def remove_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                self.phones.remove(phone_obj)
                break

    def edit_phone(self, old_phone, new_phone):
        for phone_obj in self.phones:
            if phone_obj.value == old_phone:
                phone_obj.value = new_phone
                break

    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj.value
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = "; ".join(str(phone) for phone in self.phones)
        birthday_str = str(self.birthday) if self.birthday else "N/A"
        return (
            f"Contact name: {self.name}, phones: {phones_str}, birthday: {birthday_str}"
        )


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        birthday_dict = defaultdict(list)
        today = datetime.today().date()

        for record in self.data.values():
            name = record.name.value
            if record.birthday:
                birthday = record.birthday.value
                try:
                    birthday = datetime.strptime(birthday, "%d.%m.%Y").date()
                except ValueError:
                    continue

                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days

                if delta_days < 7:
                    birthday_date = today + timedelta(days=delta_days)

                    if birthday_date.weekday() >= 5:
                        birthday_date += timedelta(days=(7 - birthday_date.weekday()))
                    weekday = birthday_date.strftime("%A")
                    birthday_dict[weekday].append(name)

        sorted_days = list(birthday_dict.keys())
        sorted_days.sort(
            key=lambda x: (
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ).index(x)
        )

        result = {}
        for day in sorted_days:
            names = birthday_dict[day]
            result[day] = names

        return result
