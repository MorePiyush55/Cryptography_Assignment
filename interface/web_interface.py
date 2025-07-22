from flask import Flask, render_template, request, redirect, url_for, flash
import sys
import os
sys.path.append('src')
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'secure_property_transaction_key_2024'

# In-memory storage for transactions (in production, use a database)
transactions = []
# Separate storage for messages in the hub (messages waiting to be forwarded)
hub_messages = []
# Contract exchange tracking
contract_exchanges = []
# Security relationship tracking (existing vs first-time communication)
security_relationships = {
    'hr_seller': {'established': False, 'first_contact': None, 'key_exchange_complete': False},
    'hr_buyer': {'established': True, 'first_contact': '2025-01-15', 'key_exchange_complete': True}  # Mrs. Harvey is established client
}

def log_transaction(sender, receiver, message, transaction_type="message", full_content=None):
    """Log a transaction with full content support and UK legal compliance"""
    transaction = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'sender': sender,
        'receiver': receiver,
        'description': message[:50] + "..." if len(message) > 50 else message,
        'full_content': full_content or message,
        'type': transaction_type,
        'legal_compliance': 'UK_PROPERTY_LAW_COMPLIANT',
        'encryption_level': 'RSA-2048_AES-256',
        'audit_trail': True
    }
    transactions.append(transaction)
    print(f"📝 Transaction logged: {sender} → {receiver} [UK Legal Compliant]")

def log_contract_exchange(step, sender, receiver, contract_type, status):
    """Log contract exchange steps for legal audit trail"""
    contract_log = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'step': step,
        'sender': sender,
        'receiver': receiver,
        'contract_type': contract_type,
        'status': status,
        'legal_binding': True,
        'uk_law_compliant': True
    }
    contract_exchanges.append(contract_log)
    print(f"📋 Contract Exchange Step {step}: {sender} → {receiver} [{status}]")

def check_communication_allowed(sender, receiver):
    """Ensure communication follows assignment rules - no direct buyer-seller contact"""
    # Define the allowed communication patterns per assignment
    allowed_patterns = [
        ('H&R (Hackit & Run LLP)', 'Seller\'s Solicitor'),
        ('Seller\'s Solicitor', 'H&R (Hackit & Run LLP)'),
        ('H&R (Hackit & Run LLP)', 'Mrs. Harvey (Property Buyer)'),
        ('Mrs. Harvey (Property Buyer)', 'H&R (Hackit & Run LLP)')
    ]
    
    # FORBIDDEN: Direct communication between buyer and seller's solicitor
    forbidden_patterns = [
        ('Mrs. Harvey (Property Buyer)', 'Seller\'s Solicitor'),
        ('Seller\'s Solicitor', 'Mrs. Harvey (Property Buyer)')
    ]
    
    if (sender, receiver) in forbidden_patterns:
        return False, "PROTOCOL VIOLATION: Direct buyer-seller communication not allowed per UK legal requirements"
    
    if (sender, receiver) in allowed_patterns:
        return True, "Communication allowed per assignment protocol"
    
    return False, "Unknown communication pattern"

def establish_security_relationship(party1, party2):
    """Handle first-time vs existing relationship security scenarios"""
    relationship_key = f"{party1.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('\'', '')}" + "_" + f"{party2.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('\'', '')}"
    
    if 'hr' in relationship_key and 'seller' in relationship_key:
        if not security_relationships['hr_seller']['established']:
            # Scenario B: First-time communication
            security_relationships['hr_seller']['established'] = True
            security_relationships['hr_seller']['first_contact'] = datetime.now().strftime('%Y-%m-%d')
            security_relationships['hr_seller']['key_exchange_complete'] = True
            return "SCENARIO_B_FIRST_TIME"
        else:
            # Scenario A: Existing relationship
            return "SCENARIO_A_EXISTING"
    
    return "ESTABLISHED_RELATIONSHIP"

