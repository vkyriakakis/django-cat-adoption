from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

def init_database():
	"""
	Populates the test database with some users and returns them
	"""
	user1 = User.objects.create(username='testuser')
	user1.set_password('12345')
	user1.save()

	user2 = User.objects.create(username='testuser2')
	user2.set_password('67890')
	user2.save()

	return user1, user2

class RegistrationViewTest(TestCase):
	def test_register_fail_no_username(self):
		"""
		Tests whether the registrastion fails if no username is supplied.
		"""
		data = {
			"email": "pass@word.pass", 
			"password": "password", 
			"first_name": "Pass", 
			"last_name": "Word"
		}

		response = self.client.post(reverse("accounts:registration"), data)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "This field is required")

		# Check that the form now contains the values the user input
		self.assertContains(response, data["email"])
		self.assertContains(response, data["first_name"])
		self.assertContains(response, data["last_name"])

	def test_register_fail_no_email(self):
		"""
		Tests whether the registrastion fails if no email is supplied.
		"""
		data = {
			"username": "pass_word", 
			"password": "password", 
			"first_name": "Pass", 
			"last_name": "Word"
		}

		response = self.client.post(reverse("accounts:registration"), data)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "This field is required")

		# Check that the form now contains the values the user input
		self.assertContains(response, data["username"])
		self.assertContains(response, data["first_name"])
		self.assertContains(response, data["last_name"])

	def test_register_fail_mismatched_passwords(self):
		"""
		Tests whether the registrastion fails if the password fields are mismatched.
		"""
		data = {
			"username": "pass_word",
			"email": "pass@word.pass", 
			"password": "password",
			"repeat_password": "passwod",
			"first_name": "Pass", 
			"last_name": "Word"
		}

		response = self.client.post(reverse("accounts:registration"), data)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "The password must be the same in both fields")

		# Check that the form now contains the values the user input
		self.assertContains(response, data["username"])
		self.assertContains(response, data["email"])
		self.assertContains(response, data["first_name"])
		self.assertContains(response, data["last_name"])
	
	def test_register_fail_existing_username(self):
		"""
		Tests whether the registrastion fails if the username belongs to another user.

		A user with that username already exists
		"""
		init_database()

		data = {
			"username": "testuser",
			"email": "pass@word.pass", 
			"password": "password",
			"repeat_password": "passwod",
			"first_name": "Pass", 
			"last_name": "Word"
		}

		response = self.client.post(reverse("accounts:registration"), data)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "A user with that username already exists")

		# Check that the form now contains the values the user input
		self.assertContains(response, data["username"])
		self.assertContains(response, data["email"])
		self.assertContains(response, data["first_name"])
		self.assertContains(response, data["last_name"])

	def test_register_successfully_without_non_mandatory(self):
		"""
		Tests whether the registration succeeds and a user is created,
		even if the non-required fields aren't supplied
		"""
		data = {
			"username": "pass_word",
			"email": "pass@word.pass", 
			"password": "password",
			"repeat_password": "password",
		}

		response = self.client.post(reverse("accounts:registration"), data)

		# Test that a redirect to the response success page was returned
		self.assertEqual(response.status_code, 302)
		self.assertEqual(reverse("accounts:registration_done"), response.url)

		# Test that the new user exists in the database
		new_user = User.objects.get(username="pass_word")
		self.assertEqual(new_user.email, "pass@word.pass")
		self.assertTrue(new_user.check_password("password"))

	def test_register_successfully(self):
		"""
		Tests whether the registration succeeds and a user is created,
		when all the fields are supplied
		"""
		data = {
			"username": "pass_word",
			"email": "pass@word.pass", 
			"password": "password",
			"repeat_password": "password",
			"first_name": "Pass", 
			"last_name": "Word"
		}

		response = self.client.post(reverse("accounts:registration"), data)

		# Test that a redirect to the response success page was returned
		self.assertEqual(response.status_code, 302)
		self.assertEqual(reverse("accounts:registration_done"), response.url)

		# Test that the new user exists in the database
		new_user = User.objects.get(username="pass_word")
		self.assertEqual(new_user.email, "pass@word.pass")
		self.assertEqual(new_user.first_name, "Pass")
		self.assertEqual(new_user.last_name, "Word")
		self.assertTrue(new_user.check_password("password"))

class RegistrationDoneViewTest(TestCase):
	def test_non_authenticated(self):
		"""
		If the user isn't authenticated, display the register
		success message
		"""
		response = self.client.get(reverse("accounts:registration_done"))
		
		self.assertContains(response, "Registration successful!")

	def test_authenticated(self):
		"""
		If the user is authenticated, redirect them to the home page
		"""
		init_database()

		self.client.login(username="testuser", password="12345")
		response = self.client.get(reverse("accounts:registration_done"))

		self.assertEqual(response.status_code, 302)
		self.assertEqual(reverse("index"), response.url)