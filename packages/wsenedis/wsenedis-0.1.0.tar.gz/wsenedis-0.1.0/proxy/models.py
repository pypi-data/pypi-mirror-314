from django.db import models

class TraceActivite(models.Model):
    demandeur = models.CharField(max_length=50)
    RAE_concerne = models.CharField(max_length=20)
    service_concerne = models.CharField(max_length=100)
    horodate = models.DateTimeField(auto_now_add=True)