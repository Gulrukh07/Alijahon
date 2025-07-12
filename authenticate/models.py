from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser
from django.db.models import Model, ForeignKey, CASCADE, TextChoices, SET_NULL
from django.db.models.fields import CharField, TextField, DecimalField


class CustomUserManager(UserManager):
    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)

    create_superuser.alters_data = True

    async def acreate_superuser(
            self, phone_number, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return await self._acreate_user(phone_number, password, **extra_fields)

    def _create_user_object(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone_number must be set")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, phone_number, password, **extra_fields):
        user = self._create_user_object(phone_number, password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

class Region(Model):
    name = CharField(max_length=255)

class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey("authenticate.Region", CASCADE, related_name="districts")

class User(AbstractUser):
    class UserRoles(TextChoices):
        OPERATOR = 'operator', "Operator"
        ADMIN = 'admin', "Admin"
        USER = 'user', "User"
        DELIVERER = 'deliverer', "Deliverer"
    phone_number = CharField(max_length=15, unique=True)
    objects = CustomUserManager()
    EMAIL_FIELD = None
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "phone_number"
    district = ForeignKey("authenticate.District", SET_NULL, related_name="district_users", blank=True, null=True)
    address = CharField(max_length=255, blank=True, null=True)
    telegram_id = CharField(max_length=30, blank=True, null=True)
    about = TextField(blank=True, null=True)
    balance = DecimalField(max_digits=10 , decimal_places=0 , default=0)
    role = TextField(choices=UserRoles.choices, default=UserRoles.USER)
    email = CharField(max_length=255, blank=True, null=True, unique=True)
    username = CharField(max_length=255, blank=True, null=True)
    # email = None
    # username = None

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def wishlist_products(self):
        return list(self.wishlists.all().values_list("product_id", flat=True))



