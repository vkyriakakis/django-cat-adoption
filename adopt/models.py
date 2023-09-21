from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

class Cat(models.Model):
    name = models.CharField(max_length=20)

    class Age(models.TextChoices):
        KITTEN = "K", _("Kitten")
        YOUNG = "Y", _("Young")
        ADULT = "A", _("Adult")
        SENIOR = "S", _("Senior")

    age = models.CharField(
        max_length=1,
        choices=Age.choices,
    )
    
    class Sex(models.TextChoices): 
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")

    sex = models.CharField(
        max_length=1,
        choices=Sex.choices,
    )

    class Color(models.TextChoices):
        BLACK = "BLK", _("Black")
        CALICO = "CAL", _("Calico")
        WHITE = "WHT", _("White")
        BLUE = "BLU", _("Blue")
        GRAY = "GRA", _("Gray")
        ORANGE = "ORA", _("Orange")
        BROWN = "BRN", _("Brown")

    color = models.CharField(
        max_length=3,
        choices=Color.choices,
    )

    image = models.ImageField(upload_to='adopt/images/cats')

    is_sterilized = models.BooleanField()
    is_vaccinated = models.BooleanField()
    is_house_trained = models.BooleanField()

    def __str__(self):
        return "{}, {} {}".format(self.name, self.get_sex_display(), self.get_age_display())