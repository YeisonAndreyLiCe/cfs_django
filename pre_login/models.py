from django.db import models

class CookieManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if not postData['ip']:
            errors["ip"] = "Ip is required"
        if not postData['country']:
            errors["country"] = "Country is required"
        if not postData['city']:
            errors["city"] = "city is required"
        return errors

class Cookie(models.Model):
    ip = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CookieManager() # now User.validator() is a function that takes postData and returns errors