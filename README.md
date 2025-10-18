# PM Framework Analyzer

A Django-based web application for comparing and analyzing project management standards (ISO 21500, ISO 21502, PRINCE2, PMBOK Guide) with AI-powered comparative insights.

## Project Overview

PM Framework Analyzer is a comprehensive tool designed to help project managers, students, and professionals understand and compare different project management methodologies. The application extracts content from industry-standard PDF documents, enables intelligent searching, and provides AI-powered comparative analysis across different frameworks.

## Features

### Core Functionality
- **PDF Content Extraction**: Automatically extracts and indexes content from PM standard PDFs with accurate page mapping
- **Smart Search**: Search topics across all standards with results grouped by book
- **AI-Powered Analysis**: Gemini AI generates comparative analysis showing similarities, differences, and unique points
- **Hierarchical Navigation**: Properly structured table of contents with sections and subsections
- **Page References**: All content includes accurate page number references for easy citation

### User Experience
- **Modern Interface**: Clean, gradient-based design with responsive layout
- **Loading Indicators**: Visual feedback during AI analysis processing
- **Context-Aware Navigation**: Smart back buttons that remember your browsing context
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices

## Technology Stack

### Backend
- Django 4.2.7
- Python 3.9+
- SQLite Database
- pdfplumber 0.10.3

### AI Integration
- Google Gemini API (gemini-2.0-flash-exp)
- google-genai 0.3.0

### Frontend
- HTML5
- CSS3
- Vanilla JavaScript
- Responsive Design

### Deployment
- Vercel (Serverless Functions)
- GitHub (Version Control)
- Git

## Local Development Setup (Windows, PowerShell)

1. Create a virtualenv and install requirements:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. **Set up environment variables** (create `.env` file):

```env
DJANGO_SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
```

