# Bub's Trading Study Toolkit

An AI-powered study tool built to help a beginner forex trader learn trading concepts in simple, clear English — created using the Claude API.

🔗 **Live app:** [bubs-trading-toolkit.onrender.com](https://bubs-trading-toolkit.onrender.com)

## What it does

- **Learn** — type any trading term, get a beginner-friendly explanation with a concrete example, tailored for a non-native English speaker
- **Quiz** — get tested on saved terms, with AI-graded feedback on your answer before revealing the full explanation
- **Glossary** — a running, saved list of every term learned so far
- **Risk Calculator** — calculates safe position size based on account balance and risk tolerance (pure math, not trading advice)

## Why I built this

My partner is a beginner trader learning forex through MetaTrader 5, and existing resources were either too technical or not adapted for someone whose first language isn't English. I built this to generate explanations that actually match his level, with quizzing built in to reinforce what he's learned — and to teach myself how to build and ship real AI-powered tools along the way.

## Tech stack

- **Python** — core logic
- **Anthropic Claude API** (Sonnet for explanations, Haiku for quiz grading — chosen deliberately to balance quality and cost)
- **Gradio** — web interface
- **Render** — hosting/deployment

## Notes on the build

This project went through two deployment attempts — originally planned for Hugging Face Spaces, but their free tier changed to exclude Gradio-based apps mid-build. Pivoted to Render instead, which is what's currently live. A good reminder that real projects rarely go in a straight line.

## Status

Actively in progress — next planned additions include permanent glossary storage and score tracking.

---

Built by [Jam](https://github.com/jamilynchrishachan-web) as part of a self-directed transition into AI automation.
