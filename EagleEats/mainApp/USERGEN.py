import random
from mainApp.models import Profile 
from django.contrib.auth.models import User
users = [
    {"first_name": "Bill", "last_name": "Clark", "points": 31483},
    {"first_name": "Alice", "last_name": "Chen", "points": 30322},
    {"first_name": "Robert", "last_name": "Smith", "points": 29412},
    {"first_name": "Johnny", "last_name": "Block", "points": 28453},
    {"first_name": "Trevor", "last_name": "White", "points": 26432},
    {"first_name": "Erica", "last_name": "Park", "points": 26422},
    {"first_name": "Dorris", "last_name": "Will", "points": 25532},
    {"first_name": "Maria", "last_name": "Stark", "points": 25452},
    {"first_name": "Mary", "last_name": "Huel", "points": 25250},
    {"first_name": "Aisha", "last_name": "Wunsch", "points": 25159},
    {"first_name": "Bernie", "last_name": "Wunsch", "points": 25022},
    {"first_name": "Sedrick", "last_name": "Grady", "points": 24449},
    {"first_name": "Bessie", "last_name": "Hills", "points": 23432},
    {"first_name": "Ebony", "last_name": "Abshire", "points": 22432},
    {"first_name": "Chester", "last_name": "Weissnat", "points": 17232},
    {"first_name": "Ally", "last_name": "Herzog", "points": 15431},
    {"first_name": "Anika", "last_name": "Roberts", "points": 15422},
    {"first_name": "Tessie", "last_name": "White", "points": 12732},
    {"first_name": "Carolanne", "last_name": "Jones", "points": 12435}
]
def create_user_instance(first_name, last_name, email):
    username = f"{first_name.lower()}.{last_name.lower()}"
    user = User.objects.get_or_create(
        username=username,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
    )
    return user

for user_data in users:
    first_name = user_data['first_name']
    last_name = user_data['last_name']
    points = user_data['points']
    email = f"{first_name.lower()}.{last_name.lower()}@bc.com"
    user_instance = create_user_instance(first_name, last_name, email)
    major = random.choice(['Computer Science', 'Biology', 'Business', 'Physics', 'Mathematics'])
    school = random.choice(['School of Arts', 'School of Science', 'School of Business'])
    graduation_year = random.randint(2024, 2028)
    eagle_id = f"{random.randint(100000, 999999)}"
    group_id = random.randint(1, 10)
    user_type = random.choice(['student', 'mod', 'admin'])
    profile, created = Profile.objects.get_or_create(
        user=user_instance,
        defaults={
            'major': major,
            'school': school,
            'graduation_year': graduation_year,
            'eagle_id': eagle_id,
            'user_type': user_type,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'group_id': group_id,
            'lifetime_points': points,
            'current_points': points
        }
    )
    if created:
        print(f"Profile created for {first_name} {last_name}")
    else:
        print(f"Profile already exists for {first_name} {last_name}")
