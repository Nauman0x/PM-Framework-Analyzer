# Deployment Guide for Vercel

## Prerequisites
- Git installed
- Vercel account (free tier available)
- Node.js installed (for Vercel CLI)

## Step-by-Step Deployment

### 1. Initialize Git Repository (if not already done)
```powershell
git init
git add .
git commit -m "Initial commit - PMStandards Hub"
```

### 2. Install Vercel CLI
```powershell
npm install -g vercel
```

### 3. Login to Vercel
```powershell
vercel login
```

### 4. Deploy to Vercel
```powershell
vercel
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? Select your account
- Link to existing project? **N**
- What's your project's name? **pmstandards-hub** (or your choice)
- In which directory is your code located? **./** (current directory)
- Want to override settings? **N**

### 5. Set Environment Variables
After first deployment, go to Vercel Dashboard:

1. Go to your project → Settings → Environment Variables
2. Add these variables:
   - `DJANGO_SECRET_KEY`: Generate a new secret key
   - `GEMINI_API_KEY`: AIzaSyCuQ0JzRB-esLXcBnfMxt9ESjzDzD-8wBQ
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: your-project.vercel.app

To generate a Django secret key:
```powershell
.\.venv\Scripts\python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Deploy to Production
```powershell
vercel --prod
```

## Important Notes

### Database Persistence
⚠️ **Critical**: Vercel's serverless functions have ephemeral file systems. Your SQLite database will NOT persist between deployments.

**Solutions**:
1. **Recommended**: Use Vercel Postgres or external PostgreSQL
   ```powershell
   # In Vercel Dashboard, go to Storage → Create Database → Postgres
   # Then update settings_production.py with the connection string
   ```

2. **Alternative**: Use Supabase, PlanetScale, or Railway for database hosting

### Pre-Import PDFs
Since you can't upload files on Vercel's free tier:
1. Import all PDFs locally first
2. Export database: `python manage.py dumpdata > data.json`
3. Use external database and load data there

### File Storage
For production file uploads, integrate:
- AWS S3
- Cloudinary
- Vercel Blob Storage

## Testing Your Deployment

1. Visit your Vercel URL (shown after deployment)
2. Test the search functionality
3. Test AI analysis (requires GEMINI_API_KEY)
4. Check all navigation works

## Troubleshooting

### Build Fails
- Check `vercel` logs in dashboard
- Ensure all dependencies are in requirements.txt
- Verify Python version matches runtime.txt

### 500 Errors
- Check environment variables are set
- Review Function Logs in Vercel Dashboard
- Ensure ALLOWED_HOSTS includes your Vercel domain

### Static Files Missing
- Run: `python manage.py collectstatic`
- Check vercel.json routes configuration

## Continuous Deployment

Link to GitHub for automatic deployments:
1. Push code to GitHub
2. In Vercel Dashboard: Settings → Git → Connect Repository
3. Every push to main branch auto-deploys

## Custom Domain

1. Go to Vercel Dashboard → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Add domain to ALLOWED_HOSTS environment variable
