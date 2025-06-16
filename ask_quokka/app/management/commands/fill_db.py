from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike

import random
import string

class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio for data generation')

    def handle(self, *args, **options):
        User.objects.all().delete()
        Profile.objects.all().delete()
        Question.objects.all().delete()
        Answer.objects.all().delete()
        Tag.objects.all().delete()
        QuestionLike.objects.all().delete()
        AnswerLike.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'All data deleted'))

        ratio = options['ratio']
        num_users = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_tags = ratio
        num_likes = ratio * 200

        self.stdout.write(self.style.SUCCESS(f'Generating {num_users} users...'))
        profiles = []
        for i in range(num_users):
            user = User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='password'
            )
            profile = Profile.objects.create(user=user)
            profiles.append(profile)

        self.stdout.write(self.style.SUCCESS(f'Generating {num_tags} tags...'))
        tags = []
        for i in range(num_tags):
            tag = Tag.objects.create(name=f'tag{i}')
            tags.append(tag)

        self.stdout.write(self.style.SUCCESS(f'Generating {num_questions} questions...'))
        questions = []
        for i in range(num_questions):
            q = Question.objects.create(
                title=f'Question {i}',
                text='Some sample question text here.',
                author=random.choice(profiles)  # ✅ передаётся Profile
            )
            q.tags.set(random.sample(tags, k=min(3, len(tags))))
            questions.append(q)

        self.stdout.write(self.style.SUCCESS(f'Generating {num_answers} answers...'))
        for i in range(num_answers):
            Answer.objects.create(
                text='Answer text ' + str(i),
                author=random.choice(profiles),
                question=random.choice(questions)
            )

        self.stdout.write(self.style.SUCCESS(f'Generating {num_likes} likes...'))
        for _ in range(num_likes):
            try:
                if random.choice([True, False]):
                    q = random.choice(questions)
                    user = random.choice(profiles)
                    QuestionLike.objects.create(question=q, user=user, value=random.choice([1, -1]))
                else:
                    a = Answer.objects.order_by('?').first()
                    user = random.choice(profiles)
                    AnswerLike.objects.create(answer=a, user=user, value=random.choice([1, -1]))
            except:
                pass  # игнорируем дубли likes из-за unique_together

        self.stdout.write(self.style.SUCCESS('Database successfully filled.'))
