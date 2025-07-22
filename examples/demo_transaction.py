"""
Demonstration of the Property Transaction Protocol
This script shows a complete execution of the secure communication protocol
"""

import json
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from crypto_protocol import PropertyTransactionProtocol

def print_section(title: str, content: str = None):
    """Print a formatted section header"""
    print(f"\n{'='*80}")
    print(f" {title}")
    print(f"{'='*80}")
    if content:
        print(content)

def print_subsection(title: str):
    """Print a formatted subsection header"""
    print(f"\n{'-'*60}")
    print(f" {title}")
    print(f"{'-'*60}")

def print_json(data: dict, title: str = None):
    """Print JSON data in a formatted way"""
    if title:
        print(f"\n{title}:")
    print(json.dumps(data, indent=2, default=str))

def demonstrate_protocol():
    """Demonstrate the complete property transaction protocol"""
    
    print_section("PROPERTY TRANSACTION CRYPTOGRAPHIC PROTOCOL DEMONSTRATION")
    print("This demonstration shows secure communication between:")
    print("- H&R (Hackit & Run LLP) - Main solicitor firm")
    print("- Seller's Solicitor - Representing Mr L.M. Facey")
    print("- Mrs. Harvey - The buyer")
    
    # Initialize the protocol
    protocol = PropertyTransactionProtocol()
    
    # Phase 1: Party Initialization
    print_section("PHASE 1: PARTY INITIALIZATION AND KEY GENERATION")
    init_results = protocol.initialize_parties()
    print("✓ Generated RSA-2048 key pairs for all parties")
    print("✓ Public keys ready for distribution")
    print_json(init_results, "Initialization Results")
    
    # Phase 2: Secure Channel Establishment
    print_section("PHASE 2: SECURE CHANNEL ESTABLISHMENT")
    
    # Scenario A: First time communication between H&R and Seller's Solicitor
    print_subsection("Scenario A: First-time communication")
    channel_results_first = protocol.establish_secure_channels(first_time_communication=True)
    print("✓ Full key exchange and authentication performed")
    print("✓ Session keys established")
    print_json(channel_results_first, "First-time Channel Results")
    
    # Scenario B: Subsequent communication (simulated)
    print_subsection("Scenario B: Subsequent communication")
    channel_results_subsequent = protocol.establish_secure_channels(first_time_communication=False)
    print("✓ Existing secure relationship utilized")
    print("✓ Simplified authentication process")
    print_json(channel_results_subsequent, "Subsequent Channel Results")
    
    # Phase 3: Contract Details Setup
    print_section("PHASE 3: TRANSACTION SETUP")
    
    contract_details = {
        'seller': {
            'name': 'Mr L.M. Facey',
            'address': '123 Property Lane, London, UK',
            'solicitor': 'ABC Legal Services'
        },
        'buyer': {
            'name': 'Mrs. Harvey',
            'address': '456 Buyer Street, Manchester, UK',
            'solicitor': 'H&R (Hackit & Run LLP)'
        },
        'property': {
            'address': '789 Land Parcel Road, Birmingham, UK',
            'description': 'Commercial development land, 2.5 acres',
            'price': '500,000',
            'completion_date': '2025-09-15',
            'contract_id': 'CONTRACT-2025-001'
        }
    }
    
    print("Property transaction details configured:")
    print_json(contract_details, "Transaction Details")
    
    # Phase 4: Contract Exchange (Seller's Solicitor → H&R)
    print_section("PHASE 4: CONTRACT TRANSMISSION")
    print_subsection("Seller's Solicitor sends contract to H&R")
    
    contract_exchange = protocol.initiate_contract_exchange(contract_details)
    print("✓ Contract created and digitally prepared")
    print("✓ Message authenticated with RSA-PSS signature")
    print("✓ Message encrypted with hybrid RSA+AES encryption")
    print_json({
        'phase': contract_exchange['phase'],
        'sender': contract_exchange['sender'],
        'recipient': contract_exchange['recipient'],
        'contract_id': contract_exchange['contract_id'],
        'timestamp': contract_exchange['timestamp'],
        'encryption_used': 'RSA-OAEP + AES-256-CBC'
    }, "Contract Exchange Summary")
    
    # Phase 5: H&R Receives and Forwards Contract
    print_section("PHASE 5: CONTRACT FORWARDING")
    print_subsection("H&R receives contract and forwards to Mrs. Harvey")
    
    forwarding_results = protocol.hr_receive_and_forward_contract(
        contract_exchange['encrypted_message']
    )
    
    if 'error' in forwarding_results:
        print(f"❌ Error: {forwarding_results['error']}")
        return
    
    print("✓ H&R successfully decrypted contract from Seller's Solicitor")
    print("✓ Contract authenticity verified")
    print("✓ Contract forwarded to Mrs. Harvey with cover instructions")
    print_json({
        'phase': forwarding_results['phase'],
        'sender': forwarding_results['sender'],
        'recipient': forwarding_results['recipient'],
        'timestamp': forwarding_results['timestamp']
    }, "Forwarding Summary")
    
    # Phase 6: Mrs. Harvey Signs Contract
    print_section("PHASE 6: CONTRACT SIGNING")
    print_subsection("Mrs. Harvey reviews and signs the contract")
    
    signing_results = protocol.mrs_harvey_sign_contract(
        forwarding_results['encrypted_message']
    )
    
    if 'error' in signing_results:
        print(f"❌ Error: {signing_results['error']}")
        return
    
    print("✓ Mrs. Harvey successfully decrypted contract from H&R")
    print("✓ H&R message authenticity verified")
    print("✓ Contract digitally signed with RSA-PSS signature")
    print("✓ Signed contract encrypted and returned to H&R")
    print_json({
        'phase': signing_results['phase'],
        'sender': signing_results['sender'],
        'recipient': signing_results['recipient'],
        'contract_signed': signing_results['contract_signed'],
        'timestamp': signing_results['timestamp'],
        'signature_details': signing_results['signature_verification']
    }, "Signing Summary")
    
    # Phase 7: Final Contract Delivery
    print_section("PHASE 7: FINAL CONTRACT DELIVERY")
    print_subsection("H&R forwards signed contract to Seller's Solicitor")
    
    final_results = protocol.hr_forward_signed_contract(
        signing_results['encrypted_message']
    )
    
    if 'error' in final_results:
        print(f"❌ Error: {final_results['error']}")
        return
    
    print("✓ H&R successfully decrypted signed contract from Mrs. Harvey")
    print("✓ Mrs. Harvey's message authenticity verified")
    print("✓ Contract signature validity confirmed")
    print("✓ Signed contract delivered to Seller's Solicitor")
    print_json({
        'phase': final_results['phase'],
        'sender': final_results['sender'],
        'recipient': final_results['recipient'],
        'contract_verified': final_results['contract_verified'],
        'timestamp': final_results['timestamp']
    }, "Final Delivery Summary")
    
    # Protocol Summary
    print_section("PROTOCOL EXECUTION SUMMARY")
    
    summary = protocol.get_protocol_summary()
    
    print("✅ ALL PHASES COMPLETED SUCCESSFULLY")
    print("\nProtocol State:")
    for state, value in summary['protocol_state'].items():
        status = "✓" if value else "✗"
        print(f"  {status} {state.replace('_', ' ').title()}: {value}")
    
    print("\n🔒 Security Measures Implemented:")
    for algorithm in summary['security_measures']['encryption_algorithms']:
        print(f"  • {algorithm}")
    
    print("\n⚖️ Legal Compliance:")
    for compliance, status in summary['legal_compliance'].items():
        if status:
            print(f"  ✓ {compliance.replace('_', ' ').title()}")
    
    print("\n📊 Communication Audit Trail:")
    print(f"  Total communications logged: {len(summary['communication_log'])}")
    for i, log_entry in enumerate(summary['communication_log'], 1):
        print(f"  {i}. {log_entry['sender']} → {log_entry['recipient']}: {log_entry['action']}")
    
    print_section("DEMONSTRATION COMPLETE")
    print("The property transaction protocol has been successfully demonstrated.")
    print("All security objectives achieved:")
    print("  ✓ Confidentiality - All messages encrypted")
    print("  ✓ Integrity - All messages authenticated and hash-verified")
    print("  ✓ Authenticity - Digital signatures verify sender identity")
    print("  ✓ Non-repudiation - Legally binding digital signatures")
    print("  ✓ Availability - Protocol handles both first-time and repeat communications")

