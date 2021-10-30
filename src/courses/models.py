from django.db import models
from django.contrib.auth import get_user_model
from common.models import BaseModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField

User = get_user_model()


class Subject(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']
        db_table = 'subjects'

    def __str__(self):
        return self.title


class Course(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_created')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()

    class Meta:
        db_table = 'courses'
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        db_table = 'modules'
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'


class Content(BaseModel):
    """
    Create a Content model that represents the modules' contents,
    and define a generic relation to associate any kind of content
    
    Only the content_type and object_id fields have a corresponding column in the
    database table of this model. The item field allows you to retrieve or set the related
    object directly, and its functionality is built on top of the other two fields.
    """
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, 
        on_delete=models.CASCADE, 
        limit_choices_to={'model__in': ('text', 'video', 'image', 'file')
    })
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_related')
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.ImageField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()

