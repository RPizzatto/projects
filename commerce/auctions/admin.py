from django.contrib import admin

from .models import User, Acquisition, Listing, Watch_list

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Acquisition)
admin.site.register(Watch_list)