<!-- Trigger Vercel redeploy: Oct 18, 2025 -->
DEBUG=True
```

3. **Run migrations**:
```powershell
.\.venv\Scripts\python manage.py migrate
```

4. **Import PDF standards** (optional):
```powershell
.\.venv\Scripts\python manage.py import_iso21500
.\.venv\Scripts\python manage.py import_iso21502
.\.venv\Scripts\python manage.py import_prince2
.\.venv\Scripts\python manage.py import_pmbok
```

5. **Run the development server**:
```powershell
.\.venv\Scripts\python manage.py runserver
```

6. **Access at** http://127.0.0.1:8000/

## Project Structure

```
PM-Framework-Analyzer/
├── library/                    # Main Django application
│   ├── management/commands/    # Custom management commands for PDF import
│   ├── migrations/             # Database migrations
│   ├── models.py              # Data models (Book, Section, Page)
│   ├── views.py               # View logic and AI analysis
│   └── urls.py                # URL routing
├── pdfcompare/                # Django project configuration
│   ├── settings.py            # Project settings
│   └── wsgi.py                # WSGI application entry point
├── templates/library/         # HTML templates
│   ├── index.html             # Home page
│   ├── book_detail.html       # Book table of contents
│   ├── section_detail.html    # Section content view
│   ├── search_results.html    # Search results page
│   ├── compare.html           # Topic comparison page
│   ├── analysis_loading.html  # Loading indicator for AI
│   └── analysis.html          # AI analysis results
├── .env                       # Environment variables (not committed)
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
├── vercel.json               # Vercel deployment configuration
├── build_files.sh            # Build script for Vercel
├── WBS.md                    # Work Breakdown Structure
└── README.md                 # This file
```

## Data Model

### Book
Represents a project management standard document.
- title: Name of the standard
- author: Author/organization
- publication_year: Year published
- total_pages: Total page count

### Section
A topic or subtopic within a book with hierarchical structure.
- book: Foreign key to Book
- title: Section title
- section_number: Reference number (e.g., "7.8", "S1.1")
- level: Hierarchy level (1=main topic, 2=subtopic, etc.)
- start_page: First page of section
- end_page: Last page of section
- content: Full text content of the section

### Page
Individual page content linked to its section.
- section: Foreign key to Section
- page_number: Page number in document
- content: Extracted text from page

## Usage Guide

### Browsing Books
1. Visit the home page to see all imported PM standards
2. Click on any book to view its hierarchical table of contents
3. Navigate through sections and subsections

### Searching Topics
1. Use the search bar on the home page or compare page
2. Enter a topic (e.g., "risk management", "stakeholder")
3. View results grouped by book with page references
4. Click any result to read the full section content

### AI Comparative Analysis
1. Search for a topic or go to the Compare page
2. Click the "Analysis" button
3. Wait for AI processing (5-10 seconds)
4. View comparative insights showing:
   - Similarities across standards
   - Differences in approach
   - Unique perspectives from each framework
5. All insights include specific page references

### Navigation
- Smart back buttons remember your browsing context
- Click on section titles to view full content
- Use breadcrumb links to navigate the hierarchy
- Return to analysis results from any linked section

## Deployment to Vercel

### Prerequisites
- Git installed
- Vercel account (free tier available)
- Node.js installed (for Vercel CLI)

### Step-by-Step Deployment

1. **Install Vercel CLI**:
```powershell
npm install -g vercel
```

2. **Login to Vercel**:
```powershell
vercel login
```

3. **Deploy**:
```powershell
vercel --prod
```

4. **Set environment variables in Vercel Dashboard**:
   - DJANGO_SECRET_KEY: Your Django secret key
   - GEMINI_API_KEY: Your Google Gemini API key  
   - DEBUG: False
   - ALLOWED_HOSTS: .vercel.app

5. **Configure Deployment Protection**:
   - Go to Project Settings > Deployment Protection
   - Set to "Public" (not "Vercel Authentication Required")

### Production Notes

**Database Persistence**: SQLite database is included in the deployment. All imported books and sections are part of the deployment bundle.

**Static Files**: Automatically collected during build process via build_files.sh

**API Keys**: Never commit API keys to Git. Always use environment variables.

**Custom Domain**: Configure in Vercel Dashboard under Domains section

## Environment Variables

Create a `.env` file in the project root with:

```
DJANGO_SECRET_KEY=your-generated-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

Generate a new Django secret key:
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Get a Gemini API key at: https://ai.google.dev/

## Imported Standards

The application includes content from four major project management frameworks:

1. **ISO 21500:2021** - Project, programme and portfolio management - Context and concepts (23 sections)
2. **ISO 21502:2020** - Guidance on project management (142 sections)
3. **PRINCE2** - Managing Successful Projects with PRINCE2 (302 sections)
4. **PMBOK Guide** - Project Management Body of Knowledge (192 sections, with STANDARD + GUIDE structure)

Total: 667 sections across 4 standards

## Contributing

Contributions are welcome. Please follow these guidelines:
1. Fork the repository
2. Create a feature branch
3. Commit your changes with clear messages
4. Push to your fork
5. Submit a pull request

## License

This project is for educational purposes. The PDF content belongs to their respective copyright holders:
- ISO standards: International Organization for Standardization
- PRINCE2: AXELOS Limited (PeopleCert)
- PMBOK Guide: Project Management Institute (PMI)

## Acknowledgments

- Google Gemini AI for comparative analysis capabilities
- Django community for the excellent web framework
- pdfplumber for reliable PDF text extraction
- Vercel for serverless deployment platform

## Contact

For questions or issues, please open an issue on the GitHub repository.

## Project Status

Status: COMPLETED AND DEPLOYED
Version: 1.0
Last Updated: October 5, 2025
- For PDFs without outlines, the importer uses heading detection heuristics (numbering patterns, capitalization, line length)
- Text is cleaned and normalized during import
- Sections show accurate page ranges (start to end)
- Web uploads are processed the same way as command-line imports
#   T r i g g e r   r e d e p l o y 
 
 