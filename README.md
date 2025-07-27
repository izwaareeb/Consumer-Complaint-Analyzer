Live link: https://huggingface.co/spaces/MujiburrRahman/consumer-complaint-classifier

---
title: Consumer Complaint Classifier
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.38.2
app_file: app.py
pinned: false
---

# 🧠 Consumer Complaint Classifier

A smart AI-powered web application that analyzes and categorizes customer complaints in real-time using natural language processing and machine learning.

## 🚀 Features

- **Smart Classification**: Automatically categorizes complaints into relevant categories (Billing, Delivery, Product Quality, Customer Service, Account, Technical)
- **Urgency Detection**: Identifies priority levels (Low/Medium/High) for efficient customer service triage
- **Emotion Analysis**: Detects customer emotional state (Angry, Frustrated, Disappointed, Confused, Worried, Neutral)
- **Confidence Scoring**: Provides reliability metrics for all classifications
- **Real-time Processing**: Instant analysis with immediate feedback
- **Sample Testing**: Pre-loaded example complaints for quick demonstration

## 🛠️ How It Works

The application uses a hybrid approach combining:
1. **Rule-based Classification**: Keyword matching and scoring algorithms for reliable baseline performance
2. **Machine Learning Ready**: Support for trained scikit-learn models with TF-IDF vectorization
3. **Text Preprocessing**: Advanced text cleaning and normalization for optimal accuracy

## 📊 Classification Categories

### Complaint Categories
- **Billing**: Payment, charges, refunds, invoicing issues
- **Delivery**: Shipping, tracking, delays, packaging problems  
- **Product Quality**: Defective items, wrong products, quality concerns
- **Customer Service**: Staff interactions, support experience
- **Account**: Login, password, profile, settings issues
- **Technical**: Website, app, system errors and bugs

### Urgency Levels
- **High**: Requires immediate attention (urgent, critical, emergency language)
- **Medium**: Should be addressed promptly (frustrated, concerned, problem keywords)
- **Low**: Standard processing timeline

### Emotional States
- **Angry**: Strong negative emotions, outrage
- **Frustrated**: Irritation, annoyance
- **Disappointed**: Unmet expectations
- **Confused**: Need for clarification
- **Worried**: Anxiety, concern
- **Neutral**: Calm, factual reporting

## 🎯 Use Cases

- **Customer Service Teams**: Prioritize and route complaints efficiently
- **Business Intelligence**: Analyze complaint patterns and trends
- **Quality Assurance**: Monitor service quality across departments
- **Training**: Demonstrate AI-powered text classification

## 🔧 Technical Details

- **Framework**: Gradio for interactive web interface
- **NLP**: scikit-learn, transformers for text processing
- **Classification**: RandomForestClassifier with TF-IDF features
- **Deployment**: Compatible with Hugging Face Spaces, Replit, local hosting

## 📝 Try It Out

1. Enter a customer complaint in the text area
2. Click "Analyze Complaint" for instant classification
3. Use sample complaints dropdown for quick testing
4. View detailed results with category, urgency, emotion, and confidence scores

Perfect for businesses looking to automate and improve their customer complaint handling process!
