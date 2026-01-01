from django.db import models
from django.utils.text import slugify

# Create your models here.
class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    class Meta:
        abstract = True


from django.db import models
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('sale', 'Sale'),
        ('sold', 'Sold'),
    )

    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    slug = models.SlugField(unique=True, blank=True, null=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


    
class Tag(TimeStampModel):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name


class Post(TimeStampModel):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("in_active", "Inactive"),
    ]
    title = models.CharField(max_length= 200)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="post_image/%y/%m/%d", blank= False)
    author = models.ForeignKey("auth.User", on_delete= models.CASCADE)
    status = models.CharField(max_length = 20, choices = STATUS_CHOICES, default="active")
    views_count = models.PositiveBigIntegerField(default=0)
    published_at = models.DateTimeField(null = True, blank = True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    

# Event model
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_time = models.DateTimeField()
    background_image = models.ImageField(upload_to='events/backgrounds/')
    event_image = models.ImageField(upload_to='events/images/')
    # slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title
    

class Contact(TimeStampModel):
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name