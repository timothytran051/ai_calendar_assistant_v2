# AI Calendar Assistant v2

This project is the second version of my AI-powered calendar assistant, built to intelligently extract important academic dates (like exams, quizzes, and homework) directly from course syllabi and sync them to a user’s calendar.

---

# Purpose

This project was designed to overcome limitations in my earlier local-only version. The main goals are to:
- Enable cross-device access via cloud infrastructure
- Integrate Microsoft OAuth 2.0 for secure user authentication
- Explore calendar syncing via Microsoft Graph API (in progress)
- Build a scalable backend using FastAPI and async database sessions

---

# Technologies

- Python + FastAPI — Backend API
- PostgreSQL (planned) — For structured event and policy storage
- Microsoft OAuth 2.0 — Secure user login and token management
- Azure (in progress) — Hosting, Graph API integration, and app registration
- AI/NLP Logic — Extracts keywords like "exam", "quiz", and their associated dates from PDFs

---

# Features

- Parses full syllabus PDFs using PyMuPDF
- Uses regex + keyword logic to extract academic deadlines
- Converts dates to ISO format and stores in PostgreSQL
- Authentication flow built on Microsoft OAuth 2.0
- (Planned) Calendar sync with Microsoft Graph API

---

# In Progress

- Full integration with Azure + Graph API
- Multi-user support
- Outlook Calendar sync
- UI dashboard (possibly React or S3-hosted frontend)

---

# Author

**Timothy Tran**  
Computer Science student | Backend-focused | AI & Cloud enthusiast