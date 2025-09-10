from django.db import models


class LinkCategory(models.Model):
    name = models.CharField("Category name", max_length=100, unique=True)
    slug = models.SlugField("slug", max_length=100, unique=True, blank=True)
    order = models.PositiveIntegerField("Order", default=0)

    class Meta:
        verbose_name = "Link category"
        verbose_name_plural = "Link categories"
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class Link(models.Model):
    category = models.ForeignKey(
        LinkCategory,
        related_name="links",
        on_delete=models.CASCADE,
        verbose_name="Category",
    )
    label = models.CharField("name", max_length=50)
    url = models.URLField("URL")
    order = models.PositiveIntegerField("order", default=0)
    is_active = models.BooleanField("show", default=True)

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.label} → {self.url}"


__all__ = ()
