from django.forms import Form,CharField,IntegerField,Textarea,EmailField,ImageField,FileField


class RegisterForm(Form):
    username = CharField(max_length=20, required=True)
    email = EmailField(required= True)
    password = CharField(min_length=6, required=True)
    password2 = CharField(min_length=6, required=True)

