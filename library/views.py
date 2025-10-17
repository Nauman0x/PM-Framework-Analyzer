from django.shortcuts import render, get_object_or_404
from .models import Book, Page
from django.db.models import Q
from django.conf import settings
from django.core.files.storage import default_storage
import os
import pdfplumber
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
import re
from .models import Section
from google import genai


def format_markdown_to_html(text):
    """Convert markdown to HTML with proper formatting and no extra spaces"""
    if not text:
        return ""
    
    # Remove excessive blank lines first
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Process lines
    lines = text.split('\n')
    formatted_lines = []
    in_ul = False
    in_ol = False
    
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines but close lists if needed
        if not stripped:
            if in_ul:
                formatted_lines.append('</ul>')
                in_ul = False
            if in_ol:
                formatted_lines.append('</ol>')
                in_ol = False
            formatted_lines.append('<br>')
            continue
        
        # Convert ## headers to h2
        if stripped.startswith('## '):
            if in_ul:
                formatted_lines.append('</ul>')
                in_ul = False
            if in_ol:
                formatted_lines.append('</ol>')
                in_ol = False
            content = stripped[3:].strip()
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            formatted_lines.append(f'<h2>{content}</h2>')
            continue
        
        # Convert ### headers to h3
        elif stripped.startswith('### '):
            if in_ul:
                formatted_lines.append('</ul>')
                in_ul = False
            if in_ol:
                formatted_lines.append('</ol>')
                in_ol = False
            content = stripped[4:].strip()
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            formatted_lines.append(f'<h3>{content}</h3>')
            continue
        
        # Convert #### headers to h4
        elif stripped.startswith('#### '):
            if in_ul:
                formatted_lines.append('</ul>')
                in_ul = False
            if in_ol:
                formatted_lines.append('</ol>')
                in_ol = False
            content = stripped[5:].strip()
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            formatted_lines.append(f'<h4>{content}</h4>')
            continue
        
        # Handle bullet points with * or -
        elif stripped.startswith('* ') or stripped.startswith('- '):
            if in_ol:
                formatted_lines.append('</ol>')
                in_ol = False
            if not in_ul:
                formatted_lines.append('<ul>')
                in_ul = True
            content = stripped[2:].strip()
            # Convert inline bold and italic
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
            formatted_lines.append(f'<li>{content}</li>')
            continue
        
        # Handle numbered lists
        elif re.match(r'^\d+\.\s+', stripped):
            if in_ul:
                formatted_lines.append('</ul>')
                in_ul = False
            if not in_ol:
                formatted_lines.append('<ol>')
                in_ol = True
            content = re.sub(r'^\d+\.\s+', '', stripped).strip()
            # Convert inline bold and italic
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
            formatted_lines.append(f'<li>{content}</li>')
            continue
        
        # Regular paragraph
        else:
            if in_ul:
                formatted_lines.append('</ul>')
                in_ul = False
            if in_ol:
                formatted_lines.append('</ol>')
                in_ol = False
            
            # Convert inline bold and italic
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', stripped)
            content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
            formatted_lines.append(f'<p>{content}</p>')
    
    # Close any open lists
    if in_ul:
        formatted_lines.append('</ul>')
    if in_ol:
        formatted_lines.append('</ol>')
    
    return '\n'.join(formatted_lines)


from .models import Section

def index(request):
    books = Book.objects.all()
    return render(request, 'library/index.html', {'books': books})


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    
    # Get all sections
    all_sections = list(book.sections.all())
    
    # Custom sort: STANDARD sections (starting with 'S') before GUIDE sections (starting with 'G')
    # For PMBOK: We want S1, S1.1, ..., S3.12, then G1, G1.1, ..., GX5.6
    def section_sort_key(section):
        num = section.section_number
        # Put S sections before G sections by prefixing with '0' for S and '1' for G
        if num.startswith('S'):
            return '0' + num[1:]  # S1 -> 01, S1.1 -> 01.1
        elif num.startswith('G'):
            return '1' + num[1:]  # G1 -> 11, G1.1 -> 11.1
        else:
            return '2' + num  # Other sections come last
    
    sections = sorted(all_sections, key=section_sort_key)
    
    return render(request, 'library/book_detail.html', {'book': book, 'sections': sections})


