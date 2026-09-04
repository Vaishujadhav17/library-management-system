from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from accounts.models import UserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(
            username='admin'
        )
        admin.set_password('Demo@12345')
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()

        librarian, created = User.objects.get_or_create(
            username='librarian'
        )
        librarian.set_password('Demo@12345')
        librarian.save()

        UserProfile.objects.update_or_create(
            user=librarian,
            defaults={'role': 'LIBRARIAN'}
        )

        student, created = User.objects.get_or_create(
            username='student'
        )
        student.set_password('Demo@12345')
        student.save()

        UserProfile.objects.update_or_create(
            user=student,
            defaults={'role': 'STUDENT'}
        )

        self.stdout.write(
            self.style.SUCCESS('Demo users created successfully.')
        )