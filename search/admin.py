from django.contrib import admin

from .models import TemporaryUser, UserSearch, UserSearchStage

admin.site.register(TemporaryUser)
admin.site.register(UserSearch)
admin.site.register(UserSearchStage)
