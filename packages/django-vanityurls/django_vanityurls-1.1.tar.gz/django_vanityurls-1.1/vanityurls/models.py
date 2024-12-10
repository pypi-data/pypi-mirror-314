from django.db import models


class VanityUrl(models.Model):

    id = models.AutoField(primary_key=True)
    vanity_url = models.CharField(max_length=256,  default='', null=False, unique=True)
    target = models.CharField(max_length=512, default='', blank=False, null=False)

    class Meta:
        verbose_name = 'Vanity URL'
