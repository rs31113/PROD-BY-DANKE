from django.db import models
from django.utils import timezone


class Photo(models.Model):
    title = models.CharField("Подпись", max_length=255, blank=True)
    image = models.ImageField("Фотография", upload_to="gallery/")
    created_at = models.DateField(
        "Дата съёмки",
        default=timezone.localdate
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or f"Photo {self.id}"


__all__ = ()
