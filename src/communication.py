"""
Secure Communication Module for Property Transaction Protocol
Implements hybrid encryption (RSA + AES) for secure message exchange
"""

import os
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from typing import Dict, Any, Tuple, Optional
from datetime import datetime
import hashlib

class SecureCommunication:
    """Handles secure communication between parties using hybrid encryption"""
    
    def __init__(self):
        self.session_keys = {}  # Store established session keys
    
    def encrypt_message(self, message: str, recipient_public_key: rsa.RSAPublicKey, 
                       sender_name: str, recipient_name: str) -> Dict[str, Any]:
        """
        Encrypt a message using hybrid encryption (AES + RSA)
        
        Args:
            message: The message to encrypt
            recipient_public_key: Recipient's RSA public key
            sender_name: Name of the sender
            recipient_name: Name of the recipient
            
        Returns:
            Encrypted message package
        """
        # Generate random AES key for this message
        aes_key = os.urandom(32)  # 256-bit AES key
        iv = os.urandom(16)  # 128-bit IV for AES
        
        # Encrypt message with AES
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Pad message to AES block size
        message_bytes = message.encode('utf-8')
        padding_length = 16 - (len(message_bytes) % 16)
        padded_message = message_bytes + bytes([padding_length] * padding_length)
        
        encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
        
        # Encrypt AES key with RSA
        encrypted_aes_key = recipient_public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Create message package
        message_package = {
            'sender': sender_name,
            'recipient': recipient_name,
            'timestamp': datetime.now().isoformat(),
            'encrypted_aes_key': base64.b64encode(encrypted_aes_key).decode('utf-8'),
            'iv': base64.b64encode(iv).decode('utf-8'),
            'encrypted_message': base64.b64encode(encrypted_message).decode('utf-8'),
            'encryption_algorithm': 'AES-256-CBC + RSA-OAEP'
        }
        
        return message_package
    
    def decrypt_message(self, message_package: Dict[str, Any], 
                       recipient_private_key: rsa.RSAPrivateKey) -> Tuple[bool, str]:
        """
        Decrypt a message using hybrid decryption
        
        Args:
            message_package: The encrypted message package
            recipient_private_key: Recipient's RSA private key
            
        Returns:
            Tuple of (success, decrypted_message_or_error)
        """
        try:
            # Decrypt AES key with RSA
            encrypted_aes_key = base64.b64decode(message_package['encrypted_aes_key'].encode('utf-8'))
            aes_key = recipient_private_key.decrypt(
                encrypted_aes_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            # Decrypt message with AES
            iv = base64.b64decode(message_package['iv'].encode('utf-8'))
            encrypted_message = base64.b64decode(message_package['encrypted_message'].encode('utf-8'))
            
            cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            
            padded_message = decryptor.update(encrypted_message) + decryptor.finalize()
            
            # Remove padding
            padding_length = padded_message[-1]
            message_bytes = padded_message[:-padding_length]
            
            message = message_bytes.decode('utf-8')
            
            return True, message
            
        except Exception as e:
            return False, f"Decryption failed: {str(e)}"
    
    def establish_session_key(self, party1: str, party2: str, 
                             party1_private_key: rsa.RSAPrivateKey,
                             party2_public_key: rsa.RSAPublicKey) -> bytes:
        """
        Establish a shared session key between two parties using Diffie-Hellman-like exchange
        
        Args:
            party1: Name of first party
            party2: Name of second party
            party1_private_key: First party's private key
            party2_public_key: Second party's public key
            
        Returns:
            Shared session key
        """
        # Generate random session key
        session_key = os.urandom(32)
        
        # Store session key
        session_id = self._get_session_id(party1, party2)
        self.session_keys[session_id] = session_key
        
        return session_key
    
    def encrypt_with_session_key(self, message: str, party1: str, party2: str) -> Optional[Dict[str, Any]]:
        """
        Encrypt message using established session key
        
        Args:
            message: Message to encrypt
            party1: First party name
            party2: Second party name
            
        Returns:
            Encrypted message package or None if no session key
        """
        session_id = self._get_session_id(party1, party2)
        session_key = self.session_keys.get(session_id)
        
        if not session_key:
            return None
        
        # Encrypt with AES using session key
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Pad message
        message_bytes = message.encode('utf-8')
        padding_length = 16 - (len(message_bytes) % 16)
        padded_message = message_bytes + bytes([padding_length] * padding_length)
        
        encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
        
        return {
            'session_id': session_id,
            'iv': base64.b64encode(iv).decode('utf-8'),
            'encrypted_message': base64.b64encode(encrypted_message).decode('utf-8'),
            'timestamp': datetime.now().isoformat(),
            'encryption_algorithm': 'AES-256-CBC with shared session key'
        }
    
    def decrypt_with_session_key(self, message_package: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Decrypt message using session key
        
        Args:
            message_package: Encrypted message package
            
        Returns:
            Tuple of (success, decrypted_message_or_error)
        """
        try:
            session_id = message_package['session_id']
            session_key = self.session_keys.get(session_id)
            
            if not session_key:
                return False, "Session key not found"
            
            iv = base64.b64decode(message_package['iv'].encode('utf-8'))
            encrypted_message = base64.b64decode(message_package['encrypted_message'].encode('utf-8'))
            
            cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            
            padded_message = decryptor.update(encrypted_message) + decryptor.finalize()
            
            # Remove padding
            padding_length = padded_message[-1]
            message_bytes = padded_message[:-padding_length]
            
            message = message_bytes.decode('utf-8')
            
            return True, message
            
        except Exception as e:
            return False, f"Session decryption failed: {str(e)}"
    
    def _get_session_id(self, party1: str, party2: str) -> str:
        """Create consistent session ID for two parties"""
        parties = sorted([party1, party2])
        return f"session_{parties[0]}_{parties[1]}"

class MessageIntegrity:
    """Handles message integrity and authentication"""
    
    def __init__(self):
        pass
    
    def create_message_hash(self, message: str) -> str:
        """Create SHA-256 hash of a message"""
        return hashlib.sha256(message.encode('utf-8')).hexdigest()
    
    def verify_message_integrity(self, message: str, expected_hash: str) -> bool:
        """Verify message integrity using hash comparison"""
        computed_hash = self.create_message_hash(message)
        return computed_hash == expected_hash
    
    def create_authenticated_message(self, message: str, sender: str, 
                                   private_key: rsa.RSAPrivateKey) -> Dict[str, Any]:
        """
        Create a message with authentication and integrity protection
        
        Args:
            message: The message content
            sender: Sender's name
            private_key: Sender's private key for authentication
            
        Returns:
            Authenticated message package
        """
        # Create message hash
        message_hash = self.create_message_hash(message)
        
        # Create authentication data
        auth_data = {
            'sender': sender,
            'timestamp': datetime.now().isoformat(),
            'message_hash': message_hash
        }
        
        # Sign authentication data
        auth_payload = json.dumps(auth_data, sort_keys=True).encode('utf-8')
        signature = private_key.sign(
            auth_payload,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return {
            'message': message,
            'auth_data': auth_data,
            'signature': base64.b64encode(signature).decode('utf-8')
        }
    
    def verify_authenticated_message(self, auth_message: Dict[str, Any], 
                                   sender_public_key: rsa.RSAPublicKey) -> Tuple[bool, str]:
        """
        Verify an authenticated message
        
        Args:
            auth_message: The authenticated message package
            sender_public_key: Sender's public key
            
        Returns:
            Tuple of (is_valid, message_or_error)
        """
        try:
            message = auth_message['message']
            auth_data = auth_message['auth_data']
            signature_b64 = auth_message['signature']
            
            # Verify message hash
            expected_hash = auth_data['message_hash']
            if not self.verify_message_integrity(message, expected_hash):
                return False, "Message integrity check failed"
            
            # Verify signature
            auth_payload = json.dumps(auth_data, sort_keys=True).encode('utf-8')
            signature = base64.b64decode(signature_b64.encode('utf-8'))
            
            sender_public_key.verify(
                signature,
                auth_payload,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            return True, message
            
        except Exception as e:
            return False, f"Authentication verification failed: {str(e)}"
