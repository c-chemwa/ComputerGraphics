import unittest

def generate_email(name):
    name_parts = name.split()
    if len(name_parts) == 2:
        email = f"{name_parts[0][0]}{name_parts[1].lower()}@gmail.com"
    else:
        email = f"{name_parts[0][0]}{name_parts[-1].lower()}@gmail.com"
    email = email.replace("'", "").replace(" ", "").replace("-", "")
    return email

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()


