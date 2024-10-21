from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, RecipeIngredient, RecipeImage, RecipeCollection
from datetime import timedelta


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'title', 'servings', 'prepration_time', 'total_time',
            'calories', 'instructions', 'cuisine', 'food_type', 'difficulty','featured'
        )
        
    def clean_instructions(self):
        instructions = self.cleaned_data.get('instructions')

        if instructions:
            lines = instructions.splitlines()
            
            for line in lines:
                if line.strip() == "":
                    raise forms.ValidationError("Please do not leave any blank lines in the description.")
        
        return instructions
        
    def clean(self):
        cleaned_data = super().clean()
        preparation_time = cleaned_data.get('prepration_time')
        total_time = cleaned_data.get('total_time')
        
        if preparation_time is not None and total_time is not None:
            if not isinstance(preparation_time, timedelta) or not isinstance(total_time, timedelta):
                self.add_error('prepration_time', "Preparation time and total time must be valid durations.")
            elif preparation_time > total_time:
                self.add_error('prepration_time', "Preparation time must be less than or equal to total time.")

        return cleaned_data
          

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