from django import forms
from django.contrib.auth.models import User

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)
    nickname = forms.CharField(label='Никнейм', max_length=150)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data.get('password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class QuestionForm(forms.Form):
    title = forms.CharField(
        label='Вопрос',
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например, Как работает шаблонизация Django?'})
    )
    text = forms.CharField(
        label='Подробное описание',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Опишите, что вы пробовали, и что не работает...'})
    )
    tags = forms.CharField(
        label='Теги',
        max_length=100,
        help_text='Укажите 1–5 тегов через пробел. Например: python django orm',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: python django orm'})
    )

class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

class ProfileSettingsForm(forms.Form):
    nickname = forms.CharField(label='Никнейм', max_length=150)
    email = forms.EmailField(label='Почта')
    avatar = forms.ImageField(label='Аватар', required=False)
    password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput, required=False)
    password_confirm = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput, required=False)

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password_confirm')
        if p1 and p1 != p2:
            self.add_error('password_confirm', 'Пароли не совпадают')

