from django.contrib import admin

from .models import Category, Image, Link, Review, Workshop

admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Link)
admin.site.register(Review)
admin.site.register(Workshop)