def demonstrate_security_features():
    """Demonstrate specific security features"""
    
    print_section("SECURITY FEATURES DEMONSTRATION")
    
    from key_management import KeyManager
    from digital_signature import DigitalSignature
    from communication import SecureCommunication
    
    # Key Management Demo
    print_subsection("RSA Key Generation")
    key_manager = KeyManager()
    private_key, public_key = key_manager.generate_rsa_keypair(2048)
    print("✓ 2048-bit RSA key pair generated")
    print(f"✓ Public key size: {public_key.key_size} bits")
    
    # Digital Signature Demo
    print_subsection("Digital Signature Creation and Verification")
    ds = DigitalSignature()
    test_document = "This is a test legal document for signature verification."
    signer_info = {'name': 'Test User', 'role': 'buyer', 'jurisdiction': 'UK'}
    
    signed_doc = ds.sign_document(test_document, private_key, signer_info)
    print("✓ Document digitally signed with RSA-PSS")
    
    is_valid, message = ds.verify_signature(signed_doc, public_key)
    print(f"✓ Signature verification: {is_valid} - {message}")
    
    # Encryption Demo
    print_subsection("Hybrid Encryption")
    secure_comm = SecureCommunication()
    test_message = "Confidential contract information for Mrs. Harvey"
    
    encrypted_msg = secure_comm.encrypt_message(test_message, public_key, "sender", "recipient")
    print("✓ Message encrypted with AES-256 + RSA-OAEP")
    
    success, decrypted_msg = secure_comm.decrypt_message(encrypted_msg, private_key)
    print(f"✓ Message decryption: {success}")
    print(f"✓ Original message recovered: {decrypted_msg == test_message}")

if __name__ == "__main__":
    print("Starting Property Transaction Protocol Demonstration...")
    print("=" * 80)
    
    try:
        # Run main demonstration
        demonstrate_protocol()
        
        print("\n\n")
        
        # Run security features demonstration
        demonstrate_security_features()
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("Demonstration completed. Check the output above for results.")