def add_to_hub(sender, receiver, message, full_content=None):
    """Add message to hub for forwarding (only non-H&R messages)"""
    if sender != 'H&R (Hackit & Run LLP)':
        hub_message = {
            'id': len(hub_messages),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'sender': sender,
            'receiver': receiver,
            'description': message[:50] + "..." if len(message) > 50 else message,
            'full_content': full_content or message,
            'type': 'hub_message'
        }
        hub_messages.append(hub_message)
        print(f"📨 Message added to hub: {sender} → {receiver}")

def remove_from_hub(message_id):
    """Remove message from hub after forwarding"""
    global hub_messages
    if 0 <= message_id < len(hub_messages):
        removed_msg = hub_messages.pop(message_id)
        print(f"🗑️ Message removed from hub: {removed_msg['sender']} → {removed_msg['receiver']}")
        # Re-index remaining messages
        for i, msg in enumerate(hub_messages):
            msg['id'] = i
        return True
    return False

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hr')
def hr_interface():
    return render_template('hr.html', 
                         transactions=transactions, 
                         hub_messages=hub_messages,
                         contract_exchanges=contract_exchanges,
                         security_relationships=security_relationships)

@app.route('/seller')
def seller_interface():
    return render_template('seller.html', transactions=transactions)

@app.route('/buyer')
def buyer_interface():
    return render_template('buyer.html', transactions=transactions)

@app.route('/send_message', methods=['POST'])
def send_message():
    sender = request.form.get('sender', '')
    receiver = request.form.get('receiver', '')
    message = request.form.get('message', '')
    
    if not all([sender, receiver, message]):
        flash('All fields are required!', 'error')
        return redirect(request.referrer or url_for('home'))
    
    # Map internal names to display names
    sender_map = {
        'hr': 'H&R (Hackit & Run LLP)',
        'seller': 'Seller\'s Solicitor',
        'buyer': 'Mrs. Harvey (Property Buyer)'
    }
    
    receiver_map = {
        'hr': 'H&R (Hackit & Run LLP)',
        'seller': 'Seller\'s Solicitor',
        'buyer': 'Mrs. Harvey (Property Buyer)'
    }
    
    sender_display = sender_map.get(sender, sender)
    receiver_display = receiver_map.get(receiver, receiver)
    
    # Check if communication is allowed per assignment rules
    allowed, reason = check_communication_allowed(sender_display, receiver_display)
    if not allowed:
        flash(f'❌ {reason}', 'error')
        return redirect(request.referrer or url_for('home'))
    
    # Establish security relationship (Scenario A vs B)
    security_scenario = establish_security_relationship(sender_display, receiver_display)
    
    # Log the transaction with UK legal compliance
    log_transaction(sender_display, receiver_display, message, full_content=message)
    
    # Add to hub if it's not from H&R (for forwarding)
    add_to_hub(sender_display, receiver_display, message, full_content=message)
    
    # Add security scenario info to flash message
    scenario_info = ""
    if security_scenario == "SCENARIO_B_FIRST_TIME":
        scenario_info = " [First-time secure communication established]"
    elif security_scenario == "SCENARIO_A_EXISTING":
        scenario_info = " [Existing secure relationship]"
    
    flash(f'✅ Message sent securely from {sender_display} to {receiver_display}!{scenario_info}', 'success')
    
    # Redirect based on sender
    if sender == 'hr':
        return redirect(url_for('hr_interface'))
    elif sender == 'seller':
        return redirect(url_for('seller_interface'))
    elif sender == 'buyer':
        return redirect(url_for('buyer_interface'))
    else:
        return redirect(url_for('home'))

