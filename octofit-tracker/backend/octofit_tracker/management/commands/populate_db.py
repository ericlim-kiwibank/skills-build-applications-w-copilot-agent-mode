from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from djongo import models

from octofit_tracker import models as octo_models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Delete all data
        User.objects.all().delete()
        octo_models.Team.objects.all().delete()
        octo_models.Activity.objects.all().delete()
        octo_models.Leaderboard.objects.all().delete()
        octo_models.Workout.objects.all().delete()

        # Create Teams
        marvel = octo_models.Team.objects.create(name='Marvel')
        dc = octo_models.Team.objects.create(name='DC')

        # Create Users (Superheroes)
        users = [
            User.objects.create_user(username='ironman', email='ironman@marvel.com', password='password', team=marvel),
            User.objects.create_user(username='captainamerica', email='cap@marvel.com', password='password', team=marvel),
            User.objects.create_user(username='spiderman', email='spiderman@marvel.com', password='password', team=marvel),
            User.objects.create_user(username='batman', email='batman@dc.com', password='password', team=dc),
            User.objects.create_user(username='superman', email='superman@dc.com', password='password', team=dc),
            User.objects.create_user(username='wonderwoman', email='wonderwoman@dc.com', password='password', team=dc),
        ]

        # Create Activities
        for user in users:
            for i in range(3):
                octo_models.Activity.objects.create(user=user, description=f"Activity {i+1} for {user.username}", duration=30+i*10)

        # Create Workouts
        for user in users:
            octo_models.Workout.objects.create(user=user, name=f"Workout for {user.username}", type="Cardio", duration=45)

        # Create Leaderboard
        for team in [marvel, dc]:
            octo_models.Leaderboard.objects.create(team=team, points=100)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))

        # Create unique index on email
        with connection.cursor() as cursor:
            cursor.execute('db.users.createIndex({ "email": 1 }, { unique: true })')
