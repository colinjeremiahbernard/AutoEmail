# AutoEmail 📧🤖

An intelligent email automation system that reads unread Gmail messages, detects phishing attempts, generates AI-powered summaries, and drafts professional replies using Groq's LLM API.

## 🌟 Features

- **Gmail Integration**: Securely connects to your Gmail account using OAuth 2.0
- **Phishing Detection**: Identifies suspicious emails using keyword analysis and URL inspection
- **AI-Powered Summarization**: Generates concise summaries of email content using Groq's Llama 3.1 model
- **Smart Reply Generation**: Creates professional, context-aware email replies automatically
- **Privacy-First**: Processes emails locally with secure API authentication

## 🏗️ Architecture

```
AutoEmail/
├── main.py                 # Main orchestration logic
├── gmail_service.py        # Gmail API integration
├── phishing_detector.py    # Phishing detection algorithms
├── summarizer.py           # AI email summarization
├── reply_generator.py      # AI reply generation
├── config.py               # Configuration management
├── setup_gmail.py          # Gmail authentication setup
└── requirements.txt        # Python dependencies
```

## 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Gmail Account** with API access enabled
- **Groq API Key** (free tier available at [console.groq.com](https://console.groq.com))
- **Google Cloud Project** with Gmail API enabled

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/colinjeremiahbernard/AutoEmail.git
cd AutoEmail
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Gmail API Credentials

#### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Gmail API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

#### Step 2: Create OAuth 2.0 Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Configure the OAuth consent screen if prompted:
   - User Type: External (for personal use)
   - Add your email as a test user
4. Application type: **Desktop app**
5. Download the credentials file
6. Rename it to `credentials.json` and place it in the project root directory

#### Step 3: Authenticate Gmail Access
```bash
python setup_gmail.py
```
- A browser window will open for Gmail authentication
- Grant the requested permissions
- A `token.json` file will be created automatically

### 5. Configure Groq API Key

#### Get Your Groq API Key
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key

#### Set the API Key

**Option A: Environment Variable (Recommended)**
```bash
# Windows (PowerShell)
$env:GROQ_API_KEY="gsk_your_actual_key_here"

# Windows (Command Prompt)
set GROQ_API_KEY=gsk_your_actual_key_here

# macOS/Linux
export GROQ_API_KEY="gsk_your_actual_key_here"
```

**Option B: .env File**
1. Create a `.env` file in the project root:
```bash
GROQ_API_KEY=gsk_your_actual_key_here
```
2. The application will automatically read from this file

## 🎯 Usage

### Run the Application

```bash
python main.py
```

### What Happens

1. **Authentication**: Connects to Gmail using your `token.json`
2. **Fetch Emails**: Retrieves all unread emails from your inbox
3. **Process Each Email**:
   - Displays the email content
   - Checks for phishing indicators
   - If safe, generates:
     - 📌 **Summary**: Concise overview of the email
     - ✉️ **Reply Draft**: Professional response suggestion

### Example Output

```
--- NEW EMAIL ---

Subject: Project Update Request
From: colleague@company.com

Hi, could you provide an update on the Q2 project status?

📌 SUMMARY:
Colleague requesting Q2 project status update.

✉️ REPLY DRAFT:
Hi [Name],

Thank you for reaching out. I'll compile the Q2 project status 
and send you a comprehensive update by end of day today.

Best regards,
[Your Name]
```

### Phishing Detection

If a phishing attempt is detected:
```
⚠️ Phishing detected! Skipping...
```

The email will be flagged and skipped if it contains:
- Suspicious keywords (urgent, verify account, password, etc.)
- Links to untrusted domains
- Common phishing patterns

## 🔧 Configuration

### Customize Phishing Detection

Edit `phishing_detector.py` to modify detection rules:

```python
# Add or remove suspicious keywords
SUSPICIOUS_KEYWORDS = [
    "urgent", "verify your account", "password", 
    "click here", "bank", "login", "suspended"
]

# Whitelist trusted domains
def contains_suspicious_links(text):
    # Add trusted domains here
    if domain not in ["google", "microsoft", "amazon", "yourdomain"]:
        return True
```

### Adjust AI Model Settings

Modify `summarizer.py` or `reply_generator.py` to change:
- Model selection (e.g., `llama-3.1-70b-versatile` for better quality)
- System prompts for different reply styles
- Temperature and other generation parameters

## 🛠️ Troubleshooting

### "GROQ_API_KEY is missing"
- Ensure your API key is set as an environment variable or in `.env`
- Verify the key starts with `gsk_`
- Check for extra quotes or spaces in the key

### "Groq authentication failed"
- Your API key may be invalid or revoked
- Generate a new key at [console.groq.com](https://console.groq.com)
- Update your environment variable or `.env` file

### "credentials.json not found"
- Download OAuth credentials from Google Cloud Console
- Ensure the file is named exactly `credentials.json`
- Place it in the project root directory

### "token.json not found"
- Run `python setup_gmail.py` to authenticate
- Complete the OAuth flow in your browser
- The token will be created automatically

### Gmail API Quota Exceeded
- Free tier: 1 billion quota units per day
- Reading emails uses minimal quota
- If exceeded, wait 24 hours or upgrade your quota

### No Emails Displayed
- Check if you have unread emails in your inbox
- Verify Gmail API permissions were granted
- Ensure `token.json` is valid (re-run `setup_gmail.py` if needed)

## 🔒 Security & Privacy

- **Credentials**: `credentials.json` and `token.json` are gitignored
- **API Keys**: Never commit `.env` files to version control
- **Local Processing**: Emails are processed locally; only summaries/replies use Groq API
- **OAuth 2.0**: Secure authentication without storing passwords
- **Read-Only Access**: Application only reads emails, cannot send or delete

## 📝 File Descriptions

| File | Purpose |
|------|---------|
| `main.py` | Entry point; orchestrates email processing workflow |
| `gmail_service.py` | Gmail API authentication and email retrieval |
| `phishing_detector.py` | Detects phishing attempts using pattern matching |
| `summarizer.py` | Generates email summaries using Groq LLM |
| `reply_generator.py` | Creates professional reply drafts using Groq LLM |
| `config.py` | Manages API key configuration and validation |
| `setup_gmail.py` | One-time Gmail OAuth authentication setup |
| `requirements.txt` | Python package dependencies |

## 📄 License

This project is proprietary software. All rights reserved by Colin Jeremiah Bernard.

**Copyright © 2026 Colin Jeremiah Bernard. All Rights Reserved.**

This software is provided for viewing purposes only. Any use, modification, distribution, or reproduction requires explicit written permission from the copyright holder. See the [LICENSE](LICENSE) file for complete terms.

To request permission for any use of this software, please contact the author directly.

## 🙏 Acknowledgments

- **Google Gmail API** for email integration
- **Groq** for fast LLM inference
- **Llama 3.1** by Meta for the language model
- **scikit-learn** and **tldextract** for phishing detection

## 📧 Contact

**Colin Jeremiah Bernard**
- GitHub: [@colinjeremiahbernard](https://github.com/colinjeremiahbernard)
- Repository: [AutoEmail](https://github.com/colinjeremiahbernard/AutoEmail)

---

**⭐ If you find this project useful, please consider giving it a star!**