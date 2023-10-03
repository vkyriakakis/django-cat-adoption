from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from cats.models import Cat

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

	# Initialize the test user
	user = User.objects.create(username='testuser')
	user.set_password('12345')
	user.save()

	return [cat1, cat2, cat3, cat4]

# Create your tests here.
class DetailsViewTests(TestCase):
	def test_cat_not_exists(self):
		"""
		The details view when the requested cat doesn't exist. We expect 404 not found.
		"""
		init_database()

		response = self.client.get(reverse("cats:detail", kwargs={'pk':5}))
		self.assertEqual(response.status_code, 404)

	def test_cat_displays_correctly(self):
		"""
		The details view when the requested cat exists. We expect all cat
		information to display.
		"""
		init_database()

		response = self.client.get(reverse("cats:detail", kwargs={'pk':1}))

		self.assertEqual(response.status_code, 200)

		self.assertContains(response, "Mogus")
		self.assertContains(response, "Young")
		self.assertContains(response, "Male")
		self.assertContains(response, "White")

		self.assertContains(response, "Vaccinated")
		self.assertContains(response, "Sterilized")
		self.assertNotContains(response, "House-trained")

	def test_no_adopt_for_anon_user(self):
		"""
		The details view when the user hasn't been authenticated. We
		expect an error message to appear instead of the adopt button.
		"""
		init_database()

		response = self.client.get(reverse("cats:detail", kwargs={'pk':1}))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "You need to login before requesting to adopt a cat!")
		self.assertNotContains(response, "<input type=\"submit\" value=\"Adopt\">")

	def test_adopt_displays_for_authenticated(self):
		"""
		The details view when the user has been authenticated. We
		expect the adopt button to appear.
		"""
		init_database()

		# Authenticate the user now that we have created it
		self.client.login(username="testuser", password="12345")

		response = self.client.get(reverse("cats:detail", kwargs={'pk':1}))

		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, "You need to login before requesting to adopt a cat!")
		self.assertContains(response, "<input type=\"submit\" value=\"Adopt\">")
