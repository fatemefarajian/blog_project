from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django_jalali.db import models as jmodels
from django.template.defaultfilters import slugify
from django_resized import ResizedImageField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        REJECTED = 'RJ', 'Rejected'



    CATEGORY_CHOICES = (
        ('تکنولوژی', 'تکنولوی'),
        ('زبان برنامه نویسی', 'زبان برنامه نویسی'),
        ('هوش مصنوعی', 'هوش مصنوعی'),
        ('بلاکچین', 'بلاکچین'),
        ('سایر', 'سایر'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts', verbose_name='نویسنده')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    slug = models.SlugField(max_length=200, unique=True)
    # date
    publish = jmodels.jDateTimeField(default=timezone.now, verbose_name="تاریخ انتشار")
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)

    # choice fields
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name="وضعیت")
    reading_time = models.PositiveIntegerField(verbose_name="زمان مطالعه")
    category = models.CharField(verbose_name="دسته بندی", max_length=20, choices=CATEGORY_CHOICES, default='سایر')

    # objects = models.Manager()
    objects = jmodels.jManager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['publish'])]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for img in self.images.all():
            storage, path = img.image_file.storage, img.image_file.path
            storage.delete(path)
        super().delete(*args, **kwargs)


class Ticket(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(max_length=11, verbose_name='تلفن')
    message = models.TextField(verbose_name='پیام')
    subject = models.CharField(max_length=10, verbose_name='موضوع')

    class Meta:
        ordering = ['-subject']
        indexes = [models.Index(fields=['subject'])]
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'

    def __str__(self):
        return f'{self.name} : {self.subject}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='پست')
    name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نام کاربر')
    text = models.TextField(verbose_name='متن کامنت')
    active = models.BooleanField(default=False, verbose_name='وضعیت')
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    modified = jmodels.jDateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['created'])]
        verbose_name = 'کامنت'
        verbose_name_plural = ' کامنت ها'

    def __str__(self):
        return f'{self.name} : {self.text}'


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name='تصویر')
    image_file = ResizedImageField(upload_to="post_images/", size=[600, 400], quality=100, crop=['middle', 'center'])
    title = models.CharField(max_length=200, verbose_name='عنوان', null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    created = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['created'])]
        verbose_name = 'تصویر'
        verbose_name_plural = ' تصویر ها'

    def delete(self, *args, **kwargs):
        storage, path = self.image_file.storage, self.image_file.path
        storage.delete(path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else 'None'


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    photo = ResizedImageField(verbose_name="تصویر پروفایل", upload_to="account_images/", size=[500, 500],
                              quality=60, crop=['middle', 'center'], blank=True, null=True)
    date_of_birth = jmodels.jDateField(null=True, blank=True, verbose_name='تاریخ تولد')
    bio = models.TextField(null=True, blank=True, verbose_name='بیوگرافی')
    job = models.CharField(max_length=100, null=True, blank=True, verbose_name='شغل')

    class Meta:
        verbose_name = 'اکانت'
        verbose_name_plural = ' اکانت ها'

    def __str__(self):
        return self.user.username




