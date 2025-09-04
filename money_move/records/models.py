from django.core.validators import MinValueValidator
from django.db import models


class Directory(models.Model):
    name = models.CharField(
        verbose_name='Наименование', max_length=32, unique=True,
    )

    class Meta:
        abstract = True
        db_table_comment = (
            'Будьте внимательны! Удаление наименования приведёт '
            'к удалению всех записей о ДДС, включающих данное наименование. '
            'Внесите необходимые корректировки до удаления.'
        )
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class Status(Directory):

    class Meta(Directory.Meta):
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Type(Directory):

    class Meta(Directory.Meta):
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Category(Directory):
    type = models.ForeignKey(
        Type, on_delete=models.CASCADE, verbose_name='Тип',
    )

    class Meta(Directory.Meta):
        ordering = ('type', 'name')
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.type}, {self.name}'


class Subcategory(Directory):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Категория',
    )

    class Meta(Directory.Meta):
        ordering = ('category', 'name')
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return f'{self.category}, {self.name}'


class Record(models.Model):
    created_at = models.DateField(
        verbose_name='Дата создания записи', auto_now_add=True,
    )
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, verbose_name='Статус',
    )
    type = models.ForeignKey(
        Type, on_delete=models.CASCADE, verbose_name='Тип',
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Категория',
    )
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, verbose_name='Подкатегория',
    )
    amount = models.PositiveBigIntegerField(
        verbose_name='Сумма',
        validators=[MinValueValidator(1)],
        help_text='Количество средств в рублях',
    )
    comment = models.TextField(blank=True, null=True)

    class Meta:
        db_table_comment = (
            'Полужирным шрифтом отмечены поля, обязательные для заполнения, '
            'обычным шрифтом – необязательные.'
        )
        default_related_name = 'records'
        ordering = ('-created_at',)
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return (
            (
                f'{self.created_at}, {self.status}, '
                f'{self.subcategory.name}, {self.amount}'
            ) + (', нажмите для просмотра комментария' if self.comment else '')
        )
