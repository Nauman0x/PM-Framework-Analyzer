from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=1024)
    file_path = models.CharField(max_length=2048)

    def __str__(self):
        return self.title


class Page(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='pages')
    page_number = models.IntegerField()
    text = models.TextField()
    topic = models.CharField(max_length=256, blank=True, null=True)
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True, blank=True, related_name='pages')

    class Meta:
        unique_together = ('book', 'page_number')

    def __str__(self):
        return f"{self.book.title} - page {self.page_number}"


class Section(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=1024)
    section_number = models.CharField(max_length=64, blank=True, null=True)
    level = models.IntegerField(default=1)
    start_page = models.IntegerField()
    end_page = models.IntegerField(blank=True, null=True)
    content = models.TextField(blank=True, default='')

    class Meta:
        ordering = ('book', 'start_page')

    def __str__(self):
        num = f"{self.section_number} " if self.section_number else ''
        return f"{self.book.title} - {num}{self.title} ({self.start_page}-{self.end_page or '?'})"


# Phase 2: Process Design Models

class ProjectScenario(models.Model):
    """Predefined project scenarios for process design"""
    SCENARIO_TYPES = [
        ('software', 'Custom Software Development'),
        ('innovation', 'Innovative Product Development'),
        ('government', 'Large Government Project'),
    ]
    
    COMPLEXITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    name = models.CharField(max_length=255)
    scenario_type = models.CharField(max_length=50, choices=SCENARIO_TYPES)
    description = models.TextField()
    context = models.TextField(help_text="Project context and constraints")
    duration = models.CharField(max_length=100)
    team_size = models.CharField(max_length=100)
    complexity = models.CharField(max_length=20, choices=COMPLEXITY_LEVELS, default='medium')
    key_characteristics = models.TextField()
    
    # AI-generated process design fields
    process_design = models.TextField(blank=True, help_text="AI-generated process design")
    justification = models.TextField(blank=True, help_text="Tailoring justification")
    referenced_standards = models.TextField(blank=True, help_text="Referenced PM standards")
    generated_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_scenario_type_display()})"


class ProcessTemplate(models.Model):
    """End-to-end process design for a scenario"""
    scenario = models.ForeignKey(ProjectScenario, on_delete=models.CASCADE, related_name='templates')
    name = models.CharField(max_length=255)
    description = models.TextField()
    justification = models.TextField(help_text="Why this process suits the scenario")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Process: {self.name} for {self.scenario.name}"


class ProcessPhase(models.Model):
    """Phases in a process template"""
    template = models.ForeignKey(ProcessTemplate, on_delete=models.CASCADE, related_name='phases')
    name = models.CharField(max_length=255)
    order = models.IntegerField()
    description = models.TextField()
    objectives = models.TextField()
    duration_estimate = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['template', 'order']
    
    def __str__(self):
        return f"{self.template.name} - Phase {self.order}: {self.name}"


class ProcessActivity(models.Model):
    """Activities within a phase"""
    phase = models.ForeignKey(ProcessPhase, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=255)
    order = models.IntegerField()
    description = models.TextField()
    responsible_role = models.CharField(max_length=255)
    estimated_effort = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['phase', 'order']
        verbose_name_plural = 'Process Activities'
    
    def __str__(self):
        return f"{self.phase.name} - {self.name}"


class ProcessDeliverable(models.Model):
    """Artifacts/deliverables for activities or phases"""
    activity = models.ForeignKey(ProcessActivity, on_delete=models.CASCADE, related_name='deliverables', null=True, blank=True)
    phase = models.ForeignKey(ProcessPhase, on_delete=models.CASCADE, related_name='deliverables', null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    template_available = models.BooleanField(default=False)
    
    def __str__(self):
        parent = self.activity or self.phase
        return f"{parent} - Deliverable: {self.name}"


class ProcessDecisionGate(models.Model):
    """Decision gates between phases"""
    phase = models.ForeignKey(ProcessPhase, on_delete=models.CASCADE, related_name='decision_gates')
    name = models.CharField(max_length=255)
    description = models.TextField()
    criteria = models.TextField(help_text="Go/No-Go criteria")
    approvers = models.CharField(max_length=255, help_text="Roles responsible for approval")
    
    def __str__(self):
        return f"{self.phase.name} - Gate: {self.name}"


class ProcessStandardReference(models.Model):
    """Citations to PM standards used in process design"""
    template = models.ForeignKey(ProcessTemplate, on_delete=models.CASCADE, related_name='standard_references', null=True, blank=True)
    phase = models.ForeignKey(ProcessPhase, on_delete=models.CASCADE, related_name='standard_references', null=True, blank=True)
    activity = models.ForeignKey(ProcessActivity, on_delete=models.CASCADE, related_name='standard_references', null=True, blank=True)
    
    standard = models.ForeignKey(Book, on_delete=models.CASCADE, help_text="Referenced PM standard")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, help_text="Specific section referenced")
    rationale = models.TextField(help_text="Why this standard was referenced")
    tailoring_note = models.TextField(blank=True, help_text="How it was adapted/tailored")
    
    def __str__(self):
        return f"Reference to {self.standard.title} - {self.section.title}"


class ProcessRole(models.Model):
    """Roles defined in a process"""
    template = models.ForeignKey(ProcessTemplate, on_delete=models.CASCADE, related_name='roles')
    name = models.CharField(max_length=255)
    description = models.TextField()
    responsibilities = models.TextField()
    required_skills = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.template.name} - Role: {self.name}"
