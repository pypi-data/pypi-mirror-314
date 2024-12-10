import gzip
import os
from dataclasses import dataclass

@dataclass
class PasswordStrengthChecker:
    password: str
    min_length: int = 8
    min_uppercase: int = 1
    min_lowercase: int = 1
    min_digits: int = 1
    min_special_chars: int = 1
    rockyou_gz_file: str = "rockyou.txt.gz"  # Default value

    def __post_init__(self):
        self.rockyou_passwords = set()
        self.load_rockyou_dataset()

    def load_rockyou_dataset(self):
        """Load the RockYou dataset from a compressed .gz file."""
        try:
            # Get the package path for 'rockyou.txt.gz'
            base_dir = os.path.dirname(__file__)  # Get the current directory of the script
            data_dir = os.path.join(base_dir, 'data')  # Define the 'data' directory path
            file_path = os.path.join(data_dir, self.rockyou_gz_file)  # Full path to the file

            print(f"Loading RockYou dataset from {file_path}...")

            with gzip.open(file_path, "rt", encoding="latin1") as rockyou:
                self.rockyou_passwords = set(rockyou.read().splitlines())
            print(f"RockYou dataset loaded with {len(self.rockyou_passwords)} passwords.")
        except FileNotFoundError:
            print(f"Error: File '{self.rockyou_gz_file}' not found in the data directory.")
        except Exception as e:
            print(f"An error occurred while loading RockYou dataset: {e}")

    def is_valid(self):
        """Check if the password meets strength criteria and if it's found in the RockYou dataset."""
        if self.password_in_leaked_dataset():
            return "Password has been leaked"

        strength = self.calculate_password_strength()
        return strength

    def calculate_password_strength(self):
        """Calculate the password strength based on the criteria."""
        score = 0
        password = self.password

        # Check each criterion and add points accordingly
        if len(password) >= self.min_length:
            score += 1
        if sum(1 for c in password if c.isupper()) >= self.min_uppercase:
            score += 1
        if sum(1 for c in password if c.islower()) >= self.min_lowercase:
            score += 1
        if sum(1 for c in password if c.isdigit()) >= self.min_digits:
            score += 1
        if sum(1 for c in password if c in "!@#$%^&*()_+-=[]{}|;:,.<>?/~") >= self.min_special_chars:
            score += 1

        # Calculate percentage score
        score_percentage = (score / 5) * 100

        # Return strength based on score
        if score_percentage == 0:
            return "Very Weak Password"
        elif 0 < score_percentage <= 20:
            return "Very Weak Password"
        elif 21 <= score_percentage <= 40:
            return "Weak Password"
        elif 41 <= score_percentage <= 60:
            return "Medium Password"
        elif 61 <= score_percentage <= 80:
            return "Strong Password"
        else:
            return "Very Strong Password"

    def password_in_leaked_dataset(self):
        """Check if the password is in the RockYou dataset."""
        password = self.password.strip()
        if password in self.rockyou_passwords:
            return True
        return False
