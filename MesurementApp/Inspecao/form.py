from django import forms
from .models import Divisao, Inspection
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Fieldset


FOCUS_COLOR = "this.style.boxShadow = '0 0 5px #ea32b3'; "
ONFOCUS_SCRIPT = f"{FOCUS_COLOR}if (this.value==0){{ this.value = ''; }}"
class Form_Divisao(forms.ModelForm):

    class Meta:
        model = Divisao
        fields = ('nome', 'mesurement_point1', 'mesurement_point2', 'mesurement_point3', 'mesurement_point4')
        labels = {'nome': 'Name ',
                  'mesurement_point1': "Point 1 ",
                  'mesurement_point2': 'Point 2 ',
                  'mesurement_point3': 'Point 3 ',
                  'mesurement_point4': 'Point 4 '}
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control',
                                           'onfocus': FOCUS_COLOR}),
            'mesurement_point1': forms.NumberInput(attrs={'class': 'narrow-select ',
                                                          'onfocus': ONFOCUS_SCRIPT,
                                                          'onblur': "this.style.boxShadow = 'none';"}),
            'mesurement_point2': forms.NumberInput(
                attrs={'class': 'narrow-select ',
                       'onfocus': ONFOCUS_SCRIPT}),
            'mesurement_point3': forms.NumberInput(
                attrs={'class': 'narrow-select ',
                       'onfocus': ONFOCUS_SCRIPT}),
            'mesurement_point4': forms.NumberInput(
                attrs={'class': 'narrow-select ',
                       'onfocus': ONFOCUS_SCRIPT})
        }

        # help_texts = {
        #     'nome': 'Name dado à divisão a ser inspecionada',
        # }
        error_messages = {
            'nome': {
                'max_length': 'Division name exceeded the character limit',
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
                                'mesurement_point1',
                                css_class="form-control narrow-select ms-2"
                            ),
                            css_class="col"
                        ),

                        Div(
                            Field(
                                'mesurement_point2',
                                css_class="form-control narrow-select mx-1"
                            ),
                            css_class="col"
                         ),

                        Div(
                            Field(
                                'mesurement_point3',
                                css_class="form-control narrow-select ms-2"
                            ),
                            css_class="col"
                        ),
                        Div(
                            Field(
                                'mesurement_point4',
                                css_class="form-control narrow-select mx-1"
                            ),
                            css_class="col"
                        ),

                        css_class="row"
                    )
        )


    def clean(self):
        cleaned_data = super().clean()
        for field_name in ['mesurement_point1', 'mesurement_point2', 'mesurement_point3', 'mesurement_point4']:
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
