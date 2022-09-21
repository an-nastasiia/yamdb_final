from django.db import models


class PubDateModel(models.Model):
    """Abstract model with pub date."""

    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
