from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

def user_directory_path(instance, filename):

    return 'customers/{0}/documents/{1}'.format(instance.user.id, filename)
class UserDocument(models.Model):
    user_link = models.ForeignKey(User, related_name="user_document", on_delete=models.CASCADE, blank=False, null=False)
    filename = models.CharField(max_length=255,blank=False,null=False,default="")
    document = models.FileField(upload_to=user_directory_path)

class Contact(models.Model):
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    user_link = models.OneToOneField(User, related_name="user_link", on_delete=models.CASCADE)

    def __str__(self):
        return self.email
class Profile(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="customers/profiles/avatars/", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=32, null=True, blank=True)
    mobile_number = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=30, null=True, blank=True)
    iban = models.CharField(max_length=32, null=True, blank=True)

    skype = models.CharField(max_length=32, null=True, blank=True)
    facebook = models.CharField(max_length=32, null=True, blank=True)
    twitter = models.CharField(max_length=32, null=True, blank=True)
    linkedin = models.CharField(max_length=32, null=True, blank=True)
    instagram = models.CharField(max_length=32, null=True, blank=True)
    dribble = models.CharField(max_length=32, null=True, blank=True)
    pinterest = models.CharField(max_length=32, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else 'assets/img/team/default-profile-picture.png'