def search_topics(request):
    """Search for sections/topics across all books"""
    query = request.GET.get('q', '').strip()
    results_by_book = {}
    
    if query:
        # Search in section titles across all books
        sections = Section.objects.filter(
            Q(title__icontains=query) | Q(section_number__icontains=query)
        ).select_related('book').order_by('book__title', 'start_page')
        
        # Group results by book
        for section in sections:
            book_title = section.book.title
            if book_title not in results_by_book:
                results_by_book[book_title] = {
                    'book': section.book,
                    'sections': []
                }
            results_by_book[book_title]['sections'].append(section)
    
    return render(request, 'library/search_results.html', {
        'query': query, 
        'results_by_book': results_by_book
    })


def compare_topic(request):
    """Compare view with recommended topics"""
    # Get some recommended topics from different books
    recommended_sections = Section.objects.filter(
        Q(title__icontains='project') | 
        Q(title__icontains='risk') | 
        Q(title__icontains='stakeholder') |
        Q(title__icontains='scope') |
        Q(title__icontains='quality') |
        Q(title__icontains='planning')
    ).select_related('book').order_by('book__title', 'start_page').distinct()
    
    # Group by book
    recommended_by_book = {}
    for section in recommended_sections:
        book_title = section.book.title
        if book_title not in recommended_by_book:
            recommended_by_book[book_title] = {
                'book': section.book,
                'sections': []
            }
        if len(recommended_by_book[book_title]['sections']) < 6:  # Limit per book
            recommended_by_book[book_title]['sections'].append(section)
    
    return render(request, 'library/compare.html', {
        'recommended_by_book': recommended_by_book
    })


def upload_pdf(request):
    if request.method == 'POST' and request.FILES.get('pdf'):
        f = request.FILES['pdf']
        # save to media
        save_path = os.path.join(settings.MEDIA_ROOT, f.name)
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        with open(save_path, 'wb') as out:
            for chunk in f.chunks():
                out.write(chunk)


        # create Book entry and import pages with section detection
        title = os.path.splitext(f.name)[0]
        book, created = Book.objects.get_or_create(title=title, file_path=save_path)
        with pdfplumber.open(save_path) as pdf:
            total_pages = len(pdf.pages)
            outlines = []
            try:
                outlines = pdf.outlines or []
            except Exception:
                outlines = []

            sections = []
            if outlines:
                def flatten(outlist, level=1):
                    res = []
                    for item in outlist:
                        if isinstance(item, dict) and 'title' in item:
                            title = item.get('title')
                            try:
                                pnum = item.get('page_number') or item.get('page') or None
                            except Exception:
                                pnum = None
                            res.append((title, pnum, level))
                            if item.get('children'):
                                res.extend(flatten(item.get('children'), level+1))
                    return res
                entries = flatten(outlines)
                for title2, pnum, level in entries:
                    if pnum:
                        sections.append({'title': title2, 'start_page': int(pnum), 'level': level})

            if not sections:
                header_re = re.compile(r'^(\d+(?:\.\d+){0,5})?\s*([A-Z][\w\-\s\/:]{3,200})$')
                for i, page in enumerate(pdf.pages, start=1):
                    try:
                        raw = page.extract_text() or ''
                    except Exception:
                        raw = ''
                    lines = [l.strip() for l in raw.splitlines() if l.strip()][:10]
                    for ln in lines:
                        if len(ln) < 120 and (ln.isupper() or ln[0].isdigit() or len(ln.split()) <= 8):
                            m = header_re.match(ln)
                            if m:
                                secnum = m.group(1)
                                t = m.group(2).strip()
                            else:
                                secnum = None
                                t = ln
                            sections.append({'title': t, 'start_page': i, 'level': 1, 'section_number': secnum})
                            break

            sections = sorted(sections, key=lambda s: s['start_page'])
            created_sections = []
            for idx, s in enumerate(sections):
                start = s['start_page']
                end = sections[idx+1]['start_page'] - 1 if idx + 1 < len(sections) else total_pages
                sec = Section.objects.create(
                    book=book,
                    title=s.get('title')[:1024],
                    section_number=s.get('section_number') or '',
                    level=s.get('level', 1),
                    start_page=start,
                    end_page=end
                )
                created_sections.append(sec)

            for i, page in enumerate(pdf.pages, start=1):
                try:
                    raw = page.extract_text() or ''
                except Exception:
                    raw = ''
                text = re.sub(r'\s+', ' ', raw).strip()
                assigned = None
                for sec in created_sections:
                    if sec.start_page <= i <= (sec.end_page or sec.start_page):
                        assigned = sec
                        break
                Page.objects.update_or_create(book=book, page_number=i, defaults={'text': text, 'section': assigned, 'topic': (assigned.title if assigned else '')[:256]})

        return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('index'))


