from django.test import TestCase
from django.urls import reverse

from .models import Cat

def create_cat(name, age, sex, color, is_vaccinated, is_house_trained, is_sterilized):
	"""
	Creates a cat in the database
	"""
	return Cat.objects.create(name=name, age=age, sex=sex, color=color, \
							  is_vaccinated=is_vaccinated, is_house_trained=is_house_trained, \
							  is_sterilized=is_sterilized)

def init_database():
	"""
	Initializes the test database and returns a list containing the objects created
	"""
	cat1 = create_cat(name="Mogus", age="Y", sex="M", color="WHT", is_vaccinated=True, is_house_trained=False, is_sterilized=True)
	cat2 = create_cat(name="Magous", age="S", sex="F", color="BLK", is_vaccinated=False, is_house_trained=True, is_sterilized=True)
	cat3 = create_cat(name="Migous", age="K", sex="F", color="BRN", is_vaccinated=True, is_house_trained=False, is_sterilized=False)
	cat4 = create_cat(name="Mugous", age="A", sex="M", color="ORA", is_vaccinated=False, is_house_trained=True, is_sterilized=False)

	return [cat1, cat2, cat3, cat4]

# Create your tests here.
class SearchResultsViewTests(TestCase):
	def test_no_cats(self):
		"""
		The results view when no cats exist in the database.
		"""
		response = self.client.get(reverse("search:results"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No pets are available :(")
		self.assertQuerySetEqual(response.context["cat_list"], [])

	def test_vaccinated(self):
		"""
		The results view when cats are required to be vaccinated.
		"""
		cat_list = init_database()

		response = self.client.get(reverse("search:results") + "?vaccinated=true")

		self.assertQuerySetEqual(
            response.context["cat_list"],
            [cat_list[0], cat_list[2]],
            ordered=False
        )

	def test_sterilized(self):
		"""
		The results view when cats are required to be sterilized.
		"""
		cat_list = init_database()

		response = self.client.get(reverse("search:results") + "?sterilized=true")

		self.assertQuerySetEqual(
            response.context["cat_list"],
            [cat_list[0], cat_list[1]],
            ordered=False
        )

	def test_house_trained(self):
		"""
		The results view when cats are required to be house-trained.
		"""
		cat_list = init_database()

		response = self.client.get(reverse("search:results") + "?house_trained=true")

		self.assertQuerySetEqual(
            response.context["cat_list"],
            [cat_list[1], cat_list[3]],
            ordered=False
        )

	def test_house_trained_and_sterilized(self):
		"""
		The results view when cats are required to be house-trained and sterilized.
		"""
		cat_list = init_database()

		response = self.client.get(reverse("search:results") + "?house_trained=true&sterilized=true")

		self.assertQuerySetEqual(
            response.context["cat_list"],
            [cat_list[1]],
            ordered=False
        )

	def test_male_only(self):
		"""
		The results view when cats are required to be male.
		"""
		cat_list = init_database()

		response = self.client.get(reverse("search:results") + "?sex=Male")

		self.assertQuerySetEqual(
            response.context["cat_list"],
            [cat_list[0], cat_list[3]],
            ordered=False
        )

	def test_young_only(self):
		"""
		The results view when cats are required to be young.
		"""
		cat_list = init_database()

		response = self.client.get(reverse("search:results") + "?age=Young")

		self.assertQuerySetEqual(
            response.context["cat_list"],
            [cat_list[0]],
            ordered=False
        )

	def test_male_or_female(self):
		"""
		The results view when cats can be male or female.
		"""
		cat_list = init_database()

		response = self.client.get(reverse("search:results") + "?sex=Male&sex=Female")

		self.assertQuerySetEqual(
            response.context["cat_list"],
            cat_list,
            ordered=False
        )

	def test_young_or_senior(self):
		"""
		The results view when cats can be young or senior.
		"""
		cat_list = init_database()

		response = self.client.get(reverse("search:results") + "?age=Young&age=Senior")

		self.assertQuerySetEqual(
            response.context["cat_list"],
            [cat_list[0], cat_list[1]],
            ordered=False
        )

	def test_kitten_or_adult_or_senior(self):
		"""
		The results view when cats can be kittens or adult or senior.
		"""
		cat_list = init_database()

		response = self.client.get(reverse("search:results") + "?age=Kitten&age=Adult&age=Senior")

		self.assertQuerySetEqual(
            response.context["cat_list"],
            [cat_list[1], cat_list[2], cat_list[3]],
            ordered=False
        )

	def test_male_kitten_and_adult(self):
		"""
		The results view when cats can be male kittens or adults
		"""
		cat_list = init_database()

		response = self.client.get(reverse("search:results") + "?age=Kitten&age=Adult&sex=Male")

		self.assertQuerySetEqual(
            response.context["cat_list"],
            [cat_list[3]],
            ordered=False
        )

	def test_female_young_and_senior(self):
		"""
		The results view when cats can be young females or female seniors
		"""
		cat_list = init_database()

		response = self.client.get(reverse("search:results") + "?age=Young&age=Senior&sex=Female")

		self.assertQuerySetEqual(
            response.context["cat_list"],
            [cat_list[1]],
            ordered=False
        )

	def test_no_checked(self):
		"""
		The results view when no conditions is specified (must contain every cat)
		"""
		cat_list = init_database()

		response = self.client.get(reverse("search:results"))

		self.assertQuerySetEqual(
            response.context["cat_list"],
            cat_list,
            ordered=False
        )

	def test_all_age_sex_checked(self):
		"""
		The results view when all age and sex conditions are specified (must also contain every cat)
		"""
		cat_list = init_database()

		response = self.client.get(reverse("search:results") + \
			"?age=Kitten&age=Young&age=Adult&age=Senior&sex=Male&sex=Female")

		self.assertQuerySetEqual(
            response.context["cat_list"],
            cat_list,
            ordered=False
        )

	def test_only_white(self):
		"""
		The results view when cats are required to be white.
		"""
		cat_list = init_database()

		response = self.client.get(reverse("search:results") + "?color=White")

		self.assertQuerySetEqual(
            response.context["cat_list"],
            [cat_list[0]],
            ordered=False
        )

	def test_brown_and_black(self):
		"""
		The results view when cats are required to be black or brown.
		"""
		cat_list = init_database()

		response = self.client.get(reverse("search:results") + "?color=Black&color=Brown")

		self.assertQuerySetEqual(
            response.context["cat_list"],
            [cat_list[1], cat_list[2]],
            ordered=False
        )

	def test_not_white_female(self):
		"""
		The results view when cats can't be white and must be female.
		"""
		cat_list = init_database()

		color_params = "&".join(["color={}".format(color) for color in Cat.Color.labels if color != "White"])

		response = self.client.get(reverse("search:results") + "?" + color_params + "&sex=Female")

		self.assertQuerySetEqual(
            response.context["cat_list"],
            [cat_list[1], cat_list[2]],
            ordered=False
        )

	def test_all_colors_allowed(self):
		"""
		The results view when cats can be any color.
		"""
		cat_list = init_database()

		color_params = "&".join(["color={}".format(color) for color in Cat.Color.labels])

		response = self.client.get(reverse("search:results") + "?" + color_params)

		self.assertQuerySetEqual(
            response.context["cat_list"],
            cat_list,
            ordered=False
        )

	def test_not_fulfilled_query(self):
		"""
		The results view when cats exist in the database but none fill the conditions.
		"""
		cat_list = init_database()

		response = self.client.get(reverse("search:results") + "?color=Orange&sex=Female")

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No pets are available :(")
		self.assertQuerySetEqual(response.context["cat_list"], [])