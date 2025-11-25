import json
from typing import Dict, Any


class ClientShort:
    """Базовый класс с краткой информацией о клиенте"""

    def __init__(self, last_name: str, first_name: str, father_name: str, haircut_counter: int):
        self._validate_name(last_name, "last_name")
        self._validate_name(first_name, "first_name")
        self._validate_name(father_name, "father_name")
        self._validate_haircut_counter(haircut_counter)

        self.__last_name = last_name
        self.__first_name = first_name
        self.__father_name = father_name
        self.__haircut_counter = haircut_counter

    # Статические методы валидации
    @staticmethod
    def _validate_name(name, field_name):
        """Валидация имени, фамилии и отчества"""
        if not isinstance(name, str):
            raise ValueError(f"{field_name} должен быть строкой")
        if not name.strip():
            raise ValueError(f"{field_name} не может быть пустым")
        if len(name.strip()) < 2:
            raise ValueError(f"{field_name} должен содержать минимум 2 символа")
        if not name.replace(" ", "").isalpha():
            raise ValueError(f"{field_name} должен содержать только буквы и пробелы")

    @staticmethod
    def _validate_haircut_counter(haircut_counter):
        """Валидация количества стрижек"""
        if not isinstance(haircut_counter, int):
            raise ValueError("haircut_counter должен быть целым числом")
        if haircut_counter < 0:
            raise ValueError("haircut_counter не может быть отрицательным")

    # Геттеры как свойства, добавляем свойство property для обращения к полям без get
    @property
    def last_name(self) -> str:
        return self.__last_name

    @property
    def first_name(self) -> str:
        return self.__first_name

    @property
    def father_name(self) -> str:
        return self.__father_name

    @property
    def haircut_counter(self) -> int:
        return self.__haircut_counter

    def to_string(self) -> str:
        """Возвращает в формате 'Фамилия И.О., 1'"""
        return f"{self.__last_name.title()} {self.__first_name[0].upper()}.{self.__father_name[0].upper()}., {self.__haircut_counter}"

    # Строковые представления
    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return (f"ClientShort(last_name='{self.last_name}', first_name='{self.first_name}', "
                f"father_name='{self.father_name}', haircut_counter={self.haircut_counter})")

    # Методы сравнения
    def __eq__(self, other) -> bool:
        if not isinstance(other, ClientShort):
            return False
        return (self.last_name == other.last_name and
                self.first_name == other.first_name and
                self.father_name == other.father_name and
                self.haircut_counter == other.haircut_counter)


class Client(ClientShort):
    """Класс клиента с полной информацией, наследует от ClientShort"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            # Обработка единичного аргумента
            data = self._parse_single_arg(args[0])
            self._init_from_data(data)
        elif len(args) == 5:
            # Обычное создание
            self._init_from_data({
                'last_name': args[0],  # исправлен порядок
                'first_name': args[1],  # исправлен порядок
                'father_name': args[2],
                'haircut_counter': args[3],
                'discount': args[4]
            })
        elif kwargs:
            # Создание из именованных параметров
            self._init_from_data(kwargs)
        else:
            raise ValueError("Неверное количество аргументов")

    def _parse_single_arg(self, arg):
        """Обработка единичного аргумента"""
        if isinstance(arg, str):
            try:
                return json.loads(arg)
            except json.JSONDecodeError:
                raise ValueError("Некорректный JSON формат")
        elif isinstance(arg, dict):
            return arg
        else:
            raise ValueError("Не поддерживаемый тип аргумента")

    def _init_from_data(self, data: Dict[str, Any]):
        """Инициализация из данных"""
        # Проверка обязательных полей
        required_fields = ['first_name', 'last_name', 'father_name', 'haircut_counter', 'discount']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Отсутствуют обязательные поля: {missing_fields}")

        # Валидация скидки
        self._validate_discount(data['discount'])

        # Вызов конструктора родительского класса
        super().__init__(
            data['last_name'],
            data['first_name'],
            data['father_name'],
            data['haircut_counter']
        )

        self.__discount = data['discount']

    @staticmethod
    def _validate_discount(discount):
        """Валидация скидки"""
        if not isinstance(discount, (int, float)):
            raise ValueError("discount должен быть числом")
        if discount < 0 or discount > 100:
            raise ValueError("discount должен быть в диапазоне от 0 до 100")

    # Геттер для скидки
    @property
    def discount(self) -> int:
        return self.__discount

    # Сеттер для скидки
    @discount.setter
    def discount(self, value):
        self._validate_discount(value)
        self.__discount = value

    # Методы преобразования
    def to_string(self) -> str:
        """Возвращает строку в формате: 'Иващенко А.В., 5, 0'"""
        base_string = super().to_string()
        return f"{base_string}, {self.discount}"

    def to_short_version(self) -> ClientShort:
        """Создает краткую версию клиента (без скидки)"""
        return ClientShort(
            self.last_name,  # БЕЗ скобок - это свойство
            self.first_name,  # БЕЗ скобок - это свойство
            self.father_name,  # БЕЗ скобок - это свойство
            self.haircut_counter  # БЕЗ скобок - это свойство
        )

    # Строковые представления
    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return (f"Client(last_name='{self.last_name}', first_name='{self.first_name}', "
                f"father_name='{self.father_name}', haircut_counter={self.haircut_counter}, "
                f"discount={self.discount})")

    # Методы сравнения
    def __eq__(self, other) -> bool:
        if not isinstance(other, Client):
            return False
        return (super().__eq__(other) and self.discount == other.discount)

    # Статические фабричные методы
    @classmethod
    def from_json(cls, json_str: str) -> 'Client':
        """Создание клиента из JSON строки"""
        return cls(json_str)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Client':
        """Создание клиента из словаря"""
        return cls(data)


if __name__ == '__main__':
    print("Создание Client:")
    client1 = Client("Петров", "Петр", "Петрович", 10, 5)
    print(f"Client: {client1}")
    print(f"Repr: {repr(client1)}")
    print(f"Client: {str(client1)}")

    client2 = Client("Петров", "Петр", "Петрович", 10, 5)
    print(f"Скидка: {client1.discount}%")  # БЕЗ скобок - свойство

    print(client2.first_name)  # БЕЗ скобок - свойство
    print(f"")
    print(f"Создание ClientShort:")
    client_short = ClientShort("Иванов", "Иван", "Иванович", 5)
    print(f"ClientShort: {client_short}")
    print(f"Repr: {repr(client_short)}")
    print(f"Фамилия: {client_short.last_name}")  # БЕЗ скобок
    print(f"Имя: {client_short.first_name}")  # БЕЗ скобок
    print(f"Кол-во Стрижек: {client_short.haircut_counter}")  # БЕЗ скобок