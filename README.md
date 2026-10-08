# Explain It Like I'm Wrong 🧠

A simple AI chatbot that challenges your claims instead of blindly agreeing with you.

Built using **LangChain** and **Google Gemini**, the chatbot evaluates what you say, explains whether you're correct, identifies what you may have missed, and asks a follow-up question to make you think deeper.

## ✨ Features

- 🔍 Analyzes user claims
- ✅ Identifies whether a claim is correct, partially correct, or incorrect
- 💡 Explains the reasoning in simple language
- ⚠️ Detects misconceptions and hidden assumptions
- 🎯 Provides challenge questions
- 💬 Maintains conversation context
- 🤖 Powered by Google Gemini through LangChain

## 🛠️ Tech Stack

- Python
- LangChain
- Google Gemini

## 📁 Project Structure

```text
Explain-It-Like-Im-Wrong/
│
├── app.py
├── requirements.txt
└── README.md
```

## 💬 Example

```text
You: C++ is always faster than Python.

AI:

VERDICT: PARTIALLY CORRECT

WHY:
C++ is generally faster for CPU-intensive operations because it
is compiled to native machine code and provides low-level control.

WHAT YOU MISSED:
Python libraries such as NumPy use optimized C/C++ implementations,
so Python can still achieve excellent performance for many tasks.

CHALLENGE:
Can you think of a situation where Python could outperform
a naive C++ implementation?
```

## 🎯 Purpose

The goal of this project is to experiment with **conversational AI, prompt engineering, and critical reasoning** using LangChain and Gemini.

Unlike a traditional chatbot that tries to be helpful by agreeing with the user, this project is designed to **question assumptions and encourage better reasoning**.

## 🚀 Future Improvements

- Add claim confidence scoring
- Add difficulty levels
- Add topic selection
- Add conversation history storage
- Add fact-checking with external sources
- Add debate mode
- Track user's reasoning improvement over time

## 👨‍💻 Author

**Adrij Ghosh**

B.Tech CSE | AI/ML & Software Development

---

⭐ If you find the project interesting, consider giving it a star!