def section_detail(request, section_id):
    section = get_object_or_404(Section, pk=section_id)
    
    # Get all sections for this book in order
    all_sections = list(section.book.sections.all().order_by('start_page', 'id'))
    current_index = all_sections.index(section)
    
    # Get previous and next sections
    prev_section = all_sections[current_index - 1] if current_index > 0 else None
    next_section = all_sections[current_index + 1] if current_index < len(all_sections) - 1 else None
    
    return render(request, 'library/section_detail.html', {
        'section': section,
        'prev_section': prev_section,
        'next_section': next_section
    })


def format_analysis_markdown_to_html(text):
    """Convert markdown to HTML matching the book detail page style"""
    import re
    
    # Normalize line breaks and remove excessive whitespace
    text = text.strip()
    
    # Mark main headings (## SIMILARITIES, ## DIFFERENCES, etc.) with a special class
    text = re.sub(r'(?:^|\n)## (SIMILARITIES|DIFFERENCES|UNIQUE POINTS?|COMPARATIVE ANALYSIS)', 
                  r'\n<strong class="main-heading">\1</strong>\n', text, flags=re.IGNORECASE)
    
    # Convert remaining ## headers to regular strong tags (sub-headings)
    text = re.sub(r'(?:^|\n)## (.+)', r'\n<strong>\1</strong>\n', text)
    
    # Convert ### headers to regular strong tags (sub-headings)
    text = re.sub(r'(?:^|\n)### (.+)', r'\n<strong>\1</strong>\n', text)
    
    # Convert **bold** at start of line to strong tags (headings)
    text = re.sub(r'(?:^|\n)\*\*(.+?)\*\*(?=\s*\n)', r'\n<strong>\1</strong>\n', text)
    
    # Convert remaining **bold** (inline) to HTML
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # Convert *italic* to HTML
    text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', text)
    
    # Remove ALL excessive blank lines - replace 2+ newlines with just 1
    text = re.sub(r'\n{2,}', '\n', text)
    
    # Add single line break after headings
    text = re.sub(r'(</strong>)\n', r'\1\n', text)
    
    return text.strip()


def analyze_topics(request):
    """Loading page before actual analysis"""
    query = request.GET.get('q', '').strip()
    from_page = request.GET.get('from', 'compare')
    
    if not query:
        return render(request, 'library/analysis.html', {
            'query': '',
            'error': 'Please provide a search term to analyze topics.'
        })
    
    # Show loading page
    return render(request, 'library/analysis_loading.html', {
        'query': query,
        'from_page': from_page
    })


