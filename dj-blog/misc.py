# import json
import random
import string

import secrets

# from tests.factories import ArticleFactory


# def generate_random_string(length=5):
#     """Generate a random string of lowercase letters."""
#     return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


# def generate_json_data(num_records=2):
#     """Generate JSON data with id, name, and slug."""
#     data = []

#     for i in range(1, num_records + 1):
#         record = {
#             "model": "blog.Category",
#             "pk": str(i),
#             "fields": {
#                 "name": f"Name-{i}",
#                 "slug": generate_random_string(),
#             },
#         }
#         data.append(record)

#     return data


# if __name__ == "__main__":
#     # Change the argument to generate a different number of records
#     json_data = generate_json_data(num_records=2)

#     with open("./blog/fixtures/category_data.json", "w") as file:
#         json.dump(json_data, file, indent=2)

# print("JSON data has been generated and saved to 'generated_data.json'.")


import json
from faker import Faker

fake = Faker()


def generate_fake_article():
    return {
        "model": "blog.Article",
        "pk": str(secrets.randbelow(1000) + 1),
        "fields": {
            "title": fake.sentence(),
            "author": 5,
            "content": fake.paragraph(),
            "image": "media/article_pics/default.png",
            "publish": str(fake.date_time_this_decade(tzinfo=None).isoformat()),
            "status": fake.random_element(elements=("draft", "published")),
            "slug": fake.slug(),
            # "tags": [fake.random_int(min=1, max=100) for _ in range(5)],
            "category": random.choice([1, 2]),
            "likes": [],
            "snippet": fake.sentence(),
        },
    }


def generate_n_articles_json(n):
    articles_json_data = [generate_fake_article() for _ in range(n)]
    return articles_json_data


# Example usage to generate 5 articles
n = 10
articles_json_list = generate_n_articles_json(n)
output_file_path = "article_data.json"
with open(output_file_path, "w") as json_file:
    json.dump(articles_json_list, json_file, indent=2)

print(f"Generated articles saved to {output_file_path}")


# import json
# import hashlib
# from faker import Faker

# fake = Faker()


# def generate_password_hash(password, salt_length=32):
#     salt = fake.binary(length=salt_length)
#     password_hash = hashlib.pbkdf2_hmac(
#         "sha256", password.encode("utf-8"), salt, 100000
#     )
#     return {
#         "salt": salt.hex(),
#         "password_hash": password_hash.hex(),
#     }


# def generate_fake_user():
#     plain_password = fake.password()  # Using Faker's password generator
#     password_data = generate_password_hash(plain_password)

#     return {
#         "email": fake.email(),
#         "first_name": fake.first_name(),
#         "last_name": fake.last_name(),
#         "is_staff": fake.boolean(),
#         "is_active": fake.boolean(),
#         "date_joined": str(fake.date_time_this_decade()),
#         "password_salt": password_data["salt"],
#         "password_hash": password_data["password_hash"],
#     }


# def generate_n_users_json(n):
#     users_json_data = [generate_fake_user() for _ in range(n)]
#     return users_json_data


# # Example usage to generate 5 users
# n = 100
# users_json_list = generate_n_users_json(n)

# # Save the data to a JSON file
# output_file_path = "generated_users.json"
# with open(output_file_path, "w") as json_file:
#     json.dump(users_json_list, json_file, indent=2)

# print(f"Generated users saved to {output_file_path}")

""" 
def generate_fake_user():
    plain_password = secrets.token_hex(
        8
    )  # Generate a random 8-character hexadecimal string
    return {
        "model": "users.CustomUser",
        "pk": str(secrets.randbelow(1000) + 1),
        "fields": {
            "email": f"{plain_password.lower()}@example.com",  # Using part of the password for a fake email
            "first_name": "John",
            "last_name": "Doe",
            "is_staff": False,
            "is_active": True,
            "date_joined": "2022-01-01T00:00:00Z",
            "password": plain_password,
        },
    }


def generate_n_users_json(n):
    users_json_data = [generate_fake_user() for _ in range(n)]
    return users_json_data


# Example usage to generate 5 users
n = 2
users_json_list = generate_n_users_json(n)

# Save the data to a JSON file
output_file_path = "./blog/fixtures/users_data.json"
with open(output_file_path, "w") as json_file:
    json.dump(users_json_list, json_file, indent=2)

print(f"Generated users saved to {output_file_path}")
 """

import secrets
import base64


def generate_url_safe_string(length):
    # Generate a random byte string using secrets
    random_bytes = secrets.token_bytes(length)

    # Encode the byte string using base64
    base64_encoded = base64.urlsafe_b64encode(random_bytes)

    # Convert the bytes to a string and remove padding
    url_safe_string = base64_encoded.decode("utf-8").rstrip("=")

    return url_safe_string


print(generate_url_safe_string(40))
