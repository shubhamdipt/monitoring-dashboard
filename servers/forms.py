from django.forms import ModelForm, ValidationError
from servers.models import Alarm, DATA_TYPES


class AlarmForm(ModelForm):
    """Form validation for Alarm model"""

    class Meta:
        model = Alarm
        fields = ['data_type', 'comparison_type', 'comparison_value', ]

    def clean(self):
        cleaned_data = super().clean()
        data_type = cleaned_data.get("data_type")
        comparison_type = cleaned_data.get("comparison_type")
        comparison_value = cleaned_data.get("comparison_value")

        if data_type == DATA_TYPES["DOWNTIME"]:
            if comparison_type == Alarm.LESS_THAN:
                raise ValidationError(
                    "For DOWNTIME, comparison must be Greater Than (>)"
                )
        if comparison_value <= 0:
            raise ValidationError(
                "Value must be greater than 0."
            )