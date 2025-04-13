from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Update existing superusers to have the superadmin role'

    def handle(self, *args, **options):
        superusers = User.objects.filter(is_superuser=True).exclude(role='superadmin')
        count = superusers.count()
        
        if count > 0:
            superusers.update(role='superadmin')
            self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} superusers to have superadmin role'))
        else:
            self.stdout.write(self.style.SUCCESS('No superusers need role updates'))
