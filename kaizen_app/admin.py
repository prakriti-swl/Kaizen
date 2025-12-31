from django.contrib import admin
from .models import Post, Category, Tag, Event, Contact, Product
# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Event)
admin.site.register(Contact)
admin.site.register(Product)