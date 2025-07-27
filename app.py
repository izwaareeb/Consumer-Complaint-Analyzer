import gradio as gr
import re
import string

# Sample complaints data
SAMPLE_COMPLAINTS = [
    "I ordered a laptop two weeks ago and it still hasn't arrived. The tracking number doesn't work and customer service keeps giving me different excuses. I need this for work and this delay is completely unacceptable!",
    "My monthly bill has been charged twice this month. I've called three times and each representative tells me something different. One said it would be refunded in 3-5 days, another said 7-10 days. It's been two weeks now and nothing has changed.",
    "The product I received is completely different from what was advertised on your website. The quality is terrible and it broke after just one day of use. I want a full refund immediately.",
    "Your customer service team was incredibly rude to me today. When I called to ask about my order status, the representative hung up on me twice. This is no way to treat paying customers.",
    "I'm having trouble logging into my account. I've tried resetting my password multiple times but the verification emails never arrive. Can someone please help me access my account?",
    "The delivery driver left my package outside in the rain even though I was home. Now my electronics are damaged and unusable. This is the second time this has happened.",
    "I've been trying to cancel my subscription for months but your website keeps giving me error messages. Every time I call, I'm on hold for over an hour. This is extremely frustrating.",
    "The food I ordered was cold and tasted terrible. The restaurant was also an hour late with delivery. I've ordered from you many times before and this was by far the worst experience.",
    "I was promised a discount code that would be emailed to me within 24 hours. It's been a week and I still haven't received anything. I need this code to complete my purchase.",
    "Your app keeps crashing every time I try to make a payment. I've tried on different devices and the problem persists. This is making it impossible for me to place orders."
]

def preprocess_text(text):
    """Preprocess complaint text for better classification"""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove phone numbers
    text = re.sub(r'[\+]?[1-9]?[0-9]{7,15}', '', text)
    
    # Keep only alphanumeric characters and basic punctuation
    text = ''.join(char for char in text if char.isalnum() or char in ' .,!?-')
    
    # Remove excessive punctuation
    text = re.sub(r'[!]{2,}', '!', text)
    text = re.sub(r'[?]{2,}', '?', text)
    text = re.sub(r'[.]{2,}', '.', text)
    
    # Trim whitespace
    text = text.strip()
    
    return text

def classify_complaint(text):
    """Main classification function using rule-based approach"""
    if not text or text.strip() == "":
        raise ValueError("Empty complaint text provided")
    
    # Preprocess the text
    processed_text = preprocess_text(text)
    text_lower = processed_text.lower()
    
    # Category classification based on keywords
    categories = {
        'Billing': ['bill', 'charge', 'payment', 'invoice', 'fee', 'cost', 'price', 'refund', 'money'],
        'Delivery': ['delivery', 'shipping', 'ship', 'arrive', 'package', 'order', 'tracking', 'late', 'delay'],
        'Product Quality': ['broken', 'defective', 'quality', 'damaged', 'wrong', 'faulty', 'poor', 'bad'],
        'Customer Service': ['service', 'staff', 'rude', 'help', 'support', 'representative', 'agent', 'call'],
        'Account': ['account', 'login', 'password', 'access', 'profile', 'settings', 'username'],
        'Technical': ['website', 'app', 'technical', 'error', 'bug', 'crash', 'loading', 'system']
    }
    
    category_scores = {}
    for category, keywords in categories.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        category_scores[category] = score
    
    predicted_category = max(category_scores.keys(), key=lambda x: category_scores[x])
    if category_scores[predicted_category] == 0:
        predicted_category = 'General'
    
    # Urgency detection
    high_urgency_words = ['urgent', 'immediately', 'asap', 'emergency', 'critical', 'terrible', 'awful', 'worst']
    medium_urgency_words = ['soon', 'quickly', 'disappointed', 'frustrated', 'concerned', 'issue', 'problem']
    
    urgency_score = 0
    for word in high_urgency_words:
        if word in text_lower:
            urgency_score += 3
    for word in medium_urgency_words:
        if word in text_lower:
            urgency_score += 1
    
    if urgency_score >= 5:
        urgency = 'High'
    elif urgency_score >= 2:
        urgency = 'Medium'
    else:
        urgency = 'Low'
    
    # Emotion detection
    emotions = {
        'Angry': ['angry', 'furious', 'mad', 'outraged', 'livid', 'hate', 'disgusted'],
        'Frustrated': ['frustrated', 'annoyed', 'irritated', 'bothered', 'upset'],
        'Disappointed': ['disappointed', 'let down', 'expected', 'hoping', 'sad'],
        'Confused': ['confused', 'understand', 'unclear', 'explain', 'what', 'how', 'why'],
        'Worried': ['worried', 'concerned', 'anxious', 'nervous', 'scared']
    }
    
    emotion_scores = {}
    for emotion, keywords in emotions.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        emotion_scores[emotion] = score
    
    predicted_emotion = max(emotion_scores.keys(), key=lambda x: emotion_scores[x])
    if emotion_scores[predicted_emotion] == 0:
        predicted_emotion = 'Neutral'
    
    # Calculate confidence based on keyword matches
    total_keywords = sum(category_scores.values()) + urgency_score + sum(emotion_scores.values())
    confidence = min(85 + (total_keywords * 2), 95)
    
    # Generate summary
    summary = generate_summary(text, predicted_category, urgency, predicted_emotion)
    
    return {
        "category": predicted_category,
        "urgency": urgency,
        "emotion": predicted_emotion,
        "confidence": f"{confidence}%",
        "summary": summary
    }

