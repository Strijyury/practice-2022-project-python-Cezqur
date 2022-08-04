from typing import Final


class TransactionErrors:
    CATEGORY_NOT_ALLOWED: Final[str] = 'Для данного типа опреации нельзя выбрать категорию'
    CATEGORY_IS_REQUIRE: Final[str] = 'Для данного типа операции нужно выбрать категорию'

class TransactionCategoryErrors:
    ALREADY_EXISTS: Final[str] = 'У пользоваетля уже существует категория с таким названием и типом'
