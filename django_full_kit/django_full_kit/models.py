from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .validators import auth,utils
from .upload_paths import user_avatar_upload_path
from django.utils import timezone

# --------------------------
# Advanced Fields
# --------------------------
class PhoneNumberField(models.CharField):
    """
    Custom Django model field for validating international phone numbers in E.164 format.
    Usage: like models.EmailField
    """
    default_validators = [
        auth.phone_number_validator
    ]

    description = "International phone number"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 16)
        super().__init__(*args, **kwargs)


class VideoField(models.FileField):
    """
    Custom Django model field for video
    Usage: like models.ImageField
    """
    default_validators = [
        utils.video_validator
    ]
    description = "support video"


class AudioField(models.FileField):
    """
    Custom Django model field for Audio
    Usage: like models.ImageField
    """
    default_validators = [
        utils.audio_validator
    ]
    description = "support audio"



# --------------------------
# Advanced Models
# --------------------------

# -------------
# User models
# -------------
class AdvancedBaseUser(AbstractUser):

    phone_number = PhoneNumberField(verbose_name=_("Phone number"),blank=True,null=True)
    bio = models.TextField(verbose_name=_("Biography"),blank=True,null=True)
    about = models.TextField(verbose_name=_("About"),blank=True,null=True,max_length=500)

    avatar = models.ImageField(verbose_name=_("Avatar"),upload_to=user_avatar_upload_path,blank=True,null=True)

    
    is_verify = models.BooleanField(verbose_name=_("Verify"),default=False)
    is_ban = models.BooleanField(verbose_name=_("Ban"),default=False)
    
    verify_date = models.DateTimeField(verbose_name=_("Verify date"),blank=True,null=True)
    ban_date = models.DateTimeField(verbose_name=_("Ban date"),blank=True,null=True)
    
    following = models.ManyToManyField("self",symmetrical=False,related_name="followers")
    
    def verify(self):
        self.is_verify = True
        self.verify_date = timezone.now()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        abstract = True

    def ban(self):
        self.is_ban = True
        self.ban_date = timezone.now()
    
    def get_followers(self):
        return self.followers.all()
    
    def get_following(self):
        return self.following.all()
    
    def get_full_name(self):
        return super().get_full_name()
    
    def get_short_name(self):
        return super().get_short_name()
    
    def __str__(self):
        return self.get_full_name or self.username