def analyze_topics_process(request):
    """AI analysis of topics across books using Gemini - actual processing"""
    query = request.GET.get('q', '').strip()
    from_page = request.GET.get('from', 'compare')
    
    if not query:
        return render(request, 'library/analysis.html', {
            'query': '',
            'error': 'Please provide a search term to analyze topics.'
        })
    
    # Search for sections matching the query
    sections = Section.objects.filter(
        Q(title__icontains=query) | Q(section_number__icontains=query)
    ).select_related('book').order_by('book__title', 'start_page')
    
    if not sections:
        return render(request, 'library/analysis.html', {
            'query': query,
            'from_page': from_page,
            'error': 'No topics found matching your query.'
        })
    
    # Group sections by book
    sections_by_book = {}
    for section in sections:
        book_title = section.book.title
        if book_title not in sections_by_book:
            sections_by_book[book_title] = []
        sections_by_book[book_title].append(section)
    
    # Prepare content for AI analysis with references
    analysis_content = f"Analyze the following topics related to '{query}' from different project management standards. "
    analysis_content += "Always reference specific sections, page numbers, and book titles when making comparisons.\n\n"
    
    for book_title, book_sections in sections_by_book.items():
        analysis_content += f"\n{'='*80}\n"
        analysis_content += f"BOOK: {book_title}\n"
        analysis_content += f"{'='*80}\n"
        for section in book_sections[:5]:  # Limit to 5 sections per book
            analysis_content += f"\n[Section: {section.section_number}] {section.title}\n"
            analysis_content += f"[Pages: {section.start_page}"
            if section.end_page and section.end_page != section.start_page:
                analysis_content += f"-{section.end_page}"
            analysis_content += "]\n"
            if section.content:
                # Limit content to first 1500 characters per section
                content_preview = section.content[:1500].strip()
                if len(section.content) > 1500:
                    content_preview += "..."
                analysis_content += f"\nContent:\n{content_preview}\n"
            analysis_content += "\n" + ("-"*80) + "\n"
    
    analysis_content += f"\n\n{'='*80}\n"
    analysis_content += "ANALYSIS REQUIREMENTS:\n"
    analysis_content += f"{'='*80}\n\n"
    analysis_content += "Provide a comprehensive comparative analysis with the following structure:\n\n"
    
    analysis_content += "## SIMILARITIES\n"
    analysis_content += "Focus on:\n"
    analysis_content += "- Common practices shared across standards\n"
    analysis_content += "- Overlapping guidance and recommendations\n"
    analysis_content += "- Similar frameworks, processes, or methodologies\n"
    analysis_content += "- Shared principles and best practices\n"
    analysis_content += "Use ### for sub-headings under SIMILARITIES.\n"
    analysis_content += "Always cite specific sections and page numbers when making points.\n\n"
    
    analysis_content += "## DIFFERENCES\n"
    analysis_content += "Focus on:\n"
    analysis_content += "- Unique terminologies used by each standard\n"
    analysis_content += "- Different methodologies and approaches\n"
    analysis_content += "- Varying levels of detail or emphasis\n"
    analysis_content += "- Contrasting perspectives on implementation\n"
    analysis_content += "- Different organizational frameworks\n"
    analysis_content += "Use ### for sub-headings under DIFFERENCES.\n"
    analysis_content += "Provide specific examples with section references and page numbers.\n\n"
    
    analysis_content += "## UNIQUE POINTS\n"
    analysis_content += "Focus on:\n"
    analysis_content += "- What only one specific standard covers\n"
    analysis_content += "- Exclusive tools, techniques, or concepts\n"
    analysis_content += "- Specialized guidance not found in other standards\n"
    analysis_content += "- Distinctive features of each framework\n"
    analysis_content += "Clearly state which standard provides each unique point.\n"
    analysis_content += "Use ### for sub-headings under UNIQUE POINTS.\n"
    analysis_content += "Reference specific sections and their page numbers.\n\n"
    
    analysis_content += "FORMATTING RULES:\n"
    analysis_content += "1. Use ## for main sections (SIMILARITIES, DIFFERENCES, UNIQUE POINTS)\n"
    analysis_content += "2. Use ### for sub-headings within each section\n"
    analysis_content += "3. Keep paragraphs concise and well-spaced\n"
    analysis_content += "4. Avoid excessive blank lines\n"
    analysis_content += "5. Always reference: [Book Title, Section X.X, Page XX]\n"
    analysis_content += "6. For UNIQUE POINTS, explicitly state which standard it's from\n\n"
    analysis_content += "IMPORTANT: Always reference the specific book title, section number, and page number(s) when citing content."
    
    try:
        # Initialize Gemini client
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        # Generate analysis
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=analysis_content,
        )
        
        analysis_text = response.text
        # Format markdown to HTML
        analysis_text = format_analysis_markdown_to_html(analysis_text)
        
    except Exception as e:
        analysis_text = f"<p>Error generating analysis: {str(e)}</p>"
    
    return render(request, 'library/analysis.html', {
        'query': query,
        'from_page': from_page,
        'analysis': analysis_text,
        'sections_by_book': sections_by_book,
        'total_books': len(sections_by_book),
        'total_sections': len(sections)
    })


# Phase 2: Process Design & Tailoring Views
from .models import ProjectScenario, ProcessTemplate, ProcessPhase

def scenarios_list(request):
    """Display all project scenarios"""
    scenarios = ProjectScenario.objects.all().order_by('scenario_type')
    return render(request, 'library/scenarios_list.html', {
        'scenarios': scenarios
    })


def scenario_detail(request, scenario_id):
    """Display detailed view of a scenario and its process templates"""
    scenario = get_object_or_404(ProjectScenario, id=scenario_id)
    templates = ProcessTemplate.objects.filter(scenario=scenario).prefetch_related(
        'phases__activities__deliverables',
        'phases__decision_gates'
    )
    
    return render(request, 'library/scenario_detail.html', {
        'scenario': scenario,
        'templates': templates
    })


def process_template_detail(request, template_id):
    """Display detailed process template with phases, activities, and deliverables"""
    template = get_object_or_404(
        ProcessTemplate.objects.prefetch_related(
            'phases__activities__deliverables',
            'phases__activities__roles',
            'phases__decision_gates',
            'standard_references__book',
            'standard_references__section'
        ),
        id=template_id
    )
    
    # Organize data by phases
    phases_data = []
    for phase in template.phases.all().order_by('order'):
        activities = phase.activities.all().order_by('order')
        decision_gates = phase.decision_gates.all().order_by('order')
        phases_data.append({
            'phase': phase,
            'activities': activities,
            'decision_gates': decision_gates
        })
    
    return render(request, 'library/process_template_detail.html', {
        'template': template,
        'phases_data': phases_data,
        'standard_references': template.standard_references.all()
    })


