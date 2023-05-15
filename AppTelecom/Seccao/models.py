# from django.db import models
# from django.contrib.auth.models import User
# from Inspecao.models import Inspection
#
# # Create your models here.
# class Seccao(models.Model):
#     nome = models.CharField(max_length=30)
#     inpec_id = models.ForeignKey(Inspection, on_delete=models.CASCADE)
#     data_insp = models.DateField()
#     data_sub = models.DateField(auto_now_add=True)
#     endereco = models.CharField(max_length=100)
#     cidade = models.CharField(max_length=30)
#     distrito = models.CharField(max_length=30)