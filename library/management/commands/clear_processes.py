from django.core.management.base import BaseCommand
from library.models import ProjectScenario

class Command(BaseCommand):
    help = 'Clear all generated process designs to allow regeneration with new formatting'

    def handle(self, *args, **options):
        self.stdout.write('Clearing generated process designs...')
        
        # Clear process_design field from all scenarios
        updated = ProjectScenario.objects.update(
            process_design='',
            justification='',
            referenced_standards='',
            generated_at=None
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Cleared process designs from {updated} scenarios'))
        self.stdout.write(self.style.SUCCESS('You can now regenerate processes with improved formatting!'))
