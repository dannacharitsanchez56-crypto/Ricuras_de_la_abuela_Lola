from django import forms
from .models import OpcionesAlmuerzo

PROTEINAS = [
    ('Pollo', 'Pollo'),
    ('Carne de res', 'Carne de res'),
    ('Carne de cerdo', 'Carne de cerdo'),
]



PRINCIPIOS = [
    ('Frijoles', 'Frijoles'),
    ('Lentejas', 'Lentejas'),
    ('Sin principio', 'Sin principio'),
]


ACOMPANAMIENTOS = [
    ('Patacones', 'Patacones'),
    ('Papa', 'Papa'),
    ('Yuca', 'Yuca'),
    ('Arroz adicional', 'Arroz adicional'),
]


class OpcionesAlmuerzoForm(forms.ModelForm):

    proteinas = forms.MultipleChoiceField(
        label='Proteínas',
        choices=PROTEINAS,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    principios = forms.MultipleChoiceField(
        label='Principios',
        choices=PRINCIPIOS,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    acompanamientos = forms.MultipleChoiceField(
        label='Acompañamientos',
        choices=ACOMPANAMIENTOS,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = OpcionesAlmuerzo
        fields = [
            'proteinas',
            'principios',
            'acompanamientos'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['proteinas'].initial = (
                self.instance.proteinas or []
            )
            self.fields['principios'].initial = (
                self.instance.principios or []
            )
            self.fields['acompanamientos'].initial = (
                self.instance.acompanamientos or []
            )


class ElegirAlmuerzoForm(forms.Form):

    proteina = forms.ChoiceField(
        label='Proteína',
        widget=forms.RadioSelect
    )

    principio = forms.ChoiceField(
        label='Principio',
        widget=forms.RadioSelect
    )

    acompanamiento = forms.ChoiceField(
        label='Acompañamiento',
        widget=forms.RadioSelect
    )

    def __init__(self, *args, configuracion, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['proteina'].choices = [
            (valor, valor)
            for valor in configuracion.proteinas
        ]

        self.fields['principio'].choices = [
            (valor, valor)
            for valor in configuracion.principios
        ]

        self.fields['acompanamiento'].choices = [
            (valor, valor)
            for valor in configuracion.acompanamientos
        ]