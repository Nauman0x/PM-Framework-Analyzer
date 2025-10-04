# PMStandards Hub

A Django-based web application for comparing and analyzing project management standards (ISO 21500, ISO 21502, PRINCE2, PMBOK Guide) with AI-powered insights.

## Features

- 📚 **PDF Content Extraction**: Automatically extracts and indexes content from PM standard PDFs
- 🔍 **Smart Search**: Search topics across all standards with book-grouped results
- 🤖 **AI Analysis**: Gemini AI-powered comparative analysis of topics across standards
- 📊 **Hierarchical TOC**: Properly structured table of contents with sections and subsections
- 🎨 **Modern UI**: Clean, gradient-based design with responsive layout
- 📄 **Page References**: All content includes accurate page number references

## Technology Stack

- **Backend**: Django 5.2.7
- **Database**: SQLite (development) / PostgreSQL (recommended for production)
- **PDF Processing**: pdfplumber 0.11.7
- **AI Integration**: Google Gemini API (gemini-2.0-flash-exp)
- **Frontend**: HTML, CSS (no framework)

## Setup (Windows, PowerShell)

1. Create a virtualenv and install requirements:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. **Set up environment variables** (create `.env` file):
```
DJANGO_SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
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

## Deployment to Vercel

1. **Install Vercel CLI**:
```bash
npm install -g vercel
```

2. **Login to Vercel**:
```bash
vercel login
```

3. **Deploy**:
```bash
vercel --prod
```

4. **Set environment variables in Vercel Dashboard**:
   - `DJANGO_SECRET_KEY`: Your Django secret key
   - `GEMINI_API_KEY`: Your Google Gemini API key  
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: your-app.vercel.app

## Important Production Notes

⚠️ **Database**: Vercel has read-only file systems. For production:
   - Use external PostgreSQL database (Vercel Postgres, Supabase, etc.)
   - Current SQLite won't persist data on Vercel

⚠️ **File Storage**: Pre-import PDFs before deployment or use cloud storage (S3, Cloudinary)

## Usage
- **Home Page**: Browse all books, search topics, compare standards
- **Book Detail**: View table of contents with hierarchical sections
- **Section View**: Read full section content with page references
- **Search**: Find topics across all standards with grouped results
- **Analysis**: AI-powered comparative analysis with similarities, differences, and unique points

## Data Model
- **Book**: PDF document metadata
- **Section**: Topics/subtopics with title, section number, level, page ranges, and full content
- **Page**: Individual page text linked to sections

## API Keys

Get a Google Gemini API key at: https://ai.google.dev/

## License

MIT License
- For PDFs without outlines, the importer uses heading detection heuristics (numbering patterns, capitalization, line length)
- Text is cleaned and normalized during import
- Sections show accurate page ranges (start to end)
- Web uploads are processed the same way as command-line imports
