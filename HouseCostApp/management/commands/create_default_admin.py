from django.core.management.base import BaseCommand
from HouseCostApp.models import CustomUser

class Command(BaseCommand):
    help = 'Create a superuser with specified email and password'

    def handle(self, *args, **options):
        email = "admin@example.com"
        password = "Admin123"
        user_type = 'admin'
        name='Sample Admin'

        if CustomUser.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'User with email {email} already exists.'))
        else:
            CustomUser.objects.create_superuser(
                email=email,
                name=name,
                password=password,
                user_type=user_type,
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser with email {email}.'))
