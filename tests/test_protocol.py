"""
Unit Tests for Property Transaction Protocol
Tests all major components of the cryptographic protocol
"""

import unittest
import sys
import os
import json

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from key_management import KeyManager, SymmetricKeyManager
from digital_signature import DigitalSignature, ContractManager
from communication import SecureCommunication, MessageIntegrity
from crypto_protocol import PropertyTransactionProtocol

class TestKeyManagement(unittest.TestCase):
    """Test key generation and management functionality"""
    
    def setUp(self):
        self.key_manager = KeyManager()
        self.symmetric_manager = SymmetricKeyManager()
    
    def test_rsa_key_generation(self):
        """Test RSA key pair generation"""
        private_key, public_key = self.key_manager.generate_rsa_keypair(2048)
        
        # Verify key properties
        self.assertEqual(public_key.key_size, 2048)
        self.assertEqual(private_key.key_size, 2048)
        
        # Verify keys are related
        test_message = b"test message"
        from cryptography.hazmat.primitives.asymmetric import padding
        from cryptography.hazmat.primitives import hashes
        
        # Encrypt with public key, decrypt with private key
        encrypted = public_key.encrypt(
            test_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        decrypted = private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        self.assertEqual(test_message, decrypted)
    
    def test_party_registration(self):
        """Test party registration and key storage"""
        party_info = self.key_manager.register_party('test_party')
        
        self.assertEqual(party_info['party'], 'test_party')
        self.assertIn('public_key', party_info)
        
        # Verify key retrieval
        private_key = self.key_manager.get_private_key('test_party')
        public_key = self.key_manager.get_public_key('test_party')
        
        self.assertIsNotNone(private_key)
        self.assertIsNotNone(public_key)
        
        # Verify the keys match (simplified test)
        from cryptography.hazmat.primitives import serialization
        public_from_private = private_key.public_key()
        
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        public_from_private_pem = public_from_private.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        self.assertEqual(public_pem, public_from_private_pem)
    
    def test_symmetric_key_management(self):
        """Test AES key generation and storage"""
        aes_key = self.symmetric_manager.generate_aes_key()
        
        # Verify key properties
        self.assertEqual(len(aes_key), 32)  # 256 bits
        
        # Test key storage and retrieval
        self.symmetric_manager.store_shared_key('party1', 'party2', aes_key)
        retrieved_key = self.symmetric_manager.get_shared_key('party1', 'party2')
        
        self.assertEqual(aes_key, retrieved_key)
        
        # Test symmetric key ID generation
        key_id1 = self.symmetric_manager._get_key_id('party1', 'party2')
        key_id2 = self.symmetric_manager._get_key_id('party2', 'party1')
        self.assertEqual(key_id1, key_id2)  # Should be same regardless of order

class TestDigitalSignature(unittest.TestCase):
    """Test digital signature functionality"""
    
    def setUp(self):
        self.ds = DigitalSignature()
        self.contract_manager = ContractManager()
        self.key_manager = KeyManager()
        self.key_manager.register_party('test_signer')
        self.private_key = self.key_manager.get_private_key('test_signer')
        self.public_key = self.key_manager.get_public_key('test_signer')
    
    def test_document_signing_and_verification(self):
        """Test basic document signing and verification"""
        document = "This is a test legal document for signature verification."
        signer_info = {
            'name': 'Test Signer',
            'role': 'test_role',
            'jurisdiction': 'UK'
        }
        
        # Sign document
        signed_doc = self.ds.sign_document(document, self.private_key, signer_info)
        
        # Verify required fields
        self.assertIn('signature_data', signed_doc)
        self.assertIn('signature', signed_doc)
        self.assertIn('document', signed_doc)
        self.assertEqual(signed_doc['document'], document)
        
        # Verify signature
        is_valid, message = self.ds.verify_signature(signed_doc, self.public_key)
        self.assertTrue(is_valid)
        self.assertIn('successfully', message.lower())
    
    def test_contract_signature(self):
        """Test contract-specific signature functionality"""
        contract_content = "Test property purchase agreement content"
        
        signed_contract = self.ds.create_contract_signature(
            contract_content, 'Test Buyer', 'buyer', self.private_key
        )
        
        # Verify contract-specific fields
        self.assertIn('legal_statement', signed_contract)
        self.assertIn('UK Electronic Communications Act', signed_contract['legal_statement'])
        
        # Verify signature
        is_valid, verification_details = self.ds.verify_contract_signature(
            signed_contract, self.public_key
        )
        
        self.assertTrue(is_valid)
        self.assertTrue(verification_details['legal_validity'])
        self.assertEqual(verification_details['signer_info']['name'], 'Test Buyer')
    
    def test_contract_creation(self):
        """Test property contract creation"""
        seller_info = {'name': 'Test Seller', 'address': 'Seller Address', 'solicitor': 'Seller Solicitor'}
        buyer_info = {'name': 'Test Buyer', 'address': 'Buyer Address', 'solicitor': 'Buyer Solicitor'}
        property_details = {
            'address': 'Property Address',
            'description': 'Test Property',
            'price': '100000',
            'completion_date': '2025-12-31',
            'contract_id': 'TEST-001'
        }
        
        contract = self.contract_manager.create_property_contract(
            seller_info, buyer_info, property_details
        )
        
        # Verify contract contains required information
        self.assertIn('Test Seller', contract)
        self.assertIn('Test Buyer', contract)
        self.assertIn('Property Address', contract)
        self.assertIn('£100000', contract)
        self.assertIn('TEST-001', contract)
    
    def test_signature_tampering_detection(self):
        """Test that signature verification detects tampering"""
        document = "Original document content"
        signer_info = {'name': 'Test Signer', 'role': 'test', 'jurisdiction': 'UK'}
        
        signed_doc = self.ds.sign_document(document, self.private_key, signer_info)
        
        # Tamper with document
        signed_doc['document'] = "Tampered document content"
        
        # Verification should fail
        is_valid, message = self.ds.verify_signature(signed_doc, self.public_key)
        self.assertFalse(is_valid)
        self.assertIn('tampered', message.lower())

class TestSecureCommunication(unittest.TestCase):
    """Test secure communication functionality"""
    
    def setUp(self):
        self.secure_comm = SecureCommunication()
        self.message_integrity = MessageIntegrity()
        self.key_manager = KeyManager()
        
        # Set up two parties
        self.key_manager.register_party('sender')
        self.key_manager.register_party('recipient')
        
        self.sender_private = self.key_manager.get_private_key('sender')
        self.sender_public = self.key_manager.get_public_key('sender')
        self.recipient_private = self.key_manager.get_private_key('recipient')
        self.recipient_public = self.key_manager.get_public_key('recipient')
    
    def test_hybrid_encryption(self):
        """Test hybrid encryption and decryption"""
        message = "This is a confidential message for testing encryption."
        
        # Encrypt message
        encrypted_package = self.secure_comm.encrypt_message(
            message, self.recipient_public, 'sender', 'recipient'
        )
        
        # Verify package structure
        self.assertIn('sender', encrypted_package)
        self.assertIn('recipient', encrypted_package)
        self.assertIn('encrypted_aes_key', encrypted_package)
        self.assertIn('iv', encrypted_package)
        self.assertIn('encrypted_message', encrypted_package)
        
        # Decrypt message
        success, decrypted_message = self.secure_comm.decrypt_message(
            encrypted_package, self.recipient_private
        )
        
        self.assertTrue(success)
        self.assertEqual(message, decrypted_message)
    
    def test_session_key_encryption(self):
        """Test session key establishment and usage"""
        # Establish session key
        session_key = self.secure_comm.establish_session_key(
            'sender', 'recipient', self.sender_private, self.recipient_public
        )
        
        self.assertEqual(len(session_key), 32)  # 256-bit key
        
        # Encrypt with session key
        message = "Session encrypted message"
        encrypted_package = self.secure_comm.encrypt_with_session_key(
            message, 'sender', 'recipient'
        )
        
        self.assertIsNotNone(encrypted_package)
        self.assertIn('session_id', encrypted_package)
        
        # Decrypt with session key
        success, decrypted_message = self.secure_comm.decrypt_with_session_key(
            encrypted_package
        )
        
        self.assertTrue(success)
        self.assertEqual(message, decrypted_message)
    
    def test_message_authentication(self):
        """Test message authentication and integrity"""
        message = "Message requiring authentication"
        
        # Create authenticated message
        auth_message = self.message_integrity.create_authenticated_message(
            message, 'sender', self.sender_private
        )
        
        # Verify structure
        self.assertIn('message', auth_message)
        self.assertIn('auth_data', auth_message)
        self.assertIn('signature', auth_message)
        
        # Verify authentication
        is_valid, recovered_message = self.message_integrity.verify_authenticated_message(
            auth_message, self.sender_public
        )
        
        self.assertTrue(is_valid)
        self.assertEqual(message, recovered_message)
    
    def test_message_integrity_detection(self):
        """Test that message tampering is detected"""
        message = "Original message content"
        
        auth_message = self.message_integrity.create_authenticated_message(
            message, 'sender', self.sender_private
        )
        
        # Tamper with message
        auth_message['message'] = "Tampered message content"
        
        # Verification should fail
        is_valid, error_message = self.message_integrity.verify_authenticated_message(
            auth_message, self.sender_public
        )
        
        self.assertFalse(is_valid)
        self.assertIn('integrity', error_message.lower())

class TestPropertyTransactionProtocol(unittest.TestCase):
    """Test the complete property transaction protocol"""
    
    def setUp(self):
        self.protocol = PropertyTransactionProtocol()
        
        # Sample transaction data
        self.contract_details = {
            'seller': {
                'name': 'Mr. Test Seller',
                'address': '123 Seller Street',
                'solicitor': 'Test Seller Solicitor'
            },
            'buyer': {
                'name': 'Mrs. Test Buyer',
                'address': '456 Buyer Avenue',
                'solicitor': 'H&R Test'
            },
            'property': {
                'address': '789 Property Lane',
                'description': 'Test property parcel',
                'price': '250000',
                'completion_date': '2025-08-15',
                'contract_id': 'TEST-CONTRACT-001'
            }
        }
    
    def test_protocol_initialization(self):
        """Test protocol initialization and party setup"""
        results = self.protocol.initialize_parties()
        
        # Verify all parties initialized
        self.assertIn('hr', results['parties'])
        self.assertIn('seller_solicitor', results['parties'])
        self.assertIn('mrs_harvey', results['parties'])
        
        # Verify protocol state
        self.assertTrue(self.protocol.protocol_state['hr_registered'])
        self.assertTrue(self.protocol.protocol_state['seller_solicitor_registered'])
        self.assertTrue(self.protocol.protocol_state['mrs_harvey_registered'])
    
    def test_secure_channel_establishment(self):
        """Test secure channel establishment"""
        # Initialize parties first
        self.protocol.initialize_parties()
        
        # Test first-time communication
        results = self.protocol.establish_secure_channels(first_time_communication=True)
        
        self.assertTrue(results['first_time_communication'])
        self.assertIn('hr_seller', results['channels'])
        self.assertIn('hr_harvey', results['channels'])
        self.assertTrue(self.protocol.protocol_state['keys_exchanged'])
    
    def test_complete_transaction_flow(self):
        """Test the complete transaction from start to finish"""
        # Phase 1: Initialize
        init_results = self.protocol.initialize_parties()
        self.assertIn('parties', init_results)
        
        # Phase 2: Establish channels
        channel_results = self.protocol.establish_secure_channels(True)
        self.assertTrue(channel_results['first_time_communication'])
        
        # Phase 3: Contract exchange
        exchange_results = self.protocol.initiate_contract_exchange(self.contract_details)
        self.assertEqual(exchange_results['sender'], 'seller_solicitor')
        self.assertEqual(exchange_results['recipient'], 'hr')
        self.assertTrue(self.protocol.protocol_state['contract_sent'])
        
        # Phase 4: H&R forwards contract
        forward_results = self.protocol.hr_receive_and_forward_contract(
            exchange_results['encrypted_message']
        )
        self.assertNotIn('error', forward_results)
        self.assertEqual(forward_results['sender'], 'hr')
        self.assertEqual(forward_results['recipient'], 'mrs_harvey')
        
        # Phase 5: Mrs. Harvey signs
        signing_results = self.protocol.mrs_harvey_sign_contract(
            forward_results['encrypted_message']
        )
        self.assertNotIn('error', signing_results)
        self.assertTrue(signing_results['contract_signed'])
        self.assertTrue(self.protocol.protocol_state['contract_signed'])
        
        # Phase 6: Final delivery
        final_results = self.protocol.hr_forward_signed_contract(
            signing_results['encrypted_message']
        )
        self.assertNotIn('error', final_results)
        self.assertTrue(final_results['contract_verified'])
        self.assertTrue(self.protocol.protocol_state['transaction_complete'])
        
        # Verify complete protocol summary
        summary = self.protocol.get_protocol_summary()
        self.assertTrue(all(summary['protocol_state'].values()))
        self.assertGreater(len(summary['communication_log']), 0)
    
    def test_error_handling(self):
        """Test protocol error handling"""
        # Test without initialization
        with self.assertRaises(Exception):
            self.protocol.initiate_contract_exchange(self.contract_details)
        
        # Test with invalid encrypted message
        self.protocol.initialize_parties()
        self.protocol.establish_secure_channels(True)
        
        invalid_message = {'invalid': 'message_format'}
        error_result = self.protocol.hr_receive_and_forward_contract(invalid_message)
        self.assertIn('error', error_result)

class TestSecurityProperties(unittest.TestCase):
    """Test security properties of the protocol"""
    
    def setUp(self):
        self.key_manager = KeyManager()
        self.ds = DigitalSignature()
        self.secure_comm = SecureCommunication()
    
    def test_key_uniqueness(self):
        """Test that generated keys are unique"""
        keys1 = self.key_manager.generate_rsa_keypair()
        keys2 = self.key_manager.generate_rsa_keypair()
        
        # Private keys should be different
        from cryptography.hazmat.primitives import serialization
        private1_pem = keys1[0].private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        private2_pem = keys2[0].private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        self.assertNotEqual(private1_pem, private2_pem)
    
    def test_encryption_uniqueness(self):
        """Test that identical messages produce different ciphertexts"""
        self.key_manager.register_party('test_party')
        public_key = self.key_manager.get_public_key('test_party')
        
        message = "Identical message content"
        
        encrypted1 = self.secure_comm.encrypt_message(message, public_key, 'sender', 'recipient')
        encrypted2 = self.secure_comm.encrypt_message(message, public_key, 'sender', 'recipient')
        
        # Should produce different ciphertexts due to random IVs and AES keys
        self.assertNotEqual(encrypted1['encrypted_message'], encrypted2['encrypted_message'])
        self.assertNotEqual(encrypted1['iv'], encrypted2['iv'])
        self.assertNotEqual(encrypted1['encrypted_aes_key'], encrypted2['encrypted_aes_key'])

if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestKeyManagement,
        TestDigitalSignature,
        TestSecureCommunication,
        TestPropertyTransactionProtocol,
        TestSecurityProperties
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    if result.wasSuccessful():
        print(f"\n✅ ALL TESTS PASSED - Protocol implementation verified!")
    else:
        print(f"\n❌ Some tests failed - Please review implementation")
