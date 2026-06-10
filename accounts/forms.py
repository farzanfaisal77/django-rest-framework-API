from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CUCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model=CustomUser
        fields = UserCreationForm.Meta.fields + ("name",)
    
class CUChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model=CustomUser
        fields = UserChangeForm.Meta.fields 