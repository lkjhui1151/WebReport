from django.db import models

# Create your models here.
class company(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = "Company"
        verbose_name_plural = "Company List"