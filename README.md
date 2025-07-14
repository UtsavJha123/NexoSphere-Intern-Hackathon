# LinkedIn Genie
....wish granted
## Key Features
1. **:lock: Real LinkedIn Profile Integration**: Authenticates with real credentials and uses your actual profile data
2. **:memo: Advanced Content Creation**: Creates and optimizes LinkedIn posts based on trending content analysis
3. **:mag: Enhanced Job Search**: Finds jobs matched to your skills with accurate location filtering
4. **:bar_chart: Trending Content Analysis**: Maximizes post reach with hashtag and engagement optimization
5. **:sparkles: Profile Optimization**: Suggests improvements to maximize profile visibility
<img width="840" height="492" alt="Screenshot 2025-07-14 at 10 32 28 PM" src="https://github.com/user-attachments/assets/a7ff8743-c3a7-4b8f-85dd-93ba90a58b42" />
## :dart: Use Cases & Examples
### Professional Content Creation
- **Career Announcements**: "Share my promotion to Senior Data Scientist at Google"
- **Project Showcases**: "Post about launching a new AI product that increased efficiency by 40%"
- **Industry Insights**: "Share thoughts on the latest trends in cybersecurity"
- **Achievement Celebrations**: "Announce completion of AWS certification"
- **Conference Highlights**: "Share key takeaways from attending TechCrunch Disrupt"
- **Research Publications**: "Announce my paper on transformer optimization published in NeurIPS"
- **Open Source Contributions**: "Share about contributing to popular ML libraries like PyTorch"
- **Startup Milestones**: "Celebrate reaching 1M users for our AI-powered app"
### Job Search & Career Development
- **Targeted Job Hunting**: "Find remote software engineering jobs in fintech companies"
- **Career Transition**: "Discover product manager roles for someone with engineering background"
- **Salary Benchmarking**: "Compare compensation for senior developer roles in Bangalore"
- **Company Research**: "Find opportunities at fast-growing startups in the AI space"
- **Network Building**: "Identify hiring managers at target companies"
- **Industry-Specific Searches**: "Find AI researcher positions at top tech companies"
- **Location-Based Opportunities**: "Discover ML engineer roles in Hyderabad tech hubs"
- **Skill-Based Matching**: "Find LLM engineer positions requiring PyTorch expertise"
### Personal Branding & Networking
- **Thought Leadership**: "Create posts about best practices in machine learning deployment"
- **Industry Commentary**: "Share opinions on market trends with data-backed insights"
- **Professional Storytelling**: "Transform career journey into engaging LinkedIn content"
- **Expertise Positioning**: "Showcase technical skills through project case studies"
- **Community Engagement**: "Participate in industry discussions with meaningful contributions"
- **Mentorship Content**: "Share experiences mentoring junior AI/ML engineers"
- **Innovation Showcase**: "Highlight breakthrough moments in AI research projects"
- **Team Leadership**: "Document building and scaling engineering teams"
### Content Strategy & Optimization
- **Hashtag Research**: "Find trending hashtags for #TechLeadership posts"
- **Engagement Analysis**: "Optimize posting times based on audience activity"
- **Content Planning**: "Create a month's worth of professional content ideas"
- **Performance Tracking**: "Analyze which types of posts get the most engagement"
- **Competitor Analysis**: "Study successful content strategies in your industry"
- **Viral Content Creation**: "Craft posts with high shareability potential"
- **Audience Targeting**: "Create content for specific professional demographics"
- **Brand Consistency**: "Maintain consistent voice across all professional posts"
### Educational & Professional Development
- **Learning Documentation**: "Share progress on completing a coding bootcamp"
- **Skill Demonstrations**: "Create posts showcasing new programming languages learned"
- **Mentorship Content**: "Share advice for junior developers entering the field"
- **Industry Education**: "Explain complex technical concepts to broader audiences"
- **Career Advice**: "Provide guidance on navigating career challenges"
- **Tutorial Sharing**: "Break down complex AI concepts for beginners"
- **Book Reviews**: "Share insights from latest tech and business books"
- **Course Completion**: "Celebrate finishing advanced machine learning specializations"
### Startup & Entrepreneurship
- **Founder Stories**: "Share the journey of building an AI startup from scratch"
- **Product Launches**: "Announce new features in your SaaS platform"
- **Funding Announcements**: "Celebrate successful seed round completion"
- **Team Growth**: "Highlight key hires and team expansion milestones"
- **Pivot Stories**: "Share lessons learned from strategic business pivots"
- **Customer Success**: "Celebrate major client wins and case studies"
- **Market Insights**: "Share observations about emerging technology trends"
- **Failure Lessons**: "Transform setbacks into valuable learning experiences"
### Technical & Research Content
- **Algorithm Explanations**: "Break down how attention mechanisms work in transformers"
- **Code Insights**: "Share elegant solutions to common programming challenges"
- **Performance Optimizations**: "Document how we improved model inference speed by 60%"
- **Architecture Decisions**: "Explain why we chose microservices for our ML platform"
- **Debugging Stories**: "Share interesting bug fixes and troubleshooting experiences"
- **Tool Comparisons**: "Compare different ML frameworks for specific use cases"
- **Best Practices**: "Share coding standards that improved our team productivity"
- **Security Insights**: "Discuss AI security challenges and mitigation strategies"
## Setup
### Backend Server Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Create a `.env` file in the project root (copy from `.env.example`):
```
LI_USER=your_linkedin_email
LI_PASS=your_linkedin_password
USE_FREE_LLM=true
HUGGINGFACE_API_KEY=hf_your_free_key_here  # Optional for better AI responses
GROQ_API_KEY=gsk_your_free_key_here  # Optional alternative AI provider
```
3. Start the backend server:
```bash
python3 app.py
```
### Chrome Extension Setup
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top-right)
3. Click "Load unpacked" and select the extension directory
4. The LinkedIn Assistant icon should appear in your toolbar
## Usage
### Via Chrome Extension
1. Click the LinkedIn Assistant icon in your Chrome toolbar
2. Enter your LinkedIn credentials if prompted
3. Choose a feature:
   - **Create Post**: Generate optimized LinkedIn content
   - **Find Jobs**: Search for matching positions
   - **Analyze Posts**: Get trending content insights
   - **Insights**: Receive profile optimization suggestions
### Via Command Line (Legacy)
*Note: Command-line interface has been removed. Use the web interface or Chrome extension.*
For web interface usage:
```bash
python3 app.py
```
Then visit `http://localhost:5002` in your browser.
## Note
This is a hackathon prototype. Use responsibly and in accordance with LinkedIn's terms of service.
