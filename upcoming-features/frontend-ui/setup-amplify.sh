#!/bin/bash

# AWS Amplify Setup Script for Next.js Application
# This script helps prepare your project for Amplify deployment

echo "🚀 Setting up AWS Amplify deployment for Next.js application..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Check if amplify.yml exists
if [ ! -f "amplify.yml" ]; then
    echo "❌ amplify.yml not found. Please ensure it exists in the root directory."
    exit 1
else
    echo "✅ amplify.yml found"
fi

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found. Please ensure it exists in the root directory."
    exit 1
else
    echo "✅ package.json found"
fi

# Add all files to git
echo "📝 Adding files to git..."
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit"
else
    echo "💾 Committing changes..."
    git commit -m "Prepare for AWS Amplify deployment"
    echo "✅ Changes committed"
fi

# Check if remote origin exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "✅ Remote origin already configured"
    echo "🌐 Remote URL: $(git remote get-url origin)"
else
    echo "⚠️  No remote origin configured"
    echo "Please add your remote repository:"
    echo "git remote add origin <your-repository-url>"
fi

echo ""
echo "🎉 Setup complete! Next steps:"
echo ""
echo "1. Push your code to your Git repository:"
echo "   git push -u origin main"
echo ""
echo "2. Go to AWS Amplify Console:"
echo "   https://console.aws.amazon.com/amplify/"
echo ""
echo "3. Click 'New app' → 'Host web app'"
echo ""
echo "4. Connect your Git repository and follow the deployment guide"
echo ""
echo "📖 For detailed instructions, see: AMPLIFY_DEPLOYMENT_GUIDE.md" 