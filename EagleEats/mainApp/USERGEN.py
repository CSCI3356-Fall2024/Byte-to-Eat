# delete db.sqlite3, delete all files in migration under mainApp other than pycache and __init__ copy code below, on a terminal run python manage.py shell, paste code below to generate test users
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
    {"first_name": "Carolanne", "last_name": "Jones", "points": 12435},
    {"first_name": "James", "last_name": "Brown", "points": 12000},
    {"first_name": "Linda", "last_name": "Johnson", "points": 11800},
    {"first_name": "Michael", "last_name": "Williams", "points": 11500},
    {"first_name": "Patricia", "last_name": "Jones", "points": 11300},
    {"first_name": "Jennifer", "last_name": "Garcia", "points": 11000},
    {"first_name": "Charles", "last_name": "Martinez", "points": 10800},
    {"first_name": "Barbara", "last_name": "Rodriguez", "points": 10600},
    {"first_name": "Susan", "last_name": "Hernandez", "points": 10400},
    {"first_name": "Joseph", "last_name": "Lopez", "points": 10200},
    {"first_name": "Thomas", "last_name": "Gonzalez", "points": 10000},
    {"first_name": "Sarah", "last_name": "Wilson", "points": 9800},
    {"first_name": "Karen", "last_name": "Anderson", "points": 9600},
    {"first_name": "Nancy", "last_name": "Thomas", "points": 9400},
    {"first_name": "Lisa", "last_name": "Taylor", "points": 9200},
    {"first_name": "Betty", "last_name": "Moore", "points": 9000},
    {"first_name": "Margaret", "last_name": "Jackson", "points": 8800},
    {"first_name": "Sandra", "last_name": "Martin", "points": 8600},
    {"first_name": "Ashley", "last_name": "Lee", "points": 8400},
    {"first_name": "Kimberly", "last_name": "Perez", "points": 8200},
    {"first_name": "Emily", "last_name": "Thompson", "points": 8000},
    {"first_name": "Donna", "last_name": "White", "points": 7800},
    {"first_name": "Jessica", "last_name": "Harris", "points": 7600},
    {"first_name": "Dorothy", "last_name": "Sanchez", "points": 7400},
    {"first_name": "Amanda", "last_name": "Clark", "points": 7200},
    {"first_name": "Melissa", "last_name": "Ramirez", "points": 7000},
    {"first_name": "Deborah", "last_name": "Lewis", "points": 6800},
    {"first_name": "Stephanie", "last_name": "Robinson", "points": 6600},
    {"first_name": "Rebecca", "last_name": "Walker", "points": 6400},
    {"first_name": "Sharon", "last_name": "Young", "points": 6200},
    {"first_name": "Laura", "last_name": "Allen", "points": 6000},
    {"first_name": "Cynthia", "last_name": "King", "points": 5800},
    {"first_name": "Kathleen", "last_name": "Wright", "points": 5600},
    {"first_name": "Amy", "last_name": "Scott", "points": 5400},
    {"first_name": "Shirley", "last_name": "Torres", "points": 5200},
    {"first_name": "Angela", "last_name": "Nguyen", "points": 5000},
    {"first_name": "Helen", "last_name": "Hill", "points": 4800},
    {"first_name": "Anna", "last_name": "Flores", "points": 4600},
    {"first_name": "Brenda", "last_name": "Green", "points": 4400},
    {"first_name": "Pamela", "last_name": "Adams", "points": 4200},
    {"first_name": "Nicole", "last_name": "Nelson", "points": 4000},
    {"first_name": "Samantha", "last_name": "Baker", "points": 3800},
    {"first_name": "Katherine", "last_name": "Hall", "points": 3600},
    {"first_name": "Christine", "last_name": "Rivera", "points": 3400},
    {"first_name": "Debra", "last_name": "Campbell", "points": 3200},
    {"first_name": "Rachel", "last_name": "Mitchell", "points": 3000},
    {"first_name": "Carol", "last_name": "Carter", "points": 2800},
    {"first_name": "Janet", "last_name": "Roberts", "points": 2600},
    {"first_name": "Catherine", "last_name": "Phillips", "points": 2400},
    {"first_name": "Maria", "last_name": "Evans", "points": 2200},
    {"first_name": "Heather", "last_name": "Turner", "points": 2000},
    {"first_name": "Diane", "last_name": "Parker", "points": 1800},
    {"first_name": "Ruth", "last_name": "Collins", "points": 1600},
    {"first_name": "Julie", "last_name": "Edwards", "points": 1400},
    {"first_name": "Olivia", "last_name": "Stewart", "points": 1200},
    {"first_name": "Joyce", "last_name": "Morris", "points": 1000},
    {"first_name": "Virginia", "last_name": "Rogers", "points": 800},
    {"first_name": "Victoria", "last_name": "Reed", "points": 600},
    {"first_name": "Lauren", "last_name": "Cook", "points": 400},
    {"first_name": "Martha", "last_name": "Morgan", "points": 200}
]

def create_user_instance(first_name, last_name, email):
    username = f"{first_name.lower()}.{last_name.lower()}"
    user, created = User.objects.get_or_create(
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
    user_type = "student"
    profile, created = Profile.objects.get_or_create(
        user=user_instance,
        defaults={
            'major': major,
            'school': school,
            'graduation_year': graduation_year,
            'eagle_id': eagle_id,
            'user_type': user_type,
            'email': email,
            'group_id': group_id,
            'lifetime_points': points,
            'current_points': points
        }
    )

for u in Profile.objects.all():
    u.lifetime_points = random.randint(1000, 10000)
    u.current_points = random.randint(u.lifetime_points, u.lifetime_points+10000)
    u.save()
