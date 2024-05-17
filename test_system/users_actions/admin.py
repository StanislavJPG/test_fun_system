from django.contrib import admin

from users_actions.models import User, Address

admin.site.register(User)
admin.site.register(Address)
