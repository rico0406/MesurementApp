from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Inspection(models.Model):
    Ref_Relatorio = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=100)
    # Ref_Relatorio = models.IntegerField()
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # data_insp = models.DateField()
    data_sub = models.DateField(auto_now_add=True)
    # endereco = models.CharField(max_length=100)
    # cidade = models.CharField(max_length=30)
    # distrito = models.CharField(max_length=30)


class Seccao(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=20)
    nome = models.CharField(max_length=30)
    inspec = models.ForeignKey(Inspection, on_delete=models.CASCADE)

class Divisao(models.Model):
    nome = models.CharField(max_length=100, default='New Division')
    sec = models.ForeignKey(Seccao, on_delete=models.CASCADE)
    mesurement_point1 = models.DecimalField(decimal_places=1, max_digits=8, default=0.0, blank=False)
    mesurement_point2 = models.DecimalField(decimal_places=1, max_digits=8, default=0.0, blank=False)
    mesurement_point3 = models.DecimalField(decimal_places=1, max_digits=8, default=0.0, blank=False)
    mesurement_point4 = models.DecimalField(decimal_places=1, max_digits=8, default=0.0, blank=False)


