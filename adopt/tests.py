from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from cats.models import Cat
from adopt.models import AdoptionRequest

def create_cat(name, age, sex, color, is_vaccinated, is_house_trained, is_sterilized):
	"""
	Creates a cat in the database
	"""
	return Cat.objects.create(name=name, age=age, sex=sex, color=color, \
							  is_vaccinated=is_vaccinated, is_house_trained=is_house_trained, \
							  is_sterilized=is_sterilized)

def create_adoption_request(cat_id, user_id):
	"""
	Creates an adoption request in the database
	"""
	return AdoptionRequest.objects.create(cat_id=cat_id, user_id=user_id)

def init_database(user1_empty=True):
	"""
	Initializes the test database and returns a list containing the objects created
	"""
	cat1 = create_cat(name="Mogus", age="Y", sex="M", color="WHT", is_vaccinated=True, is_house_trained=False, is_sterilized=True)
	cat2 = create_cat(name="Magous", age="S", sex="F", color="BLK", is_vaccinated=False, is_house_trained=True, is_sterilized=True)
	cat3 = create_cat(name="Migous", age="K", sex="F", color="BRN", is_vaccinated=True, is_house_trained=False, is_sterilized=False)
	cat4 = create_cat(name="Mugous", age="A", sex="M", color="ORA", is_vaccinated=False, is_house_trained=True, is_sterilized=False)

	# Initialize the test user database
	user1 = User.objects.create(username='testuser')
	user1.set_password('12345')
	user1.save()

	user2 = User.objects.create(username='testuser2')
	user2.set_password('67890')
	user2.save()

	# Add some adoption requests
	req1 = create_adoption_request(cat2.id, user2.id)
	req2 = create_adoption_request(cat4.id, user2.id)

	# If the appropriate setting is used, add a request to user1 as well
	if not user1_empty:
		create_adoption_request(cat3.id, user1.id)

	return req1, req2


class MyAdoptionsViewTest(TestCase):
	def test_unauthorized_user(self):
		"""
		Tests the case when a user hasn't logged in, so they should be redirected to the login page.
		"""
		init_database()

		response = self.client.get(reverse("adopt:my_adoptions"))

		self.assertRedirects(response, "/accounts/login/?next=" + reverse("adopt:my_adoptions"))

	def test_no_adoptions(self):
		"""
		Tests the case when a user has logged in, but hasn't requested to adopt any cats.
		"""
		init_database()

		self.client.login(username="testuser", password="12345")
		response = self.client.get(reverse("adopt:my_adoptions"))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "You haven't made any adoption requests!")
		self.assertQuerySetEqual(
            response.context["request_list"],
            [],
            ordered=False
        )

	def test_some_adoptions(self):
		"""
		Tests the case when a user has logged in, and has requested to adopt some cats.
		"""
		req1, req2 = init_database()

		self.client.login(username="testuser2", password="67890")
		response = self.client.get(reverse("adopt:my_adoptions"))

		self.assertQuerySetEqual(
            response.context["request_list"],
            [req1, req2],
            ordered=False
        )

