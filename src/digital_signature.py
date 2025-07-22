"""
Digital Signature Module for Property Transaction Protocol
Implements RSA-PSS digital signatures for contract authentication
"""

import base64
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from typing import Tuple, Dict, Any
import json
from datetime import datetime

class DigitalSignature:
    """Handles digital signature creation and verification"""
    
    def __init__(self):
        pass
    
    def sign_document(self, document: str, private_key: rsa.RSAPrivateKey, signer_info: Dict[str, str]) -> Dict[str, Any]:
        """
        Create a digital signature for a document using RSA-PSS
        
        Args:
            document: The document content to sign
            private_key: RSA private key for signing
            signer_info: Information about the signer
            
        Returns:
            Dictionary containing the signature and metadata
        """
        # Create document hash
        document_bytes = document.encode('utf-8')
        document_hash = hashlib.sha256(document_bytes).hexdigest()
        
        # Create signature metadata
        signature_data = {
            'document_hash': document_hash,
            'signer': signer_info,
            'timestamp': datetime.now().isoformat(),
            'algorithm': 'RSA-PSS with SHA-256'
        }
        
        # Serialize signature data for signing
        signature_payload = json.dumps(signature_data, sort_keys=True)
        signature_payload_bytes = signature_payload.encode('utf-8')
        
        # Create digital signature using RSA-PSS
        signature = private_key.sign(
            signature_payload_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return {
            'signature_data': signature_data,
            'signature': base64.b64encode(signature).decode('utf-8'),
            'document': document
        }
    
    def verify_signature(self, signed_document: Dict[str, Any], public_key: rsa.RSAPublicKey) -> Tuple[bool, str]:
        """
        Verify a digital signature
        
        Args:
            signed_document: The signed document with signature
            public_key: RSA public key for verification
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Extract components
            document = signed_document['document']
            signature_data = signed_document['signature_data']
            signature_b64 = signed_document['signature']
            
            # Verify document hash
            document_bytes = document.encode('utf-8')
            computed_hash = hashlib.sha256(document_bytes).hexdigest()
            
            if computed_hash != signature_data['document_hash']:
                return False, "Document has been tampered with - hash mismatch"
            
            # Recreate signature payload
            signature_payload = json.dumps(signature_data, sort_keys=True)
            signature_payload_bytes = signature_payload.encode('utf-8')
            
            # Decode signature
            signature = base64.b64decode(signature_b64.encode('utf-8'))
            
            # Verify signature
            public_key.verify(
                signature,
                signature_payload_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            return True, "Signature verified successfully"
            
        except Exception as e:
            return False, f"Signature verification failed: {str(e)}"
    
    def create_contract_signature(self, contract_content: str, party_name: str, 
                                party_role: str, private_key: rsa.RSAPrivateKey) -> Dict[str, Any]:
        """
        Create a legally binding digital signature for a contract
        
        Args:
            contract_content: The contract text
            party_name: Name of the signing party
            party_role: Role of the party (buyer, seller, solicitor)
            private_key: Private key for signing
            
        Returns:
            Signed contract with legal metadata
        """
        signer_info = {
            'name': party_name,
            'role': party_role,
            'intent': 'Legal agreement acceptance',
            'jurisdiction': 'UK'
        }
        
        signed_contract = self.sign_document(contract_content, private_key, signer_info)
        
        # Add legal binding statement
        signed_contract['legal_statement'] = (
            "This digital signature constitutes a legally binding agreement "
            "under UK Electronic Communications Act 2000 and Electronic "
            "Signatures Regulations 2002."
        )
        
        return signed_contract
    
    def verify_contract_signature(self, signed_contract: Dict[str, Any], 
                                public_key: rsa.RSAPublicKey) -> Tuple[bool, Dict[str, Any]]:
        """
        Verify a contract signature and return verification details
        
        Args:
            signed_contract: The signed contract
            public_key: Public key for verification
            
        Returns:
            Tuple of (is_valid, verification_details)
        """
        is_valid, message = self.verify_signature(signed_contract, public_key)
        
        verification_details = {
            'is_valid': is_valid,
            'message': message,
            'signer_info': signed_contract.get('signature_data', {}).get('signer', {}),
            'timestamp': signed_contract.get('signature_data', {}).get('timestamp', ''),
            'algorithm': signed_contract.get('signature_data', {}).get('algorithm', ''),
            'legal_validity': is_valid and 'UK' in signed_contract.get('signature_data', {}).get('signer', {}).get('jurisdiction', '')
        }
        
        return is_valid, verification_details

class ContractManager:
    """Manages contract creation and validation"""
    
    def __init__(self):
        self.digital_signature = DigitalSignature()
    
    def create_property_contract(self, seller_info: Dict[str, str], 
                               buyer_info: Dict[str, str], 
                               property_details: Dict[str, str]) -> str:
        """
        Create a property transaction contract
        
        Args:
            seller_info: Seller details
            buyer_info: Buyer details
            property_details: Property transaction details
            
        Returns:
            Contract text
        """
        contract_template = f"""
PROPERTY PURCHASE AGREEMENT

This agreement is made between:

SELLER:
Name: {seller_info.get('name', '')}
Address: {seller_info.get('address', '')}
Represented by: {seller_info.get('solicitor', '')}

BUYER:
Name: {buyer_info.get('name', '')}
Address: {buyer_info.get('address', '')}
Represented by: {buyer_info.get('solicitor', '')}

PROPERTY DETAILS:
Address: {property_details.get('address', '')}
Description: {property_details.get('description', '')}
Purchase Price: £{property_details.get('price', '')}
Completion Date: {property_details.get('completion_date', '')}

TERMS AND CONDITIONS:
1. The Buyer agrees to purchase the Property for the stated purchase price.
2. The transaction is subject to satisfactory surveys and searches.
3. Completion shall take place on the agreed completion date.
4. This agreement is governed by English Law.

Digital signatures below constitute legal acceptance of these terms.

Contract ID: {property_details.get('contract_id', '')}
Date: {datetime.now().strftime('%Y-%m-%d')}
        """
        
        return contract_template.strip()
    
    def add_signature_to_contract(self, contract: str, party_name: str, 
                                party_role: str, private_key: rsa.RSAPrivateKey) -> Dict[str, Any]:
        """Add a digital signature to a contract"""
        return self.digital_signature.create_contract_signature(
            contract, party_name, party_role, private_key
        )
