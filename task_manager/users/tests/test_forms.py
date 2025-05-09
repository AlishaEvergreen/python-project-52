from task_manager.users.forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
)
from task_manager.users.tests.testcase import UserTestCase
from task_manager.users.models import User


class TestCustomUserCreationForm(UserTestCase):
    def get_form(self, overrides=None):
        data = self.valid_user_data.copy()
        if overrides:
            data.update(overrides)
        return CustomUserCreationForm(data=data)

    def test_valid_data(self):
        form = self.get_form()
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, self.valid_user_data['username'])
        self.assertEqual(User.objects.count(), self.user_count + 1)

    def test_missing_fields(self):
        cases = [
            {'username': self.valid_user_data['username']},
            {
                'username': self.valid_user_data['username'],
                'password1': 'test123',
            },
            {'first_name': 'Test', 'last_name': 'User'},
        ]

        for data in cases:
            with self.subTest(data=data):
                form = CustomUserCreationForm(data=data)
                self.assertFalse(form.is_valid())

    def test_password_too_short(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data.update({
            'password1': '12',
            'password2': '12'
        })
        form = CustomUserCreationForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_invalid_username(self):
        test_cases = [
            '!!!',
            'user#name',
            'user name',
            'x' * 151,
        ]

        for username in test_cases:
            with self.subTest(username=username):
                invalid_data = self.valid_user_data.copy()
                invalid_data['username'] = username
                form = CustomUserCreationForm(data=invalid_data)
                self.assertFalse(form.is_valid())
                self.assertIn('username', form.errors)

    def test_passwords_do_not_match(self):
        form = self.get_form({'password2': 'Different123'})
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_empty_strings(self):
        form = self.get_form({
            'first_name': '',
            'last_name': '',
            'username': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)

    def test_duplicate_username(self):
        form = self.get_form({'username': 'john_snow'})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class TestCustomUserChangeForm(UserTestCase):
    def get_form(self, overrides=None):
        data = self.update_user_data.copy()
        data.update({
            'password': data.pop('password1'),
            'password_confirmation': data.pop('password2')
        })
        if overrides:
            data.update(overrides)
        return CustomUserChangeForm(data=data, instance=self.user1)

    def test_valid_password_update(self):
        form = self.get_form()
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, self.update_user_data['username'])
        self.assertTrue(user.check_password(
            self.update_user_data['password1']
        ))

    def test_passwords_do_not_match(self):
        form = self.get_form({'password_confirmation': 'WrongConfirm'})
        self.assertFalse(form.is_valid())
        self.assertIn('password_confirmation', form.errors)

    def test_short_password(self):
        form = self.get_form({
            'password': '12',
            'password_confirmation': '12'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password_confirmation', form.errors)

    def test_missing_password_fields(self):
        for case in [
            {'password': '', 'password_confirmation': 'SomePassword'},
            {'password': 'SomePassword', 'password_confirmation': ''}
        ]:
            with self.subTest(case=case):
                form = self.get_form(case)
                self.assertFalse(form.is_valid())
                self.assertIn('password_confirmation', form.errors)

    def test_update_with_existing_valid_password(self):
        form = self.get_form({
            'password': 'QueenInNorth456',
            'password_confirmation': 'QueenInNorth456',
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.check_password('QueenInNorth456'))
