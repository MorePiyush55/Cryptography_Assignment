# Protocol Design Documentation

## Overview

This document describes the cryptographic protocol designed for secure property transactions between three parties: H&R (Hackit & Run LLP), the Seller's Solicitor, and Mrs. Harvey (the buyer).

## Protocol Objectives

### Primary Security Goals
1. **Confidentiality** - All communications must be encrypted to prevent eavesdropping
2. **Integrity** - Messages must be tamper-evident to detect unauthorized modifications
3. **Authenticity** - All parties must be able to verify the identity of message senders
4. **Non-repudiation** - Digital signatures must provide legally binding proof of agreement
5. **Availability** - The protocol must handle both first-time and repeat communications efficiently

### Legal Requirements
- Compliance with UK Electronic Communications Act 2000
- Compliance with Electronic Signatures Regulations 2002
- Enforceable under UK law
- Suitable for remote property transactions

## Protocol Architecture

### Party Roles

#### H&R (Hackit & Run LLP)
- Central coordinating solicitor
- Receives contracts from Seller's Solicitor
- Forwards contracts to Mrs. Harvey
- Returns signed contracts to Seller's Solicitor
- Acts as trusted intermediary

#### Seller's Solicitor
- Represents Mr. L.M. Facey (the seller)
- Initiates contract transmission
- Receives final signed contract
- No direct communication with Mrs. Harvey

#### Mrs. Harvey
- The buyer
- Receives contract through H&R
- Provides legally binding digital signature
- Returns signed contract through H&R

### Communication Flow

```
Seller's Solicitor ←→ H&R ←→ Mrs. Harvey
                      ↑
                 Central Hub
```

## Cryptographic Algorithms

### 1. RSA-2048 (Asymmetric Encryption)
**Usage**: Key exchange, digital signatures, identity verification

**Justification**:
- Industry standard with proven security
- 2048-bit keys provide adequate security until 2030+ (NIST recommendations)
- Widely supported and legally recognized
- Enables non-repudiation through digital signatures

**Implementation**:
- RSA-OAEP padding for encryption
- RSA-PSS padding for digital signatures
- SHA-256 as hash function

### 2. AES-256-CBC (Symmetric Encryption)
**Usage**: Bulk data encryption for contract content

**Justification**:
- Symmetric encryption is much faster than RSA for large documents
- 256-bit key provides military-grade security
- CBC mode with random IV ensures different ciphertexts for identical plaintexts
- FIPS-approved algorithm

**Implementation**:
- 256-bit randomly generated keys
- 128-bit random initialization vectors
- PKCS#7 padding for block alignment

### 3. Hybrid Encryption (RSA + AES)
**Usage**: Secure message transmission

**Process**:
1. Generate random AES-256 key for each message
2. Encrypt message content with AES-256-CBC
3. Encrypt AES key with recipient's RSA public key
4. Transmit encrypted AES key + encrypted message

**Benefits**:
- Combines RSA security with AES performance
- Each message uses unique symmetric key
- Forward secrecy for individual messages

### 4. SHA-256 (Cryptographic Hashing)
**Usage**: Message integrity, digital signatures, document fingerprinting

**Justification**:
- Collision-resistant cryptographic hash function
- Widely adopted standard
- Provides 128-bit security level
- Required for RSA-PSS signatures

## Protocol Phases

### Phase 1: Party Initialization
```
For each party (H&R, Seller's Solicitor, Mrs. Harvey):
1. Generate RSA-2048 key pair (private_key, public_key)
2. Store private key securely
3. Publish public key for other parties
4. Verify key authenticity (out-of-band if first contact)
```

### Phase 2: Secure Channel Establishment

#### Scenario A: First-time Communication
```
H&R ↔ Seller's Solicitor:
1. Exchange and verify public keys
2. Establish session parameters
3. Create audit trail for future communications

H&R ↔ Mrs. Harvey:
1. Exchange and verify public keys
2. Establish secure communication channel
```

#### Scenario B: Subsequent Communication
```
H&R ↔ Seller's Solicitor:
1. Use previously verified keys
2. Simplified authentication process
3. Maintain communication efficiency
```

