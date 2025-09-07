from django.db import models

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=100, null=True, blank=True)  # New field
    city = models.CharField(max_length=100, null=True, blank=True)     # New field

    def __str__(self):
        return f"{self.ip_address} accessed {self.path} at {self.timestamp}"

# Model for blocking IPs
class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return self.ip_address