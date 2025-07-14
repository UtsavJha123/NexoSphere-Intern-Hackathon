# 🌐 Nexosphere Project - Setup & Run Guide

## 📦 Step 1: Unzip the Project

```bash
# Navigate to where you downloaded the ZIP file
cd ~/Downloads  # or your download location

# Unzip the Nexosphere project
unzip Nexosphere.zip

# Navigate to the extracted directory
cd Desktop  # or wherever the folders were extracted

# You should now see three directories:
ls
# Output should show:
# - Nexosphere/
# - Nexosphere_Frontend/  
# - post-creation 3/
```

---

## 🚀 Step 2: Run All Three Applications

### Method 1: Run Each Application in Separate Terminals (Recommended)

Open **3 different terminal windows** and run these commands:

#### Terminal 1 - Backend API (FastAPI)
```bash
cd Nexosphere/
python3 -m pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8080 --reload
```
**Access at: http://localhost:8000** | **API Docs: http://localhost:8000/docs**

#### Terminal 2 - Frontend Web App (Flask)
```bash
cd Nexosphere_Frontend/
python3 -m pip install -r requirements.txt
python3 app.py
```
**Access at: http://localhost:5000**

#### Terminal 3 - Content Generator (Streamlit)
```bash
cd "post-creation 3"/
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```
**Access at: http://localhost:8501**

---

### Method 2: One-Command Script (Automated)

Create and run this script to start everything automatically:

```bash
# Create startup script
cat > start_nexosphere.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Nexosphere Platform..."

# Install dependencies for all apps
echo "📦 Installing dependencies..."
(cd Nexosphere && python3 -m pip install -r requirements.txt > /dev/null 2>&1)
(cd Nexosphere_Frontend && python3 -m pip install -r requirements.txt > /dev/null 2>&1)
(cd "post-creation 3" && python3 -m pip install -r requirements.txt > /dev/null 2>&1)

# Start all applications in background
echo "� Starting Backend API on port 8000..."
cd Nexosphere && python3 -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)" &

echo "🌐 Starting Frontend on port 5000..."
cd ../Nexosphere_Frontend && python3 app.py &

echo "🤖 Starting Content Generator on port 8501..."
cd "../post-creation 3" && python3 -m streamlit run app.py &

echo ""
echo "✅ All applications started!"
echo "🌐 Access URLs:"
echo "   Backend API:      http://localhost:8000"
echo "   API Docs:         http://localhost:8000/docs"
echo "   Frontend:         http://localhost:5000"
echo "   Content Generator: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop this script"
wait
EOF

# Make script executable and run
chmod +x start_nexosphere.sh
./start_nexosphere.sh
```

---

## 📍 Application Access URLs

| Application | URL | Description |
|-------------|-----|-------------|
| **Backend API** | http://localhost:8000 | Main API server |
| **API Documentation** | http://localhost:8000/docs | Interactive API docs |
| **Frontend Web App** | http://localhost:5000 | Web interface |
| **Content Generator** | http://localhost:8501 | AI post generator |

---

## 🔧 Prerequisites

- **Python 3.7+** (check with: `python3 --version`)
- **pip** (Python package manager)

---

## 🛠 Quick Setup Commands (Copy & Paste)

```bash
# Complete setup from ZIP to running applications
unzip Nexosphere.zip
cd Desktop  # or extracted directory

# Install all dependencies at once
(cd Nexosphere && python3 -m pip install -r requirements.txt)
(cd Nexosphere_Frontend && python3 -m pip install -r requirements.txt)
(cd "post-creation 3" && python3 -m pip install -r requirements.txt)

# Run all applications (requires 3 terminals)
# Terminal 1:
cd Nexosphere && python3 -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)"

# Terminal 2: 
cd Nexosphere_Frontend && python3 app.py

# Terminal 3:
cd "post-creation 3" && python3 -m streamlit run app.py
```

---

## 🚨 Troubleshooting

### If applications won't start:

1. **Check Python version:**
   ```bash
   python3 --version  # Should be 3.7+
   ```

2. **Install missing packages:**
   ```bash
   pip3 install fastapi uvicorn flask streamlit
   ```

3. **If ports are busy:**
   ```bash
   kill -9 $(lsof -ti:8000,5000,8501)  # Kill processes on these ports
   ```

4. **Permission issues:**
   ```bash
   chmod -R 755 Nexosphere/ Nexosphere_Frontend/ "post-creation 3"/
   ```

---

## ✅ Verify Everything is Running

