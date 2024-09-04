import unittest
import re



#This function generates email addresses
def generate_email(name):
    name_parts = name.split()
    if len(name_parts) == 2:
        email = f"{name_parts[0][0]}{name_parts[1].lower()}@gmail.com"
    else:
        email = f"{name_parts[0][0]}{name_parts[-1].lower()}@gmail.com"
    email = email.replace("'", "").replace(" ", "").replace("-", "")
    return email

#This function finds the names with special characters
def has_special_chars(name):
    return bool(re.search(r"[^a-zA-Z\s]", name))

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()


