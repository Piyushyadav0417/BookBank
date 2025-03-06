from django.contrib import admin
from .models import BooksCategories, Books, Likes, Comments, UserProfile, PasswordReset
# Register your models here.
admin.site.register(BooksCategories)
admin.site.register(Books)
admin.site.register(Likes)
admin.site.register(Comments)
admin.site.register(UserProfile)
admin.site.register(PasswordReset)