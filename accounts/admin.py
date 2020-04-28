from django.contrib import admin
from .models import Profile
from .models import Flight
from .models import Flightseat
# Register your models here.
admin.site.register(Profile)
admin.site.register(Flight)
admin.site.register(Flightseat)