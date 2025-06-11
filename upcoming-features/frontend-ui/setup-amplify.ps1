# AWS Amplify Setup Script for Next.js Application (PowerShell)
# This script helps prepare your project for Amplify deployment

Write-Host "🚀 Setting up AWS Amplify deployment for Next.js application..." -ForegroundColor Green

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "📦 Initializing git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git repository already exists" -ForegroundColor Green
}

# Check if amplify.yml exists
if (-not (Test-Path "amplify.yml")) {
    Write-Host "❌ amplify.yml not found. Please ensure it exists in the root directory." -ForegroundColor Red
    exit 1
} else {
    Write-Host "✅ amplify.yml found" -ForegroundColor Green
}

# Check if package.json exists
if (-not (Test-Path "package.json")) {
    Write-Host "❌ package.json not found. Please ensure it exists in the root directory." -ForegroundColor Red
    exit 1
} else {
    Write-Host "✅ package.json found" -ForegroundColor Green
}

# Add all files to git
Write-Host "📝 Adding files to git..." -ForegroundColor Yellow
git add .

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    Write-Host "💾 Committing changes..." -ForegroundColor Yellow
    git commit -m "Prepare for AWS Amplify deployment"
    Write-Host "✅ Changes committed" -ForegroundColor Green
} else {
    Write-Host "ℹ️  No changes to commit" -ForegroundColor Blue
}

# Check if remote origin exists
try {
    $remoteUrl = git remote get-url origin 2>$null
    if ($remoteUrl) {
        Write-Host "✅ Remote origin already configured" -ForegroundColor Green
        Write-Host "🌐 Remote URL: $remoteUrl" -ForegroundColor Cyan
    } else {
        Write-Host "⚠️  No remote origin configured" -ForegroundColor Yellow
        Write-Host "Please add your remote repository:" -ForegroundColor Yellow
        Write-Host "git remote add origin <your-repository-url>" -ForegroundColor White
    }
} catch {
    Write-Host "⚠️  No remote origin configured" -ForegroundColor Yellow
    Write-Host "Please add your remote repository:" -ForegroundColor Yellow
    Write-Host "git remote add origin <your-repository-url>" -ForegroundColor White
}

Write-Host ""
Write-Host "🎉 Setup complete! Next steps:" -ForegroundColor Green
Write-Host ""
Write-Host "1. Push your code to your Git repository:" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Go to AWS Amplify Console:" -ForegroundColor White
Write-Host "   https://console.aws.amazon.com/amplify/" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Click 'New app' → 'Host web app'" -ForegroundColor White
Write-Host ""
Write-Host "4. Connect your Git repository and follow the deployment guide" -ForegroundColor White
Write-Host ""
Write-Host "📖 For detailed instructions, see: AMPLIFY_DEPLOYMENT_GUIDE.md" -ForegroundColor Yellow 