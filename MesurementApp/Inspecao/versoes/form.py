from django import forms
from .models import Divisao, Inspection
from crispy_forms.helper import FormHelper


class Form_Divisao(forms.ModelForm):

    class Meta:
        model = Divisao
        fields = ('nome', 'freq47', 'freq862', 'freq950', 'freq2150')
        # labels = {'nome': 'Nome da divisão',
        #           'freq47': "47 MHz",
        #           'freq862': '862 MHz',
        #           'freq950': '950 MHz',
        #           'freq2150': '2150 MHz'}
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'freq47': forms.NumberInput(attrs={'class': 'narrow-select '}),
            'freq862': forms.NumberInput(attrs={'class': 'narrow-select '}),
            'freq950': forms.NumberInput(attrs={'class': 'narrow-select '}),
            'freq2150': forms.NumberInput(attrs={'class': 'narrow-select '})

        }
            # help_texts = {
        #     'nome': 'Nome dado à divisão a ser inspecionada',
        # }
        error_messages = {
            'nome': {
                'max_length': 'Nome da divisão tem mais caracteres que o permitido',
            },
        }

    # nome = models.CharField(max_length=30)
    # sec_id = models.ForeignKey(Seccao, on_delete=models.CASCADE)
    # freq47 = models.DecimalField(decimal_places=1, max_digits=20)
    # freq862 = models.DecimalField(decimal_places=1, max_digits=20)
    # freq950 = models.DecimalField(decimal_places=1, max_digits=20)
    # freq2150 = models.DecimalField(decimal_places=1, max_digits=20)

