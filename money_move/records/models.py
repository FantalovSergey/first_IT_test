from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now


class Directory(models.Model):
    name = models.CharField(
        verbose_name='Наименование', max_length=32, unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class Status(Directory):

    class Meta(Directory.Meta):
        verbose_name = 'статус'
        verbose_name_plural = 'Статусы'


class Type(Directory):

    class Meta(Directory.Meta):
        verbose_name = 'тип'
        verbose_name_plural = 'Типы'


class Category(Directory):
    type = models.ForeignKey(
        Type, on_delete=models.CASCADE, verbose_name='Тип',
    )

    class Meta(Directory.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Subcategory(Directory):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Категория',
    )

    class Meta(Directory.Meta):
        verbose_name = 'подкатегория'
        verbose_name_plural = 'Подкатегории'


class Record(models.Model):
    created_at = models.DateField(
        verbose_name='Дата создания записи', blank=True, default=now,
    )
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, verbose_name='Статус',
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        verbose_name='Подкатегория',
        help_text='Доступен поиск по подкатегориям, категориям и типам.',
    )
    amount = models.PositiveBigIntegerField(
        verbose_name='Сумма',
        validators=[MinValueValidator(1)],
        help_text='Количество средств в рублях.',
    )
    comment = models.TextField(
        verbose_name='Комментарий', blank=True, null=True,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return (
            (
                f'{self.created_at}, {self.status}, '
                f'{self.subcategory.name}, {self.amount} ₽'
            ) + (', нажмите для просмотра комментария' if self.comment else '')
        )
