from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('Customers', 'Customer'),
        ('Distributors', 'Distributor'),
    ]

    email = forms.EmailField(required=True, label='Email')
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES, 
        label="User Type",
        widget=forms.Select(attrs={'class': 'user-type'})  # إضافة فئة مخصصة
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','user_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # تحقق من أن المجموعة موجودة قبل إضافة المستخدم
            user_type = self.cleaned_data['user_type']
            try:
                group = Group.objects.get(name=user_type)
                user.groups.add(group)
            except Group.DoesNotExist:
                raise forms.ValidationError(f"Group '{user_type}' does not exist.")
        return user
