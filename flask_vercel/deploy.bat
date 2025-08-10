@echo off
echo 🚀 Travel Vibe Curator - Vercel Deployment
echo ==========================================

cd /d "%~dp0"

echo 📁 Current directory: %cd%

REM Check if Vercel CLI is installed
where vercel >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Vercel CLI not found!
    echo 📦 Installing Vercel CLI...
    npm install -g vercel
)

REM Check if user is logged in to Vercel
echo 🔐 Checking Vercel authentication...
vercel whoami >nul 2>nul
if %errorlevel% neq 0 (
    echo 🔑 Please login to Vercel:
    vercel login
)

REM Deploy to Vercel
echo 🚀 Deploying to Vercel...
vercel --prod

echo.
echo ✅ Deployment completed!
echo 🌍 Your app should be live at the URL shown above
echo.
echo 🔧 Next steps:
echo 1. Set your GEMINI_API_KEY environment variable in Vercel dashboard
echo 2. Or use: vercel env add GEMINI_API_KEY
echo.
echo 📚 Visit vercel.com to manage your deployment

pause
