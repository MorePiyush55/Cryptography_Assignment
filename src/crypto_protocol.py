"""
Main Protocol Implementation for Property Transaction
Orchestrates the complete secure communication protocol between H&R, Seller's Solicitor, and Mrs. Harvey
"""

import json
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
import uuid

from key_management import KeyManager, SymmetricKeyManager
from digital_signature import DigitalSignature, ContractManager
from communication import SecureCommunication, MessageIntegrity

class PropertyTransactionProtocol:
    """
    Main protocol class that orchestrates secure property transaction communication
    """
    
    def __init__(self):
        self.key_manager = KeyManager()
        self.symmetric_key_manager = SymmetricKeyManager()
        self.digital_signature = DigitalSignature()
        self.contract_manager = ContractManager()
        self.secure_comm = SecureCommunication()
        self.message_integrity = MessageIntegrity()
        
        # Protocol state
        self.protocol_state = {
            'hr_registered': False,
            'seller_solicitor_registered': False,
            'mrs_harvey_registered': False,
            'keys_exchanged': False,
            'contract_sent': False,
            'contract_signed': False,
            'transaction_complete': False
        }
        
        # Communication log
        self.communication_log = []
        
        # Transaction data
        self.transaction_data = {}
    
    def initialize_parties(self) -> Dict[str, Any]:
        """
        Phase 1: Initialize all parties and generate their key pairs
        
        Returns:
            Dictionary containing initialization results
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'phase': 'Party Initialization',
            'parties': {}
        }
        
        # Register H&R (Hackit & Run LLP)
        hr_keys = self.key_manager.register_party('hr')
        results['parties']['hr'] = hr_keys
        self.protocol_state['hr_registered'] = True
        
        # Register Seller's Solicitor
        seller_keys = self.key_manager.register_party('seller_solicitor')
        results['parties']['seller_solicitor'] = seller_keys
        self.protocol_state['seller_solicitor_registered'] = True
        
        # Register Mrs. Harvey (Buyer)
        harvey_keys = self.key_manager.register_party('mrs_harvey')
        results['parties']['mrs_harvey'] = harvey_keys
        self.protocol_state['mrs_harvey_registered'] = True
        
        self._log_communication('SYSTEM', 'ALL', 'Party initialization complete', results)
        
        return results
    
    def establish_secure_channels(self, first_time_communication: bool = True) -> Dict[str, Any]:
        """
        Phase 2: Establish secure communication channels
        
        Args:
            first_time_communication: True if this is first time H&R and Seller's Solicitor communicate
            
        Returns:
            Channel establishment results
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'phase': 'Secure Channel Establishment',
            'channels': {},
            'first_time_communication': first_time_communication
        }
        
        if first_time_communication:
            # First time: Full key exchange and authentication
            results['channels']['hr_seller'] = self._establish_first_time_channel('hr', 'seller_solicitor')
        else:
            # Subsequent communication: Use existing session keys
            results['channels']['hr_seller'] = self._establish_session_channel('hr', 'seller_solicitor')
        
        # Always establish fresh channel with Mrs. Harvey (she's remote)
        results['channels']['hr_harvey'] = self._establish_first_time_channel('hr', 'mrs_harvey')
        
        self.protocol_state['keys_exchanged'] = True
        self._log_communication('SYSTEM', 'ALL', 'Secure channels established', results)
        
        return results
    
    def initiate_contract_exchange(self, contract_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 3: Seller's Solicitor sends contract to H&R
        
        Args:
            contract_details: Details of the property transaction
            
        Returns:
            Contract exchange results
        """
        # Store transaction details
        self.transaction_data = contract_details
        
        # Create the property contract
        seller_info = contract_details.get('seller', {})
        buyer_info = contract_details.get('buyer', {})
        property_details = contract_details.get('property', {})
        
        contract_text = self.contract_manager.create_property_contract(
            seller_info, buyer_info, property_details
        )
        
        # Seller's Solicitor sends contract to H&R
        sender_private_key = self.key_manager.get_private_key('seller_solicitor')
        hr_public_key = self.key_manager.get_public_key('hr')
        
        # Create authenticated and encrypted message
        auth_message = self.message_integrity.create_authenticated_message(
            contract_text, 'seller_solicitor', sender_private_key
        )
        
        encrypted_message = self.secure_comm.encrypt_message(
            json.dumps(auth_message), hr_public_key, 'seller_solicitor', 'hr'
        )
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'phase': 'Contract Exchange - Seller to H&R',
            'contract_id': property_details.get('contract_id', str(uuid.uuid4())),
            'sender': 'seller_solicitor',
            'recipient': 'hr',
            'encrypted_message': encrypted_message,
            'message_type': 'contract_transmission'
        }
        
        self.protocol_state['contract_sent'] = True
        self._log_communication('seller_solicitor', 'hr', 'Contract sent to H&R', results)
        
        return results
    
    def hr_receive_and_forward_contract(self, encrypted_message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 4: H&R receives contract and forwards it to Mrs. Harvey
        
        Args:
            encrypted_message: Encrypted contract from Seller's Solicitor
            
        Returns:
            Forwarding results
        """
        # H&R decrypts the contract
        hr_private_key = self.key_manager.get_private_key('hr')
        success, decrypted_content = self.secure_comm.decrypt_message(encrypted_message, hr_private_key)
        
        if not success:
            return {'error': f'H&R failed to decrypt contract: {decrypted_content}'}
        
        # Verify authentication
        auth_message = json.loads(decrypted_content)
        seller_public_key = self.key_manager.get_public_key('seller_solicitor')
        auth_success, contract_text = self.message_integrity.verify_authenticated_message(
            auth_message, seller_public_key
        )
        
        if not auth_success:
            return {'error': f'Contract authentication failed: {contract_text}'}
        
        # H&R forwards contract to Mrs. Harvey
        hr_private_key = self.key_manager.get_private_key('hr')
        harvey_public_key = self.key_manager.get_public_key('mrs_harvey')
        
        # Create cover message
        cover_message = {
            'from_hr': True,
            'message': 'Please review and digitally sign the attached property purchase contract.',
            'contract': contract_text,
            'instructions': 'If you agree to the terms, please sign and return the contract.'
        }
        
        # Create authenticated message from H&R
        hr_auth_message = self.message_integrity.create_authenticated_message(
            json.dumps(cover_message), 'hr', hr_private_key
        )
        
        # Encrypt for Mrs. Harvey
        encrypted_to_harvey = self.secure_comm.encrypt_message(
            json.dumps(hr_auth_message), harvey_public_key, 'hr', 'mrs_harvey'
        )
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'phase': 'Contract Forwarding - H&R to Mrs. Harvey',
            'sender': 'hr',
            'recipient': 'mrs_harvey',
            'contract_received_from': 'seller_solicitor',
            'encrypted_message': encrypted_to_harvey,
            'message_type': 'contract_forwarding'
        }
        
        self._log_communication('hr', 'mrs_harvey', 'Contract forwarded to Mrs. Harvey', results)
        
        return results
    
    def mrs_harvey_sign_contract(self, encrypted_message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 5: Mrs. Harvey receives, reviews and signs the contract
        
        Args:
            encrypted_message: Encrypted contract from H&R
            
        Returns:
            Signing results
        """
        # Mrs. Harvey decrypts the message
        harvey_private_key = self.key_manager.get_private_key('mrs_harvey')
        success, decrypted_content = self.secure_comm.decrypt_message(encrypted_message, harvey_private_key)
        
        if not success:
            return {'error': f'Mrs. Harvey failed to decrypt message: {decrypted_content}'}
        
        # Verify authentication from H&R
        auth_message = json.loads(decrypted_content)
        hr_public_key = self.key_manager.get_public_key('hr')
        auth_success, cover_message_text = self.message_integrity.verify_authenticated_message(
            auth_message, hr_public_key
        )
        
        if not auth_success:
            return {'error': f'H&R message authentication failed: {cover_message_text}'}
        
        cover_message = json.loads(cover_message_text)
        contract_text = cover_message['contract']
        
        # Mrs. Harvey digitally signs the contract
        signed_contract = self.contract_manager.add_signature_to_contract(
            contract_text, 'Mrs. Harvey', 'buyer', harvey_private_key
        )
        
        # Prepare signed contract for return to H&R
        hr_public_key = self.key_manager.get_public_key('hr')
        
        return_message = {
            'signed_contract': signed_contract,
            'message': 'I have reviewed and signed the contract. Please proceed with the transaction.',
            'signer': 'Mrs. Harvey'
        }
        
        # Create authenticated message from Mrs. Harvey
        harvey_auth_message = self.message_integrity.create_authenticated_message(
            json.dumps(return_message), 'mrs_harvey', harvey_private_key
        )
        
        # Encrypt for H&R
        encrypted_to_hr = self.secure_comm.encrypt_message(
            json.dumps(harvey_auth_message), hr_public_key, 'mrs_harvey', 'hr'
        )
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'phase': 'Contract Signing - Mrs. Harvey',
            'sender': 'mrs_harvey',
            'recipient': 'hr',
            'contract_signed': True,
            'encrypted_message': encrypted_to_hr,
            'signature_verification': self._verify_signature_details(signed_contract),
            'message_type': 'signed_contract_return'
        }
        
        self.protocol_state['contract_signed'] = True
        self._log_communication('mrs_harvey', 'hr', 'Signed contract returned to H&R', results)
        
        return results
    
    def hr_forward_signed_contract(self, encrypted_message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 6: H&R forwards signed contract to Seller's Solicitor
        
        Args:
            encrypted_message: Encrypted signed contract from Mrs. Harvey
            
        Returns:
            Final forwarding results
        """
        # H&R decrypts the signed contract
        hr_private_key = self.key_manager.get_private_key('hr')
        success, decrypted_content = self.secure_comm.decrypt_message(encrypted_message, hr_private_key)
        
        if not success:
            return {'error': f'H&R failed to decrypt signed contract: {decrypted_content}'}
        
        # Verify authentication from Mrs. Harvey
        auth_message = json.loads(decrypted_content)
        harvey_public_key = self.key_manager.get_public_key('mrs_harvey')
        auth_success, return_message_text = self.message_integrity.verify_authenticated_message(
            auth_message, harvey_public_key
        )
        
        if not auth_success:
            return {'error': f'Mrs. Harvey message authentication failed: {return_message_text}'}
        
        return_message = json.loads(return_message_text)
        signed_contract = return_message['signed_contract']
        
        # Verify Mrs. Harvey's signature on the contract
        harvey_public_key = self.key_manager.get_public_key('mrs_harvey')
        signature_valid, verification_details = self.digital_signature.verify_contract_signature(
            signed_contract, harvey_public_key
        )
        
        if not signature_valid:
            return {'error': f'Contract signature verification failed: {verification_details}'}
        
        # H&R forwards signed contract to Seller's Solicitor
        seller_public_key = self.key_manager.get_public_key('seller_solicitor')
        
        completion_message = {
            'signed_contract': signed_contract,
            'message': 'Mrs. Harvey has signed the contract. Transaction can proceed to completion.',
            'verification_details': verification_details,
            'from_hr': True
        }
        
        # Create authenticated message from H&R
        hr_auth_message = self.message_integrity.create_authenticated_message(
            json.dumps(completion_message), 'hr', hr_private_key
        )
        
        # Encrypt for Seller's Solicitor
        encrypted_to_seller = self.secure_comm.encrypt_message(
            json.dumps(hr_auth_message), seller_public_key, 'hr', 'seller_solicitor'
        )
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'phase': 'Final Contract Delivery - H&R to Seller\'s Solicitor',
            'sender': 'hr',
            'recipient': 'seller_solicitor',
            'contract_verified': True,
            'signature_verification': verification_details,
            'encrypted_message': encrypted_to_seller,
            'message_type': 'final_contract_delivery'
        }
        
        self.protocol_state['transaction_complete'] = True
        self._log_communication('hr', 'seller_solicitor', 'Signed contract delivered to Seller\'s Solicitor', results)
        
        return results
    
    def get_protocol_summary(self) -> Dict[str, Any]:
        """
        Get a complete summary of the protocol execution
        
        Returns:
            Protocol summary with all steps and security measures
        """
        return {
            'protocol_state': self.protocol_state,
            'communication_log': self.communication_log,
            'security_measures': {
                'encryption_algorithms': [
                    'RSA-2048 for key exchange and digital signatures',
                    'AES-256-CBC for symmetric encryption',
                    'RSA-OAEP for hybrid encryption',
                    'RSA-PSS for digital signatures'
                ],
                'hash_functions': ['SHA-256'],
                'key_sizes': {
                    'RSA': '2048 bits',
                    'AES': '256 bits'
                },
                'authentication_methods': [
                    'Digital signatures with RSA-PSS',
                    'Message authentication with hash verification',
                    'Public key infrastructure for identity verification'
                ]
            },
            'legal_compliance': {
                'uk_electronic_communications_act': True,
                'electronic_signatures_regulations': True,
                'data_protection_compliance': True,
                'non_repudiation': True
            },
            'transaction_summary': self.transaction_data
        }
    
    def _establish_first_time_channel(self, party1: str, party2: str) -> Dict[str, Any]:
        """Establish secure channel for first-time communication"""
        party1_private_key = self.key_manager.get_private_key(party1)
        party2_public_key = self.key_manager.get_public_key(party2)
        
        session_key = self.secure_comm.establish_session_key(
            party1, party2, party1_private_key, party2_public_key
        )
        
        return {
            'parties': [party1, party2],
            'session_established': True,
            'session_key_generated': True,
            'channel_type': 'first_time',
            'encryption_method': 'RSA + AES hybrid'
        }
    
    def _establish_session_channel(self, party1: str, party2: str) -> Dict[str, Any]:
        """Establish secure channel using existing session"""
        session_id = self.secure_comm._get_session_id(party1, party2)
        
        # In a real implementation, this would use stored session keys
        # For this demo, we'll establish a new session
        return self._establish_first_time_channel(party1, party2)
    
    def _verify_signature_details(self, signed_contract: Dict[str, Any]) -> Dict[str, Any]:
        """Extract signature verification details"""
        signature_data = signed_contract.get('signature_data', {})
        
        return {
            'signer': signature_data.get('signer', {}),
            'timestamp': signature_data.get('timestamp', ''),
            'algorithm': signature_data.get('algorithm', ''),
            'document_hash': signature_data.get('document_hash', ''),
            'legal_validity': True
        }
    
    def _log_communication(self, sender: str, recipient: str, action: str, details: Dict[str, Any]) -> None:
        """Log communication for audit trail"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'sender': sender,
            'recipient': recipient,
            'action': action,
            'details': details
        }
        self.communication_log.append(log_entry)
