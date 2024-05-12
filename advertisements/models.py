from django.conf import settings
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class Advertisement(models.Model):
    """Объявление."""

    title = models.TextField(verbose_name="Статья")
    description = models.TextField(default='', verbose_name="Текст статьи")
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN,
        verbose_name="Статус",
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор статьи",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата изменения",
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title
