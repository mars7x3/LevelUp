from django.db import models


class UserStatus(models.IntegerChoices):
    STAFF = 1, 'СОТРУДНИК'
    CLIENT = 2, 'КЛИЕНТ'
    ADMIN = 777, 'АДМИН САЙТА'


class StaffRole(models.IntegerChoices):
    DIRECTOR = 1, 'ДИРЕКТОР'
    RECEIVER = 2, 'ПРИЕМЩИК'
    OTK = 3, 'ОТК'
    PACKER = 4, 'УПАКОВЩИК'
    MARKER = 5, 'МАРКЕРОВЩИК'
    CONTROLLER = 6, 'ГРУППИРОЩИК'


class ProductStatus(models.IntegerChoices):
    RECEIVER = 1, 'ПРИЕМЩИК'
    OTK = 2, 'ОТК'
    PACKER = 3, 'УПАКОВЩИК'
    MARKER = 4, 'МАРКЕРОВЩИК'
    CONTROLLER = 5, 'ГРУППИРОВЩИК'
    DEFECT = 6, 'БРАК'


class CodeType(models.IntegerChoices):
    INTERNAL = 1, 'ВНУТРЕННИЙ'
    HS = 2, 'ЧЕСТНЫЙ ЗНАК'
    WB = 3, 'WILDBERRIES'


class OrderStatus(models.IntegerChoices):
    NEW = 1, 'НОВЫЙ'
    PROGRES = 2, 'В ПРОЦЕССЕ'
    DONE = 3, 'ГОТОВО'