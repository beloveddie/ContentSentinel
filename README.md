# ContentSentinel

![License](https://img.shields.io/badge/license-MIT-blue)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)

## AI-Powered Content Moderation with Human Oversight

ContentSentinel uses AI to pre-screen user-generated content and requires human confirmation before taking down potentially controversial posts, balancing efficient moderation with nuanced judgment.

## 🔍 Overview

ContentSentinel is a content moderation system designed for online platforms that handle user-generated content. The system leverages OpenAI's GPT-4o-mini to analyze posts for potential policy violations while maintaining human oversight for nuanced decisions, especially in borderline or context-dependent cases.

### Key Features

- 🧠 **AI-powered analysis** of text and media content for policy violations
- 🚩 **Multi-category violation detection** (harassment, hate speech, violence, nudity, etc.)
- ⚖️ **Severity assessment** with confidence scoring
- ✅ **Automatic approval** for clearly acceptable content
- 👨‍⚖️ **Human confirmation** for borderline cases and potential violations
- 📊 **Multiple moderation actions** (approve, warn, restrict, remove)
- 📋 **Comprehensive documentation** of moderation decisions
- 🔄 Built on **LlamaIndex's agent workflow technology** for reliable human-AI interaction

## 💻 Installation

### Prerequisites

- Python 3.9+
- OpenAI API key

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/contentsentinel.git
cd contentsentinel
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:

```
OPENAI_API_KEY=your_api_key_here
```

## 🚀 Usage

Run the main script:

```bash
python content_moderation.py
```

This will:
1. Initialize the system with mock content items
2. Analyze each item for potential policy violations using GPT-4o-mini
3. Process items with no violations automatically
4. Request human confirmation for potential violations
5. Generate a moderation summary report

## 📊 Example Output

```
Processing 3 content items...

Analyzing content: POST-001
Type: text_post
Text: "I love this platform! The community here is so supportive and kind."

Analyzing for policy violations...
Analysis complete:
- Violation Category: none
- Severity Level: low
- AI Confidence: 0.95
- Recommended Action: approve

No violations detected. Auto-approving...
Content POST-001 has been automatically approved.

Analyzing content: POST-002
Type: text_post
Text: "This politician is completely corrupt and anyone who supports them is an idiot who deserves what's coming to them."

Analyzing for policy violations...
Analysis complete:
- Violation Category: harassment
- Severity Level: medium
- AI Confidence: 0.85
- Recommended Action: flag_for_review

Potential violation detected. Requesting human review...

CONTENT MODERATION REVIEW REQUIRED

Content ID: POST-002
Posted by: PoliticalRanter42
Content Type: text_post

CONTENT TEXT:
"This politician is completely corrupt and anyone who supports them is an idiot who deserves what's coming to them."

AI ASSESSMENT:
- Violation Category: HARASSMENT
- Severity Level: MEDIUM

AI EXPLANATION:
This content contains potentially harassing language and insults directed at a group of people. While it's in a political context which may allow for some heated discussion, the personal attacks cross into harassment territory. Human review recommended due to political context.

THIS CONTENT REQUIRES HUMAN REVIEW BEFORE TAKING ACTION.

Senior Moderator Johnson, what action should be taken? (approve/warn/restrict/remove): warn

Moderation result: Content POST-002 has been approved with a warning to the user by Senior Moderator Johnson.

===== CONTENT MODERATION SUMMARY =====
- POST-001 (by GoodUser123): APPROVE
  Type: text_post
  Text: "I love this platform! The community here is so supp..."
  Moderated by: AI System
  Moderation date: 2025-04-25T12:34:56.789012

- POST-002 (by PoliticalRanter42): WARN
  Type: text_post
  Text: "This politician is completely corrupt and anyone wh..."
  Violation: harassment (medium)
  Moderated by: Senior Moderator Johnson
  Moderation date: 2025-04-25T12:35:43.123456
```

## 🏗️ Project Structure

```
contentsentinel/
├── content_moderation.py    # Main application file
├── requirements.txt         # Project dependencies
├── .env                     # Environment variables (not in repo)
├── LICENSE                  # License file
└── README.md                # This file
```

## 🔮 Future Work

- Multi-modal content analysis (images, videos, audio)
- Real-time moderation API for integration with platforms
- User reputation and context-aware moderation
- Appeals workflow for users to contest decisions
- Learning from moderator decisions to improve AI accuracy
- Multi-language support for global communities
- Audit logs and compliance reporting features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🛠️ Technologies Used

- **Python**: Core programming language
- **OpenAI GPT-4o-mini**: AI model for content analysis
- **LlamaIndex**: Framework for agent workflows and human-in-the-loop systems
- **Pydantic**: Data validation and settings management
- **dotenv**: Environment variable management

## 🙏 Acknowledgments

- Built with [LlamaIndex](https://www.llamaindex.ai/) for AI agent workflows
- Uses [OpenAI](https://openai.com/) GPT-4o-mini for content analysis
- Content examples are fictional and for demonstration purposes only
- This project is a proof-of-concept and should be customized for specific platform policies before production use
