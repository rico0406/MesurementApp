from django import forms
from .models import Divisao, Inspection
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Fieldset


class Form_Divisao(forms.ModelForm):

    class Meta:
        model = Divisao
        fields = ('nome', 'freq47', 'freq862', 'freq950', 'freq2150')
        labels = {'nome': 'Nome ',
                  'freq47': "47 MHz ",
                  'freq862': '862 MHz ',
                  'freq950': '950 MHz ',
                  'freq2150': '2150 MHz '}
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'freq47': forms.NumberInput(attrs={'class': 'narrow-select ',
                                               'onfocus': "if (this.value==0){ this.value = ''; }"}),
            'freq862': forms.NumberInput(
                attrs={'class': 'narrow-select ',
                       'onfocus': "if (this.value==0){ this.value = ''; }"}),
            'freq950': forms.NumberInput(
                attrs={'class': 'narrow-select ',
                       'onfocus': "if (this.value==0){ this.value = ''; }"}),
            'freq2150': forms.NumberInput(
                attrs={'class': 'narrow-select ',
                       'onfocus': "if (this.value==0){ this.value = ''; }"})
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
                    Div(
                        Div(
                            Field(
                                'nome',
                                css_class="form-control"
                            ),
                            css_class="col",
                        ),

                        Div(
                            Field(
                                'freq47',
                                css_class="form-control narrow-select ms-2"
                            ),
                            css_class="col"
                        ),

                        Div(
                            Field(
                                'freq862',
                                css_class="form-control narrow-select mx-1"
                            ),
                            css_class="col"
                         ),

                        Div(
                            Field(
                                'freq950',
                                css_class="form-control narrow-select ms-2"
                            ),
                            css_class="col"
                        ),
                        Div(
                            Field(
                                'freq2150',
                                css_class="form-control narrow-select mx-1"
                            ),
                            css_class="col"
                        ),

                        css_class="row"
                    )
        )


    def clean(self):
        cleaned_data = super().clean()
        for field_name in ['freq47', 'freq862', 'freq950', 'freq2150']:
            if cleaned_data.get(field_name) == None:
                cleaned_data[field_name] = 0.0
        return cleaned_data

# Layout option



 # self.helper.layout = Layout(
 #                    Div(
 #                        Field(
 #                            'nome',
 #                            css_class="form-control"
 #                        ),
 #                        css_class="row",
 #                    ),
 #                    Div(
 #                        Div(
 #                            Field(
 #                                'freq47',
 #                                css_class="form-control narrow-select ms-2"
 #                            ),
 #                            css_class="col"
 #                        ),
 #
 #                        Div(
 #                            Field(
 #                                'freq862',
 #                                css_class="form-control narrow-select mx-1"
 #                            ),
 #                            css_class="col"
 #                         ),
 #                        css_class="row",
 #                    ),
 #                    Div(
 #                        Div(
 #                            Field(
 #                                'freq950',
 #                                css_class="form-control narrow-select ms-2"
 #                            ),
 #                            css_class="col"
 #                        ),
 #                        Div(
 #                            Field(
 #                                'freq2150',
 #                                css_class="form-control narrow-select mx-1"
 #                            ),
 #                            css_class="col"
 #                        ),
 #                        css_class="row",
 #                    )
 #                )