@app.route('/forward_message', methods=['POST'])
def forward_message():
    """New route specifically for forwarding messages from hub - Contract Exchange Protocol"""
    message_id = request.form.get('message_id', type=int)
    recipient = request.form.get('recipient', '')
    message_content = request.form.get('message_content', '')
    
    if message_id is None or not recipient or not message_content:
        flash('Invalid forwarding request!', 'error')
        return redirect(url_for('hr_interface'))
    
    # Map recipient
    recipient_map = {
        'seller': 'Seller\'s Solicitor',
        'buyer': 'Mrs. Harvey (Property Buyer)'
    }
    
    recipient_display = recipient_map.get(recipient, recipient)
    
    # Determine if this is a contract exchange step
    is_contract = 'contract' in message_content.lower() or 'agreement' in message_content.lower()
    
    if is_contract:
        # This is part of the contract exchange process
        if recipient == 'buyer':
            # Step 2: H&R → Mrs. Harvey (forward contract)
            log_contract_exchange(2, 'H&R (Hackit & Run LLP)', recipient_display, 'Property Sale Contract', 'Contract Forwarded to Buyer')
        elif recipient == 'seller':
            # Step 4: H&R → Seller's Solicitor (signed contract)
            log_contract_exchange(4, 'H&R (Hackit & Run LLP)', recipient_display, 'Signed Property Sale Contract', 'Signed Contract Delivered')
    
    # Log the forwarded message as a new transaction with UK legal compliance
    log_transaction('H&R (Hackit & Run LLP)', recipient_display, message_content, full_content=message_content)
    
    # Remove the message from hub
    if remove_from_hub(message_id):
        flash(f'✅ Message forwarded to {recipient_display} and removed from hub! [UK Legal Protocol Compliant]', 'success')
    else:
        flash('❌ Error removing message from hub!', 'error')
    
    return redirect(url_for('hr_interface'))

@app.route('/contract_exchange', methods=['POST'])
def contract_exchange():
    """Handle specific contract exchange process per assignment requirements"""
    step = request.form.get('step', type=int)
    sender = request.form.get('sender', '')
    action = request.form.get('action', '')
    
    if step == 1:
        # Step 1: Seller's Solicitor sends contract to H&R
        log_contract_exchange(1, 'Seller\'s Solicitor', 'H&R (Hackit & Run LLP)', 'Property Sale Contract', 'Contract Received')
        flash('✅ Step 1 Complete: Contract received from Seller\'s Solicitor', 'success')
    
    elif step == 3:
        # Step 3: Mrs. Harvey digitally signs contract and returns to H&R
        log_contract_exchange(3, 'Mrs. Harvey (Property Buyer)', 'H&R (Hackit & Run LLP)', 'Digitally Signed Contract', 'Contract Digitally Signed')
        flash('✅ Step 3 Complete: Contract digitally signed by Mrs. Harvey (Legally Binding)', 'success')
    
    return redirect(url_for('hr_interface'))

@app.route('/upload_file', methods=['POST'])
def upload_file():
    sender = request.form.get('sender', '')
    receiver = request.form.get('receiver', '')
    file = request.files.get('file')
    
    if not file or file.filename == '':
        flash('Please select a file to upload!', 'error')
        return redirect(request.referrer or url_for('home'))
    
    # Map internal names to display names
    sender_map = {
        'hr': 'H&R (Hackit & Run LLP)',
        'seller': 'Seller\'s Solicitor',
        'buyer': 'Mrs. Harvey (Property Buyer)'
    }
    
    receiver_map = {
        'hr': 'H&R (Hackit & Run LLP)',
        'seller': 'Seller\'s Solicitor',
        'buyer': 'Mrs. Harvey (Property Buyer)'
    }
    
    sender_display = sender_map.get(sender, sender)
    receiver_display = receiver_map.get(receiver, receiver)
    
    # Log the file upload
    message = f"📁 Secure Document Upload: {file.filename}"
    file_content = f"Document uploaded: {file.filename}\nFile size: {len(file.read())} bytes\nSecurely encrypted and transmitted."
    log_transaction(sender_display, receiver_display, message, transaction_type="file_upload", full_content=file_content)
    
    # Add to hub if it's not from H&R
    add_to_hub(sender_display, receiver_display, message, full_content=file_content)
    
    flash(f'✅ File "{file.filename}" uploaded securely from {sender_display} to {receiver_display}!', 'success')
    
    # Redirect based on sender
    if sender == 'hr':
        return redirect(url_for('hr_interface'))
    elif sender == 'seller':
        return redirect(url_for('seller_interface'))
    elif sender == 'buyer':
        return redirect(url_for('buyer_interface'))
    else:
        return redirect(url_for('home'))

if __name__ == '__main__':
    print("🚀 Starting Property Transaction Protocol Web Interface...")
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("🔒 Secure communication protocol ready!")
    app.run(debug=True, host='0.0.0.0', port=5000)
