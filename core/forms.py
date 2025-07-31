from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Region, Categorie, Contact


class CustomUserCreationForm(UserCreationForm):
    """Formulaire personnalisé de création d'utilisateur"""
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input w-full',
            'placeholder': 'Votre prénom'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input w-full',
            'placeholder': 'Votre nom'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'input w-full',
            'placeholder': 'votre.email@exemple.com'
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input w-full',
            'placeholder': 'Nom d\'utilisateur'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input w-full',
            'placeholder': 'Mot de passe'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input w-full',
            'placeholder': 'Confirmer le mot de passe'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        """Vérifier que l'email n'existe pas déjà"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un compte avec cet email existe déjà.")
        return email

    def save(self, commit=True):
        """Sauvegarder l'utilisateur avec les informations supplémentaires"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """Formulaire pour le profil utilisateur"""
    
    class Meta:
        model = UserProfile
        fields = ['telephone', 'region', 'niveau_etudes', 'domaines_interet', 'date_naissance', 'bio']
        widgets = {
            'telephone': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': '+224 XX XX XX XX'
            }),
            'region': forms.Select(attrs={
                'class': 'input w-full'
            }),
            'niveau_etudes': forms.Select(attrs={
                'class': 'input w-full'
            }),
            'domaines_interet': forms.CheckboxSelectMultiple(),
            'date_naissance': forms.DateInput(attrs={
                'class': 'input w-full',
                'type': 'date'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'input w-full',
                'rows': 4,
                'placeholder': 'Parlez-nous de vous...'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['region'].queryset = Region.objects.all()
        self.fields['region'].empty_label = "Sélectionnez une région"
        self.fields['domaines_interet'].queryset = Categorie.objects.all()


class CustomAuthenticationForm(forms.Form):
    """Formulaire de connexion personnalisé"""
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'input w-full',
            'placeholder': 'Email ou nom d\'utilisateur'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input w-full',
            'placeholder': 'Mot de passe'
        })
    )


class ContactForm(forms.ModelForm):
    """Formulaire de contact utilisant ModelForm"""
    
    class Meta:
        model = Contact
        fields = ['nom', 'email', 'telephone', 'sujet', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Votre nom complet'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input w-full',
                'placeholder': 'votre.email@exemple.com'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': '+224 XX XX XX XX (optionnel)'
            }),
            'sujet': forms.Select(attrs={
                'class': 'input w-full'
            }),
            'message': forms.Textarea(attrs={
                'class': 'input w-full',
                'rows': 5,
                'placeholder': 'Décrivez votre question ou problème...'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre tous les champs requis sauf téléphone
        for field_name, field in self.fields.items():
            if field_name != 'telephone':
                field.required = True