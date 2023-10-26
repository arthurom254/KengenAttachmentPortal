
from django.contrib.auth.models import User
import random
def getUserName(name):
    name=name.lower()
    if User.objects.filter(username=name).exists():
        username=f"{name}{random.randint(1,1000)}"
    else:
        username=name
    return username
