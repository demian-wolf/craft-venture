from django.contrib import admin

from .models import UserSearch, TemporaryUser, SearchFeedback


admin.site.register(UserSearch)
admin.site.register(TemporaryUser)
admin.site.register(SearchFeedback)
