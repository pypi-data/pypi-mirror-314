from django.contrib.auth.models import AbstractBaseUser


class AbstractPFXBaseUser(AbstractBaseUser):
    """The base abstract user for PFX."""

    class Meta:
        abstract = True

    def get_user_jwt_signature_key(self):
        """
        Return a user secret to sign JWT token.

        If not empty, the JWT token validity depends on all values
        user to build the return string. So, each time the returned value
        changes, the previously issued tokens will no longer be valid.
        """
        return self.password
