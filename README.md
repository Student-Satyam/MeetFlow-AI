# MeetFlow AI 🤖

### From Conversations to Completed Actions

MeetFlow AI is an AI-powered meeting-to-execution agent that converts unstructured meeting conversations into organized summaries, decisions, action items, owners, deadlines, and priorities.

It helps teams move from discussing work to actually completing it.

## 🚀 Features

- **Voice Input:** Use Wispr Flow to dictate natural meeting conversations directly into the application.
- **AI Meeting Summary:** Generate clear and concise meeting summaries using Google Gemini.
- **Decision Extraction:** Identify important decisions made during meetings.
- **Action Item Extraction:** Convert conversations into structured tasks.
- **Task Ownership:** Identify task owners when mentioned in the conversation.
- **Deadline Detection:** Extract deadlines from meeting discussions.
- **Human Approval:** Review and approve extracted tasks before proceeding.
- **Task Tracking:** Mark tasks as completed and track pending work.
- **Open Questions:** Identify unresolved questions that need attention.

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini API
- Wispr Flow
- Pandas
- Pydantic

## ⚙️ How It Works

1. Speak naturally using Wispr Flow.
2. Meeting text appears in the MeetFlow AI input area.
3. Google Gemini analyzes the conversation.
4. The application extracts summaries, decisions, tasks, owners, deadlines, and open questions.
5. Review and approve the extracted tasks.
6. Track task completion through the application.

## 💻 Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/Student-Satyam/MeetFlow-AI.git
cd MeetFlow-AI
```

**2. Create a virtual environment**

```bash
python -m venv venv
```

**3. Activate the environment on Windows**

```powershell
.\venv\Scripts\Activate.ps1
```

**4. Install dependencies**

```bash
pip install streamlit pandas pydantic python-dotenv google-genai
```

**5. Configure your Gemini API key
