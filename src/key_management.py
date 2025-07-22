"""
Key Management Module for Property Transaction Protocol
Handles RSA key generation, storage, and management for all parties
"""

import os
import json
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from typing import Tuple, Dict, Optional
import base64

class KeyManager:
    """Manages RSA key pairs for all parties in the transaction"""
    
    def __init__(self):
        self.keys = {}
        self.public_keys = {}
        
    def generate_rsa_keypair(self, key_size: int = 2048) -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        """
        Generate RSA key pair for digital signatures and encryption
        
        Args:
            key_size: Size of the RSA key (default 2048 bits)
            
        Returns:
            Tuple of (private_key, public_key)
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        
        return private_key, public_key
    
    def register_party(self, party_name: str) -> Dict[str, str]:
        """
        Register a new party and generate their key pair
        
        Args:
            party_name: Name of the party (e.g., 'hr', 'seller_solicitor', 'mrs_harvey')
            
        Returns:
            Dictionary containing serialized public key
        """
        private_key, public_key = self.generate_rsa_keypair()
        
        # Store keys
        self.keys[party_name] = private_key
        self.public_keys[party_name] = public_key
        
        # Serialize public key for sharing
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return {
            'party': party_name,
            'public_key': base64.b64encode(public_key_pem).decode('utf-8')
        }
    
    def get_private_key(self, party_name: str) -> Optional[rsa.RSAPrivateKey]:
        """Get private key for a party"""
        return self.keys.get(party_name)
    
    def get_public_key(self, party_name: str) -> Optional[rsa.RSAPublicKey]:
        """Get public key for a party"""
        return self.public_keys.get(party_name)
    
    def import_public_key(self, party_name: str, public_key_b64: str) -> None:
        """
        Import a public key from another party
        
        Args:
            party_name: Name of the party
            public_key_b64: Base64 encoded public key
        """
        public_key_pem = base64.b64decode(public_key_b64.encode('utf-8'))
        public_key = serialization.load_pem_public_key(
            public_key_pem,
            backend=default_backend()
        )
        self.public_keys[party_name] = public_key
    
    def save_keys_to_file(self, party_name: str, filename: str) -> None:
        """Save party's keys to file"""
        if party_name not in self.keys:
            raise ValueError(f"No keys found for party: {party_name}")
        
        private_key = self.keys[party_name]
        public_key = self.public_keys[party_name]
        
        # Serialize keys
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = public_key.public_key_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        key_data = {
            'party': party_name,
            'private_key': base64.b64encode(private_pem).decode('utf-8'),
            'public_key': base64.b64encode(public_pem).decode('utf-8')
        }
        
        with open(filename, 'w') as f:
            json.dump(key_data, f, indent=2)
    
    def load_keys_from_file(self, filename: str) -> str:
        """Load party's keys from file"""
        with open(filename, 'r') as f:
            key_data = json.load(f)
        
        party_name = key_data['party']
        
        # Deserialize private key
        private_pem = base64.b64decode(key_data['private_key'].encode('utf-8'))
        private_key = serialization.load_pem_private_key(
            private_pem,
            password=None,
            backend=default_backend()
        )
        
        # Deserialize public key
        public_pem = base64.b64decode(key_data['public_key'].encode('utf-8'))
        public_key = serialization.load_pem_public_key(
            public_pem,
            backend=default_backend()
        )
        
        self.keys[party_name] = private_key
        self.public_keys[party_name] = public_key
        
        return party_name

# Symmetric key management for AES
class SymmetricKeyManager:
    """Manages AES symmetric keys for secure communication"""
    
    def __init__(self):
        self.shared_keys = {}
    
    def generate_aes_key(self) -> bytes:
        """Generate a 256-bit AES key"""
        return os.urandom(32)  # 256 bits
    
    def store_shared_key(self, party1: str, party2: str, key: bytes) -> None:
        """Store shared symmetric key between two parties"""
        key_id = self._get_key_id(party1, party2)
        self.shared_keys[key_id] = key
    
    def get_shared_key(self, party1: str, party2: str) -> Optional[bytes]:
        """Get shared symmetric key between two parties"""
        key_id = self._get_key_id(party1, party2)
        return self.shared_keys.get(key_id)
    
    def _get_key_id(self, party1: str, party2: str) -> str:
        """Create consistent key ID for two parties"""
        parties = sorted([party1, party2])
        return f"{parties[0]}__{parties[1]}"