class RequestAdoptionViewTest(TestCase):
	def test_unauthorized_user(self):
		"""
		Tests the case where an unauthorized user attempts to make an adoption request.
		They should be redirected to the login page.
		"""
		init_database()

		response = self.client.post(reverse("adopt:adopt", kwargs={'cat_id':1}))

		self.assertRedirects(response, reverse("login") + "?next=" + reverse("adopt:adopt", kwargs={'cat_id':1}))

	def test_get_instead_of_post(self):
		"""
		Tests the case where a GET request is made to the adoption URL.
		It should give the status code 405 (Method Not Allowed).
		"""
		init_database()

		self.client.login(username="testuser2", password="67890")
		response = self.client.get(reverse("adopt:adopt", kwargs={'cat_id':2}))

		self.assertEqual(response.status_code, 405)

	def test_request_already_exists(self):
		"""
		Tests the case where an authenticated user tries to request to adopt
		a cat that they have already requested. A new request shouldn't be created
		and they should be redirected to the cat detail page with an error message.
		"""
		init_database()

		self.client.login(username="testuser2", password="67890")
		response = self.client.post(reverse("adopt:adopt", kwargs={'cat_id':2}))

		# Test that the user got redirected
		self.assertRedirects(response, reverse("cats:detail", kwargs={'pk':2}))

		# Test that another request for that cat wasn't added
		self.assertEqual(len(AdoptionRequest.objects.filter(user__id=2, cat__id=2)), 1)

	def test_request_created_successfully(self):
		"""
		Tests the case where an authenticated user makes an adoption request
		successfully. They should be redirected to the "My Adoptions" page,
		and that page should display the new request.
		"""
		init_database()

		self.client.login(username="testuser2", password="67890")
		response = self.client.post(reverse("adopt:adopt", kwargs={'cat_id':1}))

		# Test that the user got redirected to my_adoptions
		self.assertRedirects(response, reverse("adopt:my_adoptions"))
		
		# Also that the request was actually added to the database
		self.assertTrue(AdoptionRequest.objects.filter(user__id=2, cat__id=1).exists())

class DeleteAdoptionViewTest(TestCase):
	def test_unauthorized_user(self):
		"""
		Tests the case where an unauthorized user attempts to make an adoption request.
		They should be redirected to the login page.
		"""
		init_database()

		response = self.client.post(reverse("adopt:delete_adoption"), {"to_delete": "2"})

		self.assertRedirects(response, reverse("login") + "?next=" + reverse("adopt:delete_adoption"))

	def test_get_instead_of_post(self):
		"""
		Tests the case where a GET request is made to the adoption URL.
		It should give the status code 405 (Method Not Allowed).
		"""
		init_database()

		self.client.login(username="testuser2", password="67890")
		response = self.client.get(reverse("adopt:delete_adoption"), {"to_delete": "2"})

		self.assertEqual(response.status_code, 405)

	def test_no_ids_were_given(self):
		"""
		Tests the case where no ids are given in the delete link. Then
		the server should return 400 - Bad Request.
		"""
		init_database()

		self.client.login(username="testuser2", password="67890")
		response = self.client.post(reverse("adopt:delete_adoption"))

		self.assertEqual(response.status_code, 400)	

	def test_some_id_not_found(self):
		"""
		Tests the case where at least one of the adoption ids 
		requested to be deleted does not exist. It should give 404
		and no adoption should be deleted, even the correct ones.
		"""
		init_database()

		self.client.login(username="testuser2", password="67890")
		response = self.client.post(reverse("adopt:delete_adoption"), {"to_delete": ["2", "4"]})

		self.assertEqual(response.status_code, 404)
		self.assertTrue(AdoptionRequest.objects.filter(id=2).exists())

	def test_some_id_belongs_to_other_user(self):
		"""
		Tests the case where at least one of the adoption ids 
		requested to be deleted belongs to another user. It should give 403 (forbidden)
		and no adoption should be deleted, even the ones belonging to the correct user.
		"""
		init_database(user1_empty=False)

		self.client.login(username="testuser", password="12345")
		response = self.client.post(reverse("adopt:delete_adoption"), {"to_delete": ["2", "3"]})

		self.assertEqual(response.status_code, 403)
		self.assertTrue(AdoptionRequest.objects.filter(id=3).exists())

	def test_deletion_success(self):
		"""
		Tests the case where the deletion happens successfully.
		The user should be redirected to the "My adoptions" page and
		the adoption should have been removed from the database.
		"""
		init_database()

		self.client.login(username="testuser2", password="67890")
		response = self.client.post(reverse("adopt:delete_adoption"), {"to_delete": "2"})

		self.assertRedirects(response, reverse("adopt:my_adoptions"))
		self.assertFalse(AdoptionRequest.objects.filter(id=2).exists())