```bash
# Check if all applications are accessible
curl http://localhost:8000     # Backend
curl http://localhost:5000     # Frontend  
curl http://localhost:8501     # Streamlit

# Or open in browser:
# http://localhost:8000/docs (API Documentation)
# http://localhost:5000 (Web Interface)
# http://localhost:8501 (Content Generator)
```

---

## 🛑 Stop All Applications

To stop all running applications:
- Press **Ctrl+C** in each terminal window
- Or run: `kill -9 $(lsof -ti:8000,5000,8501)`

---

**🎉 That's it! Your Nexosphere platform should now be running!**

**Need help?** Check the detailed documentation in `MAIN_README.md` for advanced configuration and troubleshooting.
- 💾 **Auto-Save** - Organized file output ready for posting

## 🎯 Sample Output

```
🚨 Breaking News: EU-US Trade Talks Enter New Phase 🚨

As the global trade landscape continues to evolve, it's essential 
for professionals to stay informed about the latest developments...

💡 Here's the takeaway: The trade war between the US and EU is not 
just about tariffs; it's about the future of global trade...

🌎 So, what does this mean for us? How will this shift affect our 
businesses, industries, and careers? Share your thoughts! 💬
```

## 🚀 Quick Start (5 Minutes)

### 1. Setup
```bash
# Clone and setup
git clone <repository-url>
cd Trending-Post-Generator
./setup.sh
```

### 2. Get FREE Groq API Key
```bash
python setup_groq.py  # Shows detailed instructions
```

Visit: https://console.groq.com/ → Sign Up (Free) → API Keys → Create Key

### 3. Configure
Edit `.env` file:
```bash
GROQ_API_KEY=gsk_your_actual_groq_key_here
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

### 4. Generate Posts
```bash
source .venv/bin/activate
python main.py          # Full version with real trends
python demo.py          # Demo with sample data
python main_robust.py   # Advanced options
```

## 📊 Why Groq Over OpenAI?

| Feature | Groq (FREE) | OpenAI (Premium) |
|---------|-------------|------------------|
| Cost | 🆓 FREE | 💰 $0.002/1K tokens |
| Speed | ⚡ Very Fast | 🐌 Moderate |
| Quality | 🎯 Excellent | 🎯 Excellent |
| Daily Limits | 📈 Generous | 💳 Pay-per-use |
| Setup Time | 😊 2 minutes | 😊 2 minutes |

## 🛠️ Advanced Configuration

### Switch to Premium AI (Optional)
```python
# In main.py, change:
generate_daily_post(use_openai=True)  # Uses OpenAI instead of Groq
```

### Custom Prompts
Edit `base_linkedin_post_prompt.txt` to change AI writing style.

### Geographic Targeting
Modify `selenium_helper.py` to change region (US, UK, etc.)

## 📁 Project Structure

```
├── main.py                           # 🎯 Main application
├── main_robust.py                    # 🛡️ Advanced version with options
├── demo.py                           # 🎭 Quick demo mode
├── ai_helper.py                      # 🤖 AI integration (Groq + OpenAI)
├── selenium_helper.py                # 🌐 Web scraping (RSS feeds)
├── trend_fallback.py                 # 🔄 Fallback trending topics
├── test_ai.py                        # 🧪 Test AI integration
├── setup_groq.py                     # 📋 API setup guide
├── base_linkedin_post_prompt.txt     # 📝 AI prompt template
├── requirements.txt                  # 📦 Dependencies
├── setup.sh                          # ⚙️ Auto-setup script
└── linkedin-posts/                   # 💾 Generated content
```

## 🔧 Troubleshooting

### Common Issues
- **"Import could not be resolved"** → Activate virtual environment: `source .venv/bin/activate`
- **"GROQ_API_KEY not configured"** → Check your `.env` file
- **"No trends found"** → App automatically uses fallback sample data
- **ChromeDriver issues** → Not needed! Uses RSS feeds instead

### Performance Tips
- Use `main_robust.py` for maximum reliability
- `demo.py` works instantly without web scraping
- Multiple trend sources ensure consistent operation

## 🌟 Pro Tips

1. **Content Calendar**: Run multiple times to build a week's worth of posts
2. **A/B Testing**: Generate multiple versions with different prompts
3. **Industry Focus**: Edit prompts for specific industries
4. **Peak Times**: Generate during business hours for timely topics

## 🤝 Contributing

Found a bug? Want to add features? PRs welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

Educational use. Respect API terms and website ToS.

---

**Ready to generate viral LinkedIn content for FREE? Let's go! 🚀**

### 💡 Perfect for:
- Content creators looking for trending topics
- Professionals building their LinkedIn presence  
- Marketers needing quick, quality content
- Anyone wanting to stay current with trends

**No credit card, no payments, no limits - just professional content!** 🎉

