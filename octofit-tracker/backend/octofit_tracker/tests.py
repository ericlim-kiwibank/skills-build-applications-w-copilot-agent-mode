from django.test import TestCase
from .models import User, Team, Activity, Workout, Leaderboard

class ModelSmokeTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass', team=self.team)
        self.activity = Activity.objects.create(user=self.user, description='Test Activity', duration=30)
        self.workout = Workout.objects.create(user=self.user, name='Test Workout', type='Cardio', duration=45)
        self.leaderboard = Leaderboard.objects.create(team=self.team, points=100)

    def test_team(self):
        self.assertEqual(self.team.name, 'Test Team')
    def test_user(self):
        self.assertEqual(self.user.email, 'test@example.com')
    def test_activity(self):
        self.assertEqual(self.activity.description, 'Test Activity')
    def test_workout(self):
        self.assertEqual(self.workout.name, 'Test Workout')
    def test_leaderboard(self):
        self.assertEqual(self.leaderboard.points, 100)
