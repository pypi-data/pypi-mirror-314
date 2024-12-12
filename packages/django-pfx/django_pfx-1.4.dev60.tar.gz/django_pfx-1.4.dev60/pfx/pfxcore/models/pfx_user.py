from django.contrib.auth.models import AbstractUser

from .abstract_pfx_base_user import AbstractPFXBaseUser


class PFXUser(AbstractUser, AbstractPFXBaseUser):
    """The Django User with PFX mixin.
    """

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
