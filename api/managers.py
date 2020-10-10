from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, dni, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not dni:
            raise ValueError('The given dni must be set')
        #email = self.normalize_email(email)
        user = self.model(dni=dni, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, dni, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(dni, password, **extra_fields)

    def create_superuser(self, dni, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(dni, password, **extra_fields)