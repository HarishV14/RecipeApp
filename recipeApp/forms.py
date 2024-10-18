from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Recipe, RecipeIngredient, RecipeImage, RecipeCollection
from datetime import timedelta


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'title', 'servings', 'prepration_time', 'total_time',
            'calories', 'instructions', 'cuisine', 'food_type', 'difficulty','featured'
        )
        
    def clean(self):
        cleaned_data = super().clean()
        preparation_time = cleaned_data.get('prepration_time')
        total_time = cleaned_data.get('total_time')
        instructions = self.cleaned_data.get('instructions')
        
        if instructions:
            lines = instructions.splitlines()

            for line in lines:
                if line.strip() == "":
                    self.add_error('instructions', "Please do not leave any blank lines in the description.")
        
        if preparation_time is not None and total_time is not None:
            if not isinstance(preparation_time, timedelta) or not isinstance(total_time, timedelta):
                self.add_error('prepration_time', "Preparation time and total time must be valid durations.")
            elif preparation_time > total_time:
                self.add_error('prepration_time', "Preparation time must be less than or equal to total time.")

        self.validate_duration_format(preparation_time, "Preparation time")
        self.validate_duration_format(total_time, "Total time")

        return cleaned_data

    def validate_duration_format(self, duration, field_name):
        """Validate the duration format."""
        if duration:
            if isinstance(duration, timedelta):
                total_seconds = int(duration.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                duration_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            elif isinstance(duration, str):
                duration_str = duration
            else:
                self.add_error(field_name.lower().replace(" ", "_"), f"{field_name} must be a string formatted as HH:MM:SS.")
                return
    
            try:
                parts = list(map(int, duration_str.split(':')))
                if len(parts) > 3 or any(part < 0 for part in parts):
                    self.add_error(field_name.lower().replace(" ", "_"), f"{field_name} must be in format HH:MM:SS or less.")
                    return 
    
                if len(parts) == 3:
                    timedelta(hours=parts[0], minutes=parts[1], seconds=parts[2])
                elif len(parts) == 2:
                    timedelta(minutes=parts[0], seconds=parts[1])
                elif len(parts) == 1:
                    timedelta(seconds=parts[0])
            except ValueError:
                self.add_error(field_name.lower().replace(" ", "_"), f"{field_name} must be a valid duration (HH:MM:SS).")
            

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ('name', 'quantity', 'unit', 'optional')

RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    extra=1,
    can_delete=True  
)


class RecipeImageForm(forms.ModelForm):
    class Meta:
        model = RecipeImage
        fields = ('image', 'description')

RecipeImageFormSet = inlineformset_factory(
    Recipe,
    RecipeImage,
    form=RecipeImageForm,
    extra=1,
    can_delete=True  
)


class RecipeCollectionForm(forms.ModelForm):
    recipes = forms.ModelMultipleChoiceField(
        queryset=Recipe.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,  
        label='Select Recipes'  
    )

    class Meta:
        model = RecipeCollection
        fields = ['title', 'recipes']  