from django.core.management.base import BaseCommand
from library.models import ProjectScenario

class Command(BaseCommand):
    help = 'Initialize the three project scenarios for Phase 2'

    def handle(self, *args, **options):
        self.stdout.write('Creating project scenarios...')
        
        # Scenario 1: Custom Software Development
        software, created = ProjectScenario.objects.update_or_create(
            scenario_type='software',
            defaults={
                'name': 'Custom Software Development Project',
                'description': 'A focused software development project with clear requirements and agile delivery.',
                'context': 'Well-defined requirements, less than 6 months duration, team of fewer than 7 members. Fast-paced delivery environment requiring flexibility and rapid iteration.',
                'duration': 'Less than 6 months',
                'team_size': 'Fewer than 7 members',
                'complexity': 'low',
                'key_characteristics': '''- Clear, well-defined requirements
- Short timeline (< 6 months)
- Small, cross-functional team
- Need for speed and flexibility
- Frequent delivery cycles
- Direct client collaboration
- Minimal formal documentation
- Iterative and incremental approach'''
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created: {software.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'⟳ Updated: {software.name}'))
        
        # Scenario 2: Innovative Product Development
        innovation, created = ProjectScenario.objects.update_or_create(
            scenario_type='innovation',
            defaults={
                'name': 'Innovative Product Development Project',
                'description': 'An R&D-heavy product development initiative with high uncertainty and innovation focus.',
                'context': 'Research and development intensive project with uncertain outcomes, approximately 1 year duration. Requires balancing innovation, experimentation, and stakeholder management.',
                'duration': 'Approximately 1 year',
                'team_size': '10-15 members (cross-functional)',
                'complexity': 'medium',
                'key_characteristics': '''- High degree of uncertainty
- R&D and experimentation required
- Unclear final outcomes
- Need for prototyping and iteration
- Multiple stakeholder groups
- Balance innovation with deadlines
- Adaptive and learning-oriented
- Potential for scope changes
- Market research integration'''
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created: {innovation.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'⟳ Updated: {innovation.name}'))
        
        # Scenario 3: Large Government Project
        government, created = ProjectScenario.objects.update_or_create(
            scenario_type='government',
            defaults={
                'name': 'Large Government Infrastructure Project',
                'description': 'A comprehensive government project involving civil, electrical, and IT components with strict governance.',
                'context': 'Multi-disciplinary project with civil, electrical, and IT components over 2-year duration. Requires comprehensive governance, compliance, procurement management, risk management, and formal reporting.',
                'duration': '2 years',
                'team_size': '50+ members (multiple teams)',
                'complexity': 'high',
                'key_characteristics': '''- Multiple technical disciplines (Civil, Electrical, IT)
- Long duration (2 years)
- Large, distributed team
- Strict governance and compliance requirements
- Complex procurement processes
- Formal risk management
- Extensive documentation required
- Multiple approval levels
- Public accountability
- Regulatory compliance
- Budget oversight
- Progress reporting to authorities'''
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created: {government.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'⟳ Updated: {government.name}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ All project scenarios initialized!'))
        self.stdout.write(f'\nTotal scenarios in database: {ProjectScenario.objects.count()}')
