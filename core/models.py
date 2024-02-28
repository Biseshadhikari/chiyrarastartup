from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify
import uuid



# Create your models here.

class Category(models.Model): 
    text = models.CharField(max_length = 200)

    def __str__(self): 
        return self.text
class Story(models.Model):
    category = models.ForeignKey(Category,on_delete = models.CASCADE,null = True,blank = True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null = True,blank=True)
    title = models.CharField(max_length= 200)
    thumbnail = models.ImageField(upload_to='img', null = True,blank = True)
    body  = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add = True)
    slug= models.SlugField(unique = True,null = True,blank = True)
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.title)}-{str(uuid.uuid4())}"
            super().save(*args, **kwargs)   
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length = 200, null = True, blank  = True)
    created_at = models.DateTimeField(auto_now_add=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE,null = True ,blank = True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    
    def get_child_comments(self): 
        return Comment.objects.filter(parent_comment = self)


class Event(models.Model):
    title = models.CharField(max_length=255)
    img = models.ImageField(upload_to='even/img',null = True, blank = True)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    is_past_event = models.BooleanField(default=False)
    map_iframe = models.CharField(max_length=400,blank=True,null=True)


    def __str__(self):
        return self.title
    

class EventRegistration(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    contact = models.CharField(max_length=15)
    address = models.TextField()
    institution = models.CharField(max_length=255,null = True)
    event = models.ForeignKey(Event,on_delete = models.CASCADE)

    def __str__(self):
        return self.name