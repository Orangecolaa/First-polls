from django.db import models
import datetime


class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()  # 进组时间
    invite_reason = models.CharField(max_length=64)  # 邀请原因


# 抽象基类
# 1.
class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True


class Student(CommonInfo):
    home_group = models.CharField(max_length=5)


# 多表继承
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)


class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)


# 验证器
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )


# full_clean()
class MyModel(models.Model):
    even_field = models.IntegerField(validators=[validate_even])

    def save(self, *args, **kwargs):  # 重写save方法是关键
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            print('模型验证没通过： %s' % e.message_dict)


# clean()
class Article(models.Model):
    content = models.TextField()
    status = models.CharField(max_length=32)
    pub_date = models.DateField(blank=True, null=True)

    def clean(self):
        # 不允许草稿文章具有发布日期字段
        if self.status == '草稿' and self.pub_date is not None:
            raise ValidationError(_('草稿文章尚未发布，不应该有发布日期！'))

        # 如果已发布的文章还没有设置发布日期，则将发布日期设置为当天
        if self.status == '已发布' and self.pub_date is None:
            self.pub_date = datetime.date.today()

    def save(self, *args, **kwargs):

        from django.core.exceptions import NON_FIELD_ERRORS

        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            print('验证没通过：%s' % e.message_dict[NON_FIELD_ERRORS])


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField()
    number_of_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.headline


class Dog(models.Model):
    name = models.CharField(max_length=200)
    data = models.JSONField(null=True)

    def __str__(self):
        return self.name