def generate_summary(text, category, urgency, emotion):
    """Generate a brief analysis summary"""
    word_count = len(text.split())
    
    summary_parts = []
    
    if emotion in ['Angry', 'Frustrated']:
        summary_parts.append(f"Customer expresses strong {emotion.lower()} feelings")
    elif emotion == 'Disappointed':
        summary_parts.append("Customer shows disappointment with the experience")
    elif emotion == 'Confused':
        summary_parts.append("Customer needs clarification and guidance")
    
    if urgency == 'High':
        summary_parts.append("requires immediate attention")
    elif urgency == 'Medium':
        summary_parts.append("should be addressed promptly")
    
    summary_parts.append(f"regarding {category.lower()} issues")
    
    if word_count > 100:
        summary_parts.append("(detailed complaint)")
    elif word_count < 20:
        summary_parts.append("(brief complaint)")
    
    return ". ".join(summary_parts).capitalize() + "."

def handle_input(complaint_text):
    """Handle user input and return classification results"""
    if not complaint_text or complaint_text.strip() == "":
        return "Please enter a complaint to analyze."
    
    try:
        result = classify_complaint(complaint_text)
        return f"""
📋 **Classification Results:**

**Category:** {result['category']}
**Urgency Level:** {result['urgency']}
**Emotion Detected:** {result['emotion']}
**Confidence:** {result['confidence']}

---
**Analysis Summary:** {result['summary']}
"""
    except Exception as e:
        return f"Error processing complaint: {str(e)}"

def get_sample_complaints():
    """Return sample complaints for demonstration"""
    return SAMPLE_COMPLAINTS

# Create the Gradio interface
with gr.Blocks(title="Consumer Complaint Classifier", theme=gr.themes.Soft()) as iface:
    gr.Markdown("# 🧠 Consumer Complaint Classifier")
    gr.Markdown("Analyze and classify customer complaints using AI-powered text analysis.")
    
    with gr.Row():
        with gr.Column(scale=2):
            complaint_input = gr.Textbox(
                lines=8,
                placeholder="Enter your complaint here...\n\nExample: 'I ordered a product two weeks ago and it still hasn't arrived. The customer service team keeps giving me different tracking numbers that don't work. This is completely unacceptable and I want a full refund immediately!'",
                label="Customer Complaint Text",
                show_label=True
            )
            
            with gr.Row():
                analyze_btn = gr.Button("🔍 Analyze Complaint", variant="primary", size="lg")
                clear_btn = gr.Button("🗑️ Clear", variant="secondary")
            
            # Sample complaints dropdown
            sample_dropdown = gr.Dropdown(
                choices=get_sample_complaints(),
                label="📝 Try Sample Complaints",
                show_label=True,
                interactive=True
            )
        
        with gr.Column(scale=2):
            output = gr.Textbox(
                lines=12,
                label="Analysis Results",
                show_label=True,
                interactive=False
            )
    
    # Add instructions
    with gr.Accordion("📖 How to Use", open=False):
        gr.Markdown("""
        ### Instructions:
        1. **Enter a complaint** in the text area on the left
        2. **Click "Analyze Complaint"** to get AI-powered classification
        3. **View results** showing category, urgency, emotion, and analysis
        4. **Try sample complaints** from the dropdown for quick testing
        
        ### What we analyze:
        - **Category**: Billing, Delivery, Product Quality, Customer Service, etc.
        - **Urgency**: How quickly this issue needs attention (Low/Medium/High)
        - **Emotion**: Customer's emotional state (Angry, Frustrated, Disappointed, etc.)
        - **Confidence**: How certain our AI is about the classification
        """)
    
    # Event handlers
    analyze_btn.click(
        fn=handle_input,
        inputs=complaint_input,
        outputs=output
    )
    
    clear_btn.click(
        fn=lambda: ("", ""),
        outputs=[complaint_input, output]
    )
    
    sample_dropdown.change(
        fn=lambda x: x if x else "",
        inputs=sample_dropdown,
        outputs=complaint_input
    )

# Launch for Hugging Face Spaces
if __name__ == '__main__':
    iface.launch()