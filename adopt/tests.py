from django.test import TestCase
from django.urls import reverse

from .models import Cat

def create_cat(name, age, sex, color, is_vaccinated, is_house_trained, is_sterilized):
	"""
	Create a question with the given `question_text` and published the
	given number of `days` offset to now (negative for questions published
	in the past, positive for questions that have yet to be published).
	"""
	return Cat.objects.create(name=name, age=age, sex=sex, color=color, \
							  is_vaccinated=is_vaccinated, is_house_trained=is_house_trained, \
							  is_sterilized=is_sterilized)

# Create your tests here.
class SearchResultsViewTests(TestCase):
	def test_no_cats(self):
		"""
		The results view when no cats exist in the database.
		"""
		response = self.client.get(reverse("adopt:search_results"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No pets are available :(")
		self.assertQuerySetEqual(response.context["cat_list"], [])

	def test_vaccinated(self):
		"""
		The results view when cats are required to be vaccinated.
		"""
		cat1 = create_cat(name="Mogus", age="Y", sex="M", color="WHT", is_vaccinated=True, is_house_trained=False, is_sterilized=True)
		cat2 = create_cat(name="Magous", age="S", sex="F", color="BLK", is_vaccinated=False, is_house_trained=True, is_sterilized=True)
		cat3 = create_cat(name="Migous", age="K", sex="F", color="BRN", is_vaccinated=True, is_house_trained=False, is_sterilized=False)
		cat4 = create_cat(name="Mugous", age="A", sex="M", color="ORA", is_vaccinated=False, is_house_trained=True, is_sterilized=False)

		response = self.client.get(reverse("adopt:search_results") + "?vaccinated=true")

		self.assertQuerySetEqual(
            response.context["cat_list"],
            [cat1, cat3],
        )


	def test_sterilized(self):
		pass

	def test_house_trained(self):
		pass

	def test_male_only(self):
		pass

	def test_young_only(self):
		pass

	def test_male_and_female(self):
		pass

	def test_young_and_senior(self):
		pass

	def test_kitten_and_adult_and_senior(self):
		pass

	def test_male_kitten_and_adult(self):
		pass

	def test_female_young_and_senior(self):
		pass

	def test_no_checked(self):
		pass

	def test_all_checked(self):
		pass