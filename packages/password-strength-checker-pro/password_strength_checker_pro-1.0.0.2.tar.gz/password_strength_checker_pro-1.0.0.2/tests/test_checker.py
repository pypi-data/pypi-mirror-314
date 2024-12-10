import unittest
from password_strength_checker import PasswordStrengthChecker

class TestPasswordStrengthChecker(unittest.TestCase):

    def setUp(self):
        self.checker = PasswordStrengthChecker(
            password="Test1234!",  # Example password
            min_length=8,
            min_uppercase=1,
            min_lowercase=1,
            min_digits=1,
            min_special_chars=1
        )

    def test_password_strength(self):
        self.checker = PasswordStrengthChecker(password="SomePassword123!")
        self.assertEqual(self.checker.calculate_password_strength(), "Very Strong Password")

    def test_leaked_password(self):
        # Mock a leaked password scenario by setting the password in the RockYou dataset
        self.checker.password = "123456"
        self.assertEqual(self.checker.is_valid(), "Password has been leaked")

if __name__ == '__main__':
    unittest.main()