### Phase 3: Contract Transmission (Seller's Solicitor → H&R)
```
1. Create property contract document
2. Generate SHA-256 hash of contract
3. Create authentication metadata (sender, timestamp, hash)
4. Sign metadata with RSA-PSS private key
5. Encrypt signed message with H&R's public key using hybrid encryption
6. Transmit encrypted message to H&R
```

### Phase 4: Contract Forwarding (H&R → Mrs. Harvey)
```
1. Decrypt message from Seller's Solicitor
2. Verify Seller's Solicitor signature
3. Validate contract integrity
4. Create forwarding message with instructions
5. Sign forwarding message with H&R private key
6. Encrypt for Mrs. Harvey using hybrid encryption
7. Transmit to Mrs. Harvey
```

### Phase 5: Contract Signing (Mrs. Harvey)
```
1. Decrypt message from H&R
2. Verify H&R signature and message integrity
3. Review contract content
4. Create digital signature on contract:
   - Generate contract hash
   - Create signature metadata (name, role, timestamp, jurisdiction)
   - Sign with RSA-PSS private key
5. Encrypt signed contract for return to H&R
6. Transmit signed contract
```

### Phase 6: Final Delivery (H&R → Seller's Solicitor)
```
1. Decrypt signed contract from Mrs. Harvey
2. Verify Mrs. Harvey's signature
3. Validate legal binding requirements
4. Create completion message
5. Sign and encrypt for Seller's Solicitor
6. Deliver final signed contract
```

## Security Analysis

### Threat Model

#### Passive Attacks
- **Eavesdropping**: Mitigated by AES-256 encryption
- **Traffic Analysis**: Limited by encrypted communications

#### Active Attacks
- **Man-in-the-Middle**: Prevented by RSA public key verification
- **Message Tampering**: Detected by SHA-256 integrity checks
- **Replay Attacks**: Mitigated by timestamps and unique message IDs

#### Insider Threats
- **Key Compromise**: Compartmentalized damage due to individual key pairs
- **Repudiation**: Prevented by non-reputable digital signatures

### Security Properties

#### Confidentiality
- All messages encrypted with AES-256
- Unique encryption keys per message
- No plaintext transmission

#### Integrity
- SHA-256 hashes detect tampering
- Digital signatures provide authenticity
- End-to-end verification

#### Authentication
- RSA digital signatures verify sender identity
- Public key infrastructure ensures party verification
- Legal-grade signature metadata

#### Non-repudiation
- RSA-PSS signatures are legally binding
- Timestamped signature metadata
- Compliant with UK electronic signature laws

#### Forward Secrecy
- Unique AES keys per message
- Compromise of one message doesn't affect others

## Protocol Strengths

### Cryptographic Strengths
1. **Multi-layered Security**: Combines multiple proven algorithms
2. **Industry Standards**: Uses NIST-approved cryptographic primitives
3. **Future-Proof**: Key sizes adequate for long-term security
4. **Performance Optimized**: Hybrid encryption balances security and speed

### Legal Strengths
1. **UK Law Compliance**: Meets Electronic Communications Act requirements
2. **Court Admissibility**: Digital signatures legally equivalent to handwritten
3. **Audit Trail**: Complete communication log for legal proceedings
4. **Professional Standards**: Suitable for solicitor-to-solicitor communications

### Operational Strengths
1. **Scalability**: Handles both first-time and repeat communications
2. **Reliability**: Robust error handling and verification
3. **Usability**: Clear process flow for all parties
4. **Interoperability**: Standard cryptographic formats

## Implementation Considerations

### Key Management
- Secure key generation using cryptographically secure random number generators
- Private key protection with appropriate access controls
- Public key distribution with authenticity verification
- Key lifecycle management for long-term use

### Message Format
- Structured JSON format for interoperability
- Base64 encoding for binary data transmission
- Standardized metadata for legal requirements
- Version control for protocol evolution

### Error Handling
- Graceful handling of decryption failures
- Clear error messages for debugging
- Fallback procedures for communication failures
- Recovery mechanisms for partial transmissions

### Performance Optimization
- Minimal cryptographic operations per message
- Efficient symmetric encryption for bulk data
- Optimized key sizes balancing security and performance
- Caching of verified public keys

This protocol design provides a comprehensive solution for secure property transactions that meets both technical security requirements and legal enforceability standards in the UK jurisdiction.
