from django.core.management.base import BaseCommand
from article.models import Category


class Command(BaseCommand):
    help = 'Populate initial categories'

    def handle(self, *args, **kwargs):
        categories = [
            ('AI', 'Artificial Intelligence and Machine Learning'),
            ('Web Development', 'Web development technologies and frameworks'),
            ('Mobile', 'Mobile app development'),
            ('DevOps', 'DevOps and infrastructure'),
            ('Cloud', 'Cloud computing and services'),
            ('Security', 'Cybersecurity and best practices'),
            ('Data Science', 'Data analysis and visualization'),
            ('Blockchain', 'Blockchain and cryptocurrency'),
            ('IoT', 'Internet of Things'),
            ('Backend', 'Backend development'),
            ('Frontend', 'Frontend development and UI/UX'),
            ('Databases', 'Database design and management'),
            ('Architecture', 'System architecture and design patterns'),
            ('Testing', 'Testing and quality assurance'),
        ]

        created_count = 0
        for name, description in categories:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created category: {name}'))
            else:
                self.stdout.write(f'Category already exists: {name}')

        self.stdout.write(self.style.SUCCESS(f'\nTotal categories created: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'Total categories in database: {Category.objects.count()}'))