def generate_process(request, scenario_id):
    """AI-powered process generation for a scenario"""
    scenario = get_object_or_404(ProjectScenario, id=scenario_id)
    
    if request.method == 'POST':
        # Show loading page
        return render(request, 'library/process_generating.html', {
            'scenario': scenario
        })
    
    return HttpResponseRedirect(reverse('scenario_detail', args=[scenario_id]))


def generate_process_ai(request, scenario_id):
    """AI endpoint to generate process template"""
    scenario = get_object_or_404(ProjectScenario, id=scenario_id)
    
    # Get all available standards for reference
    books = Book.objects.all()
    
    # Create focused AI prompt
    prompt = f"""Design a tailored project management process for this scenario. Be CONCISE and SPECIFIC.

SCENARIO: {scenario.name}
Type: {scenario.scenario_type}
Context: {scenario.context}
Duration: {scenario.duration} | Team: {scenario.team_size}

STANDARDS AVAILABLE:
{chr(10).join([f'- {book.title}' for book in books])}

REQUIREMENTS:
1. Keep each section brief and actionable
2. Cite specific PM standards with page numbers where applicable
3. Focus on what's essential for THIS scenario
4. Use clear structure without unnecessary elaboration

OUTPUT FORMAT:

## Process Name
[One concise sentence describing the process]

## Approach
[2-3 sentences max on methodology and why it fits this scenario]

## Phases
For each phase (4-5 phases total):
### [Phase Name] (Duration)
- Objective: [One sentence]
- Key Activities: [List 2-3 critical activities only]
- Deliverables: [List 2-3 main outputs]
- Decision Gate: [Name and criteria in one line]
- Reference: [Standard name, page number if available]

## Critical Roles
[List only essential roles with one-line responsibility each]

## Tailoring Rationale
[3-4 bullet points explaining key adaptations from standards for this specific scenario]

IMPORTANT:
- No extra asterisks or formatting symbols
- Each bullet point should be ONE clear line
- Cite actual page numbers from standards when referencing (e.g., "PMBOK p.123")
- Keep total output under 500 words
- Focus on scenario-specific adaptations, not generic PM theory"""

    try:
        # Initialize Gemini client
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        # Generate response
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt
        )
        
        # Get the generated text
        generated_text = response.text
        
        # Format for HTML display
        formatted_html = format_markdown_to_html(generated_text)
        
        # Save to scenario
        from django.utils import timezone
        scenario.process_design = formatted_html
        scenario.generated_at = timezone.now()
        scenario.save()
        
        return JsonResponse({
            'success': True,
            'process_design': formatted_html,
            'raw_text': generated_text
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


def process_diagram(request, template_id):
    """Generate visual process diagram"""
    template = get_object_or_404(
        ProcessTemplate.objects.prefetch_related(
            'phases__activities__deliverables',
            'phases__decision_gates'
        ),
        id=template_id
    )
    
    # Generate Mermaid diagram syntax
    mermaid_diagram = generate_mermaid_diagram(template)
    
    return render(request, 'library/process_diagram.html', {
        'template': template,
        'mermaid_diagram': mermaid_diagram
    })


def generate_mermaid_diagram(template):
    """Generate Mermaid.js flowchart syntax for the process"""
    lines = ["graph TD"]
    lines.append(f"    START([Start: {template.name}])")
    
    prev_node = "START"
    phases = template.phases.all().order_by('order')
    
    for i, phase in enumerate(phases):
        phase_id = f"PHASE{i+1}"
        lines.append(f"    {phase_id}[{phase.name}]")
        lines.append(f"    {prev_node} --> {phase_id}")
        
        # Add activities within phase as subgraph
        activities = phase.activities.all().order_by('order')
        if activities:
            lines.append(f"    subgraph {phase.name}")
            for j, activity in enumerate(activities):
                act_id = f"ACT{i+1}_{j+1}"
                lines.append(f"        {act_id}[{activity.name}]")
            lines.append(f"    end")
        
        # Add decision gate if exists
        decision_gates = phase.decision_gates.all()
        if decision_gates:
            for k, gate in enumerate(decision_gates):
                gate_id = f"GATE{i+1}_{k+1}"
                lines.append(f"    {gate_id}{{{gate.name}}}")
                lines.append(f"    {phase_id} --> {gate_id}")
                prev_node = gate_id
        else:
            prev_node = phase_id
    
    lines.append(f"    END([Project Complete])")
    lines.append(f"    {prev_node} --> END")
    
    return "\n".join(lines)
