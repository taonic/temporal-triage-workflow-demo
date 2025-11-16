from flask import Flask, jsonify
from datetime import datetime, timedelta
import uuid
import random
import json
import os
from openai import OpenAI

app = Flask(__name__)

# Mock email storage
emails = []
last_poll_time = datetime.now()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Bank customer request topics
REQUEST_TOPICS = [
    "account balance inquiry",
    "credit card dispute",
    "loan application status",
    "suspicious transaction report",
    "password reset request",
    "wire transfer inquiry",
    "mortgage rate question",
    "overdraft fee complaint",
    "debit card replacement",
    "account closure request"
]

def generate_mock_email():
    topic = random.choice(REQUEST_TOPICS)
    account_id = f"ACC-{random.randint(1, 5):03d}"
    
    prompt = f"""Generate a realistic customer email to a bank about: {topic}

Include:
- A brief subject line
- Customer's concern or request in 2-3 sentences
- In some emails, mention the account ID: {account_id} naturally in the body
- Choose random tones with positive or negative sentiment

Format as JSON with keys: subject, body"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        email_data = json.loads(content)
        subject = email_data.get('subject', f'Customer Request: {topic}')
        body = email_data.get('body', f'Request regarding {topic}')
    except Exception as e:
        print(f"LLM generation failed: {e}")
        subject = f'Customer Request: {topic}'
        body = f'I need assistance with {topic} for my account {account_id}. Please help me resolve this matter.'
    
    return {
        "id": str(uuid.uuid4()),
        "subject": subject,
        "sender": f"customer{random.randint(1000, 9999)}@email.com",
        "recipient": "support@bank.com",
        "body": body,
        "receivedDateTime": datetime.now().isoformat(),
        "isRead": False
    }

@app.route('/v1.0/me/messages/delta', methods=['GET'])
def get_new_emails():
    global last_poll_time, emails
    
    # Simulate new emails arriving (add 1-2 new emails per poll)
    new_email_count = random.randint(0, 2)
    
    new_emails = []
    for _ in range(new_email_count):
        email = generate_mock_email()
        emails.append(email)
        new_emails.append(email)
    
    last_poll_time = datetime.now()
    
    return jsonify({
        "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#Collection(message)",
        "@odata.deltaLink": f"https://graph.microsoft.com/v1.0/me/messages/delta?$deltatoken={uuid.uuid4()}",
        "value": new_emails
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "graph_service"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001, debug=True)
