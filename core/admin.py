from django.contrib import admin
from .models import *

admin.site.register(Comment)
admin.site.register(Story)
admin.site.register(Category)
# Register your models here.
admin.site.register(Event)
admin.site.register(EventRegistration)
