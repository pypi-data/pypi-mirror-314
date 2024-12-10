from django import forms


class SignInForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    code = forms.CharField(label='2FA Code', required=False)


class ProcessMagicLinkForm(forms.Form):
    token = forms.CharField(label='Token', required=True)
    code = forms.CharField(label='2FA Code', required=False)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email')


class ProcessForgotPasswordForm(forms.Form):
    token = forms.CharField(label='Token', required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data
