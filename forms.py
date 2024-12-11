import re
from exceptions import InvalidFieldFormat
from abc import ABC

# Базовый абстрактный класс для всех типов полей.
class BaseField(ABC):
    display_name = ''
    pattern = ""

    def __init__(self, text):
        if not type(self).is_valid(text):
            raise InvalidFieldFormat
        self.value = text

    # Метод, проводящий проверку, соответствует ли форма определенному шаблону, заданному регулярными выражениями.
    @classmethod
    def is_valid(cls, value):
        return re.match(cls.pattern, str(value))


# Ниже перечислены все типы полей, указанные в ТЗ

class EmailField(BaseField):
    display_name = 'email'
    pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

class PhoneField(BaseField):
    display_name = 'phone'
    pattern = r"^\+7 \d{3} \d{3} \d{2} \d{2}$"

class DateField(BaseField):
    display_name = 'date'
    pattern = r"(\d{4})-(\d{2})-(\d{2})$"

    # Переопределенный метод is_valid, чтобы проводилась проврека допустимой даты
    @classmethod
    def is_valid(cls, value):
        match = re.match(DateField.pattern, str(value))
        if match:
            year, month, day = map(int, match.groups())
            if not ((year <= 0 ) or (month <= 0 or month > 12) or (day <= 0 or day > 31)):
                if month == 2:
                    if year%4 == 0 and day > 29:
                        return
                    elif year%4 != 0 and day > 28:
                        return
                elif month in (4, 6, 9, 10):
                    if day > 30:
                        return
                return True


FIELDS_LIST = [DateField, PhoneField, EmailField]

# Проверка, есть ли в пришедшей от пользователя форме все поля, которые прописаны в форме, взятой из базы данных.
def is_correct_form_containing(form, data):
    for key in list(form.keys())[1:]:
        if key not in data.keys():
            return
    return True


# Функци, принимающая на вход список всех форм, записанных в базе данных и находящая среди них те, которые соответствуют пришедшим данным формы.
def get_correct_form(forms, data):
    form_template = None
    for form in forms:
        if is_correct_form_containing(form, data):
            form_template = form
    return form_template

# Функция, прпнимающая на вход пришедшие данные формы и возвращаюая тип каждого поля.
def determine_types(data):
    determined_types = {}
    for key in data.keys():
        for FIELD in FIELDS_LIST:
            try:
                field = FIELD(data[key])
                determined_types[key] = field.display_name
                break
            except InvalidFieldFormat:
                determined_types[key] = 'text'
    return determined_types