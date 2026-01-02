# Upload Sentiment Analysis Project to IBM-AI-DEV-Certification Repo

## Steps to Add This Project to Your Certification Repository

### Step 1: Clone the Repository (if not already cloned)

```bash
cd /Users/k/IBM-AI-DEV
git clone https://github.com/kamhhm/IBM-AI-DEV-Certification.git
cd IBM-AI-DEV-Certification
```

### Step 2: Create the NLP_sentiment_analysis Folder

```bash
mkdir -p NLP_sentiment_analysis
```

### Step 3: Copy Project Files

From the current project directory (`zzrjt-practice-project-emb-ai`), copy all files to the new folder:

```bash
cd /Users/k/IBM-AI-DEV/IBM-AI-DEV-Certification
cp -r ../zzrjt-practice-project-emb-ai/* NLP_sentiment_analysis/
```

Or manually copy these files/folders:
- `flask_server.py`
- `practice_project/`
- `templates/`
- `static/`
- `README.md`
- `requirements.txt`
- `.gitignore`
- `LICENSE` (if exists)

### Step 4: Remove Unnecessary Files

Remove any files that shouldn't be in the repo:

```bash
cd NLP_sentiment_analysis
find . -name "__pycache__" -type d -exec rm -r {} + 2>/dev/null || true
find . -name "*.pyc" -delete
```

### Step 5: Stage and Commit

```bash
cd /Users/k/IBM-AI-DEV/IBM-AI-DEV-Certification
git add NLP_sentiment_analysis/
git commit -m "Add NLP Sentiment Analysis project"
```

### Step 6: Push to GitHub

```bash
git push origin main
```

## Alternative: Using Git Commands Directly

If you prefer to do it all in one go:

```bash
# Navigate to your certification repo
cd /Users/k/IBM-AI-DEV
git clone https://github.com/kamhhm/IBM-AI-DEV-Certification.git
cd IBM-AI-DEV-Certification

# Create folder and copy files
mkdir -p NLP_sentiment_analysis
cp -r ../zzrjt-practice-project-emb-ai/* NLP_sentiment_analysis/

# Clean up cache files
cd NLP_sentiment_analysis
find . -name "__pycache__" -type d -exec rm -r {} + 2>/dev/null || true
find . -name "*.pyc" -delete

# Commit and push
cd ..
git add NLP_sentiment_analysis/
git commit -m "Add NLP Sentiment Analysis project with Flask and Watson NLP API"
git push origin main
```

## Verify Upload

After pushing, check your repository at:
https://github.com/kamhhm/IBM-AI-DEV-Certification

You should see the `NLP_sentiment_analysis/` folder with all your project files.

