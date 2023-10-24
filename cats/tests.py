from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from cats.models import Cat
from adopt.models import AdoptionRequest

def create_cat(name, age, sex, color, is_vaccinated, is_house_trained, is_sterilized, is_adopted=False):
	"""
	Creates a cat in the database
	"""
	return Cat.objects.create(name=name, age=age, sex=sex, color=color, \
							  is_vaccinated=is_vaccinated, is_house_trained=is_house_trained, \
							  is_sterilized=is_sterilized, is_adopted=is_adopted)

def create_adoption_request(cat_id, user_id):
	"""
	Creates an adoption request in the database
	"""
	return AdoptionRequest.objects.create(cat_id=cat_id, user_id=user_id)

def init_database(is_adopted_view=False):
	"""
	Initializes the test database and returns a list containing the objects created
	"""
	cat1 = create_cat(name="Mogus", age="Y", sex="M", color="WHT", is_vaccinated=True, is_house_trained=False, is_sterilized=True)
	cat2 = create_cat(name="Magous", age="S", sex="F", color="BLK", is_vaccinated=False, is_house_trained=True, is_sterilized=True)
	cat3 = create_cat(name="Migous", age="K", sex="F", color="BRN", is_vaccinated=True, is_house_trained=False, is_sterilized=False)
	cat4 = create_cat(name="Mugous", age="A", sex="M", color="ORA", is_vaccinated=False, is_house_trained=True, is_sterilized=False)
	cat5 = create_cat(name="Mugous", age="A", sex="M", color="ORA", is_vaccinated=False, is_house_trained=True, is_sterilized=False, is_adopted=True)

	# Initialize the test users
	user1 = User.objects.create(username='testuser')
	user1.set_password('12345')
	user1.save()

	if is_adopted_view:
		user2 = User.objects.create(username='testuser2')
		user2.set_password('67890')
		user2.save()

		# Create adoption requests
		req = create_adoption_request(cat1.id, user1.id)
		req.status = AdoptionRequest.Status.APPROVED
		req.save()

		req = create_adoption_request(cat2.id, user1.id)
		req.status = AdoptionRequest.Status.PENDING
		req.save()

		req = create_adoption_request(cat3.id, user1.id)
		req.status = AdoptionRequest.Status.REJECTED
		req.save()	

		req = create_adoption_request(cat4.id, user2.id)
		req.status = AdoptionRequest.Status.APPROVED
		req.save()

# Create your tests here.
class DetailsViewTests(TestCase):
	def test_cat_not_exists(self):
		"""
		The details view when the requested cat doesn't exist. We expect 404 not found.
		"""
		init_database()

		response = self.client.get(reverse("cats:detail", kwargs={'pk':6}))
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

		self.assertContains(response, "Vaccinated: Yes")
		self.assertContains(response, "Sterilized: Yes")
		self.assertContains(response, "House-trained: No")

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

	def test_adopt_not_displays_when_pending_exists(self):
		"""
		If the request has a pending request for this cat, the "Adopt" button
		should not be displayed.
		"""
		init_database(is_adopted_view=True)

		# Authenticate the user now that we have created it
		self.client.login(username="testuser", password="12345")

		response = self.client.get(reverse("cats:detail", kwargs={'pk':2}))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "You already have a pending request for this cat!")
		self.assertNotContains(response, "<input type=\"submit\" value=\"Adopt\">")

	def test_adopted_cat_not_found(self):
		"""
		If a cat has been already adopted, it should not display.
		"""
		init_database()

		self.client.login(username="testuser", password="12345")

		response = self.client.get(reverse("cats:detail", kwargs={'pk':5}))

		self.assertEqual(response.status_code, 404)

class AdoptedDetailsViewTests(TestCase):
	def test_cat_not_exists(self):
		"""
		The adopted details view when the requested cat doesn't exist. We expect 404 not found.
		"""
		init_database(is_adopted_view=True)

		self.client.login(username="testuser", password="12345")

		response = self.client.get(reverse("cats:adopted_detail", kwargs={'pk':6}))
		self.assertEqual(response.status_code, 404)

	def test_not_authenticated_user(self):
		"""
		The details view when the user hasn't been authenticated. We
		expect an error message to appear instead of the adopt button.
		"""
		init_database(is_adopted_view=True)

		response = self.client.get(reverse("cats:adopted_detail", kwargs={'pk':1}))

		self.assertEqual(response.status_code, 302)
		self.assertEqual(reverse("accounts:login") + "?next=" + reverse("cats:adopted_detail", kwargs={'pk':1}), response.url)

	def test_cat_exists_but_no_request(self):
		"""
		If the cat exists but the user hasn't made an adoption request
		for it, there is no chance they have adopted it, so we expect
		404 on the adopted details view.
		"""
		init_database(is_adopted_view=True)

		self.client.login(username="testuser", password="12345")

		response = self.client.get(reverse("cats:adopted_detail", kwargs={'pk':4}))
		self.assertEqual(response.status_code, 404)

	def test_cat_exists_but_request_pending(self):
		"""
		If the cat exists and the user has made an adoption request
		for it, but it is still pending, the cat is not adopted by that user so
		we expect 404 on the adopted details view.
		"""
		init_database(is_adopted_view=True)

		self.client.login(username="testuser", password="12345")

		response = self.client.get(reverse("cats:adopted_detail", kwargs={'pk':2}))
		self.assertEqual(response.status_code, 404)

	def test_cat_exists_but_request_rejected(self):
		"""
		If the cat exists and the user has made an adoption request
		for it, but it was rejected, the cat is not adopted by that user so
		we expect 404 on the adopted details view.
		"""
		init_database(is_adopted_view=True)

		self.client.login(username="testuser", password="12345")

		response = self.client.get(reverse("cats:adopted_detail", kwargs={'pk':3}))
		self.assertEqual(response.status_code, 404)

	def test_cat_exists_and_request_approved(self):
		"""
		If the cat exists and the user has made an adoption request
		for it that was approved, the cat belongs to that user so 
		the adoption details page is displayed.
		"""
		init_database(is_adopted_view=True)

		self.client.login(username="testuser", password="12345")

		response = self.client.get(reverse("cats:adopted_detail", kwargs={'pk':1}))
		self.assertEqual(response.status_code, 200)

		self.assertContains(response, "Mogus")
		self.assertContains(response, "Young")
		self.assertContains(response, "Male")
		self.assertContains(response, "White")

		self.assertContains(response, "Vaccinated: Yes")
		self.assertContains(response, "Sterilized: Yes")
		self.assertContains(response, "House-trained: No")
