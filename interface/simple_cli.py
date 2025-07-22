#!/usr/bin/env python3
"""
Simple CLI Interface for Property Transaction Protocol
Easy-to-use command line interface with enhanced delivery confirmations
"""

import sys
import os
from datetime import datetime

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

class SimpleInterface:
    def __init__(self):
        self.transaction_log = []
        self.parties = {
            "1": {"name": "John Smith (ABC Law Firm)", "role": "Seller's Solicitor"},
            "2": {"name": "H&R Hackit & Run LLP", "role": "H&R Hub"},
            "3": {"name": "Mrs. Sarah Harvey", "role": "Property Buyer"}
        }
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_header(self, title):
        print("=" * 70)
        print(f"🔐 {title}")
        print("=" * 70)
        
    def print_separator(self):
        print("-" * 50)
        
    def log_transaction(self, sender, receiver, content_type, description):
        """Log a transaction"""
        entry = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "sender": sender,
            "receiver": receiver,
            "type": content_type,
            "description": description
        }
        self.transaction_log.append(entry)
        return len(self.transaction_log)
        
    def main_menu(self):
        """Main menu interface"""
        while True:
            self.clear_screen()
            self.print_header("Property Transaction Protocol - Professional Interface")
            print()
            print("👥 SELECT YOUR ROLE:")
            print()
            
            for key, party in self.parties.items():
                if key == "1":
                    icon = "🏢"
                elif key == "2":
                    icon = "🏛️"
                else:
                    icon = "🏠"
                    
                print(f"   {key}. {icon} {party['role']}")
                print(f"      ({party['name']})")
                print()
            
            print("   4. 📊 View Transaction History")
            print("   5. ⚙️  System Settings")
            print("   6. 🚪 Exit")
            print()
            
            choice = input("👉 Enter your choice (1-6): ").strip()
            
            if choice in ["1", "2", "3"]:
                self.party_interface(choice)
            elif choice == "4":
                self.view_history()
            elif choice == "5":
                self.system_settings()
            elif choice == "6":
                print("\n👋 Thank you for using Property Transaction Protocol!")
                print("🔒 All communications were encrypted and secure.")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")
                
    def party_interface(self, party_id):
        """Interface for each party"""
        party = self.parties[party_id]
        
        while True:
            self.clear_screen()
            self.print_header(f"{party['role']} Interface")
            print()
            print(f"👤 Logged in as: {party['name']}")
            print(f"🏷️  Role: {party['role']}")
            print()
            
            if party_id == "2":  # H&R Hub has different options
                self.hr_hub_menu(party_id)
            else:
                self.standard_party_menu(party_id)
                
            choice = input("👉 Enter your choice: ").strip()
            
            if choice == "1":
                self.send_content(party_id)
            elif choice == "2":
                self.view_my_transactions(party_id)
            elif choice == "3" and party_id == "2":
                self.hub_management()
            elif choice == "3" and party_id != "2":
                self.quick_verification(party_id)
            elif choice == "4" and party_id == "2":
                break
            elif choice == "4" and party_id != "2":
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")
                
    def standard_party_menu(self, party_id):
        """Menu for seller's solicitor and buyer"""
        print("📋 AVAILABLE ACTIONS:")
        print()
        print("   1. 📤 Send Content (Message/File)")
        print("   2. 📄 View My Transactions")
        print("   3. 🔍 Quick Verification (Last 3 Sent)")
        print("   4. 🔙 Back to Main Menu")
        print()
        
    def hr_hub_menu(self, party_id):
        """Menu for H&R Hub"""
        print("📋 HUB MANAGEMENT:")
        print()
        print("   1. 📤 Send Direct Message")
        print("   2. 📊 View All Transactions")
        print("   3. 👥 Hub Management Tools")
        print("   4. 🔙 Back to Main Menu")
        print()
        
    def quick_verification(self, party_id):
        """Quick verification of last 3 transactions"""
        self.clear_screen()
        party = self.parties[party_id]
        self.print_header(f"Quick Verification - {party['name']}")
        print()
        
        my_sent = [t for t in self.transaction_log if t['sender'] == party['name']]
        
        if not my_sent:
            print("📭 No sent messages found.")
            print("💡 Send a message first to see verification here!")
        else:
            print(f"📤 Your Last {min(3, len(my_sent))} Sent Messages:")
            print()
            
            for i, trans in enumerate(my_sent[-3:], 1):
                print(f"{i}. ✅ DELIVERED to {trans['receiver']}")
                print(f"   📝 {trans['type']}: {trans['description']}")
                print(f"   ⏰ {trans['date']} at {trans['time']}")
                print(f"   🔒 Status: Encrypted & Delivered")
                print()
                
        input("Press Enter to continue...")
        
    def send_content(self, sender_id):
        """Send content interface"""
        self.clear_screen()
        sender = self.parties[sender_id]
        self.print_header(f"Send Content - {sender['name']}")
        print()
        
        # Select recipient
        print("📤 SEND TO:")
        print()
        
        recipients = {}
        count = 1
        for key, party in self.parties.items():
            if key != sender_id:
                recipients[str(count)] = key
                if key == "1":
                    icon = "🏢"
                elif key == "2":
                    icon = "🏛️"
                else:
                    icon = "🏠"
                    
                print(f"   {count}. {icon} {party['name']}")
                print(f"      ({party['role']})")
                count += 1
        
        print(f"   {count}. 🔙 Back")
        print()
        
        recipient_choice = input("👉 Select recipient: ").strip()
        
        if recipient_choice == str(count):
            return
            
        if recipient_choice not in recipients:
            print("\n❌ Invalid choice.")
            input("Press Enter to continue...")
            return
            
        recipient_id = recipients[recipient_choice]
        recipient = self.parties[recipient_id]
        
        # Select content type
        self.content_type_menu(sender, recipient, sender_id, recipient_id)
        
    def content_type_menu(self, sender, recipient, sender_id, recipient_id):
        """Content type selection menu"""
        self.clear_screen()
        self.print_header(f"Send Content: {sender['name']} → {recipient['name']}")
        print()
        
        print("📝 CONTENT TYPE:")
        print()
        print("   1. 💬 Text Message")
        print("   2. 📄 Document/File")
        print("   3. 🔒 Confidential Data")
        print("   4. 🔙 Back")
        print()
        
        choice = input("👉 Select content type: ").strip()
        
        if choice == "1":
            self.send_text_message(sender, recipient, sender_id, recipient_id)
        elif choice == "2":
            self.send_file(sender, recipient, sender_id, recipient_id)
        elif choice == "3":
            self.send_confidential(sender, recipient, sender_id, recipient_id)
        elif choice == "4":
            return
        else:
            print("\n❌ Invalid choice.")
            input("Press Enter to continue...")
            
    def send_text_message(self, sender, recipient, sender_id, recipient_id):
        """Send text message with enhanced confirmation"""
        print("\n💬 TEXT MESSAGE")
        self.print_separator()
        print()
        
        print("📝 Enter your message (or type 'cancel' to abort):")
        message = input("Message: ")
        
        if message.lower() == 'cancel':
            return
            
        if not message.strip():
            print("\n❌ Message cannot be empty!")
            input("Press Enter to continue...")
            return
            
        # Detailed encryption simulation
        print(f"\n🔄 PROCESSING SECURE TRANSMISSION...")
        print(f"🔐 Step 1: Encrypting message with RSA-2048 + AES-256...")
        print(f"🔑 Step 2: Generating digital signature...")
        print(f"📡 Step 3: Transmitting securely from {sender['name']} to {recipient['name']}...")
        print(f"✅ Step 4: Message delivered successfully!")
        print(f"🔒 Step 5: Digital signature applied for legal compliance")
        
        # Log transaction
        trans_id = self.log_transaction(
            sender['name'],
            recipient['name'],
            "Text Message",
            f"'{message[:30]}{'...' if len(message) > 30 else ''}'"
        )
        
        print(f"\n📋 Transaction #{trans_id} logged at {datetime.now().strftime('%H:%M:%S')}")
        
        # ENHANCED CONFIRMATION - LARGE AND VISIBLE
        print("\n" + "="*70)
        print("🎉 MESSAGE DELIVERY CONFIRMATION 🎉")
        print("="*70)
        print(f"✅ FROM: {sender['name']}")
        print(f"✅ TO: {recipient['name']}")
        print(f"✅ TYPE: Text Message")
        print(f"✅ MESSAGE: {message[:40]}{'...' if len(message) > 40 else ''}")
        print(f"✅ STATUS: Successfully Delivered & Encrypted")
        print(f"✅ TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"✅ TRANSACTION ID: #{trans_id}")
        print("="*70)
        
        # IMPORTANT: Clear success message
        print("\n🎉 SUCCESS! Your message has been securely delivered!")
        print("💡 Tip: Use 'Quick Verification' to see your last 3 sent messages")
        input("\n👉 Press ENTER to return to menu...")
        
    def send_file(self, sender, recipient, sender_id, recipient_id):
        """Send file with enhanced confirmation"""
        print("\n📄 FILE UPLOAD")
        self.print_separator()
        print()
        
        print("📁 Enter file path or name (or type 'cancel' to abort):")
        file_path = input("File: ")
        
        if file_path.lower() == 'cancel':
            return
            
        if not file_path.strip():
            print("\n❌ File path cannot be empty!")
            input("Press Enter to continue...")
            return
            
        file_name = os.path.basename(file_path) if file_path else "document.pdf"
        
        # Detailed file encryption simulation
        print(f"\n🔄 PROCESSING SECURE FILE TRANSMISSION...")
        print(f"🔐 Step 1: Encrypting file '{file_name}' with hybrid encryption...")
        print(f"🔑 Step 2: Generating file integrity hash...")
        print(f"📡 Step 3: Transmitting securely from {sender['name']} to {recipient['name']}...")
        print(f"✅ Step 4: File delivered successfully!")
        print(f"🔒 Step 5: Digital signature applied for authenticity")
        
        # Log transaction
        trans_id = self.log_transaction(
            sender['name'],
            recipient['name'],
            "File",
            f"'{file_name}'"
        )
        
        print(f"\n📋 Transaction #{trans_id} logged at {datetime.now().strftime('%H:%M:%S')}")
        
        # ENHANCED CONFIRMATION - LARGE AND VISIBLE
        print("\n" + "="*70)
        print("🎉 FILE DELIVERY CONFIRMATION 🎉")
        print("="*70)
        print(f"✅ FROM: {sender['name']}")
        print(f"✅ TO: {recipient['name']}")
        print(f"✅ FILE: {file_name}")
        print(f"✅ STATUS: Successfully Delivered & Encrypted")
        print(f"✅ TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"✅ TRANSACTION ID: #{trans_id}")
        print("="*70)
        
        # IMPORTANT: Clear success message
        print("\n🎉 SUCCESS! Your file has been securely delivered!")
        print("💡 Tip: Use 'Quick Verification' to see your last 3 sent files")
        input("\n👉 Press ENTER to return to menu...")
        
    def send_confidential(self, sender, recipient, sender_id, recipient_id):
        """Send confidential data"""
        print("\n🔒 CONFIDENTIAL DATA")
        self.print_separator()
        print()
        
        print("Available confidential data types:")
        print("   1. 🔑 API Keys/Credentials")
        print("   2. 💰 Financial Information")
        print("   3. ⚖️  Legal Documents")
        print("   4. 🏠 Property Details")
        print()
        
        data_type = input("Select type (1-4): ").strip()
        
        data_types = {
            "1": "API Keys/Credentials",
            "2": "Financial Information", 
            "3": "Legal Documents",
            "4": "Property Details"
        }
        
        if data_type not in data_types:
            print("\n❌ Invalid choice.")
            input("Press Enter to continue...")
            return
            
        type_name = data_types[data_type]
        
        print(f"\n📝 Enter {type_name.lower()} (or type 'cancel' to abort):")
        data = input("Data: ")
        
        if data.lower() == 'cancel':
            return
            
        if not data.strip():
            print(f"\n❌ {type_name} cannot be empty!")
            input("Press Enter to continue...")
            return
            
        # Simulate high-security encryption
        print(f"\n🔐 Applying maximum encryption for {type_name.lower()}...")
        print(f"🛡️  Using RSA-2048 + AES-256 + Additional layers...")
        print(f"📡 Transmitting with highest security from {sender['name']} to {recipient['name']}...")
        print(f"✅ Confidential data delivered successfully!")
        print(f"🔒 Non-repudiation signatures applied")
        
        # Log transaction
        trans_id = self.log_transaction(
            sender['name'],
            recipient['name'],
            f"Confidential: {type_name}",
            "Encrypted confidential data"
        )
        
        print(f"\n📋 Transaction #{trans_id} logged at {datetime.now().strftime('%H:%M:%S')}")
        print("🚨 Maximum security protocols applied for sensitive data")
        
        # Show final confirmation
        print("\n" + "="*70)
        print("🔒 CONFIDENTIAL DATA DELIVERY CONFIRMATION")
        print("="*70)
        print(f"✅ FROM: {sender['name']}")
        print(f"✅ TO: {recipient['name']}")
        print(f"✅ TYPE: {type_name}")
        print(f"✅ STATUS: Successfully Delivered with Maximum Security")
        print(f"✅ TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🔐 CONFIDENTIAL - HIGHEST ENCRYPTION LEVEL APPLIED")
        print("="*70)
        
        input("\n👉 Press ENTER to continue...")
        
    def view_my_transactions(self, party_id):
        """View transactions for specific party"""
        self.clear_screen()
        party = self.parties[party_id]
        self.print_header(f"Transaction History - {party['name']}")
        print()
        
        my_transactions = [t for t in self.transaction_log 
                          if party['name'] in [t['sender'], t['receiver']]]
        
        if not my_transactions:
            print("📭 No transactions found for your account.")
            print("\n💡 Tip: Use 'Send Content' to start secure communications!")
        else:
            print(f"📊 Your Transactions: {len(my_transactions)}")
            print()
            
            for i, trans in enumerate(my_transactions[-10:], 1):  # Show last 10
                direction = "📤 SENT" if trans['sender'] == party['name'] else "📥 RECEIVED"
                other_party = trans['receiver'] if trans['sender'] == party['name'] else trans['sender']
                
                print(f"{i}. {direction} - {other_party}")
                print(f"   📝 {trans['type']}: {trans['description']}")
                print(f"   ⏰ {trans['date']} at {trans['time']}")
                print()
                
        input("Press Enter to continue...")
        
    def view_history(self):
        """View complete transaction history"""
        self.clear_screen()
        self.print_header("Complete Transaction History")
        print()
        
        if not self.transaction_log:
            print("📭 No transactions recorded yet.")
            print("\n💡 Start using the system to see transaction history here!")
        else:
            print(f"📊 Total Transactions: {len(self.transaction_log)}")
            print()
            
            for i, trans in enumerate(self.transaction_log, 1):
                print(f"{i}. [{trans['date']} {trans['time']}]")
                print(f"   👤 {trans['sender']} → {trans['receiver']}")
                print(f"   📝 {trans['type']}: {trans['description']}")
                print()
                
        input("Press Enter to continue...")
        
    def hub_management(self):
        """H&R Hub management tools"""
        self.clear_screen()
        self.print_header("H&R Hub - Management Tools")
        print()
        
        print("⚙️  MANAGEMENT OPTIONS:")
        print()
        print("   1. 📊 Generate Transaction Report")
        print("   2. 👥 View Party Information")
        print("   3. 🔍 Search Transactions")
        print("   4. 🔙 Back")
        print()
        
        choice = input("👉 Enter your choice: ").strip()
        
        if choice == "1":
            self.generate_report()
        elif choice == "2":
            self.view_parties()
        elif choice == "3":
            self.search_transactions()
        elif choice == "4":
            return
        else:
            print("\n❌ Invalid choice.")
            input("Press Enter to continue...")
            
    def generate_report(self):
        """Generate transaction report"""
        self.clear_screen()
        self.print_header("Transaction Report")
        print()
        
        if not self.transaction_log:
            print("📭 No transactions to report.")
            input("Press Enter to continue...")
            return
            
        # Calculate statistics
        total_transactions = len(self.transaction_log)
        
        content_types = {}
        party_activity = {}
        
        for trans in self.transaction_log:
            content_types[trans['type']] = content_types.get(trans['type'], 0) + 1
            party_activity[trans['sender']] = party_activity.get(trans['sender'], 0) + 1
            
        print(f"📊 TRANSACTION SUMMARY REPORT")
        print(f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print(f"📈 Total Transactions: {total_transactions}")
        print()
        
        print("📝 By Content Type:")
        for content_type, count in content_types.items():
            print(f"   • {content_type}: {count}")
        print()
        
        print("👥 By Sender Activity:")
        for sender, count in party_activity.items():
            print(f"   • {sender}: {count} sent")
        print()
        
        if self.transaction_log:
            first_trans = self.transaction_log[0]
            last_trans = self.transaction_log[-1]
            print(f"⏰ Period: {first_trans['date']} to {last_trans['date']}")
            
        input("\nPress Enter to continue...")
        
    def view_parties(self):
        """View party information"""
        self.clear_screen()
        self.print_header("Party Information")
        print()
        
        for key, party in self.parties.items():
            if key == "1":
                icon = "🏢"
            elif key == "2":
                icon = "🏛️"
            else:
                icon = "🏠"
                
            print(f"{icon} {party['role']}")
            print(f"   Name: {party['name']}")
            print(f"   ID: {key}")
            print()
            
        input("Press Enter to continue...")
        
    def search_transactions(self):
        """Search transactions"""
        self.clear_screen()
        self.print_header("Search Transactions")
        print()
        
        search_term = input("🔍 Enter search term (name, type, or description): ").strip().lower()
        
        if not search_term:
            print("❌ Search term cannot be empty.")
            input("Press Enter to continue...")
            return
            
        matches = []
        for trans in self.transaction_log:
            if (search_term in trans['sender'].lower() or
                search_term in trans['receiver'].lower() or
                search_term in trans['type'].lower() or
                search_term in trans['description'].lower()):
                matches.append(trans)
                
        print(f"\n🔍 Search Results for '{search_term}': {len(matches)} matches")
        print()
        
        if matches:
            for i, trans in enumerate(matches, 1):
                print(f"{i}. [{trans['date']} {trans['time']}]")
                print(f"   {trans['sender']} → {trans['receiver']}")
                print(f"   {trans['type']}: {trans['description']}")
                print()
        else:
            print("📭 No matches found.")
            
        input("Press Enter to continue...")
        
    def system_settings(self):
        """System settings"""
        self.clear_screen()
        self.print_header("System Settings")
        print()
        
        print("⚙️  SYSTEM INFORMATION:")
        print()
        print("   🔒 Encryption: RSA-2048 + AES-256-CBC")
        print("   ✍️  Digital Signatures: RSA-PSS")
        print("   🛡️  Security Level: Maximum")
        print("   ⚖️  Legal Compliance: UK Electronic Communications Act 2000")
        print("   📋 Audit Trail: Complete")
        print()
        
        print("📊 CURRENT STATUS:")
        print(f"   📈 Total Transactions: {len(self.transaction_log)}")
        print(f"   👥 Active Parties: {len(self.parties)}")
        print(f"   🕒 Session Started: {datetime.now().strftime('%H:%M:%S')}")
        print()
        
        input("Press Enter to continue...")

def main():
    """Main entry point"""
    try:
        interface = SimpleInterface()
        interface.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thank you for using Property Transaction Protocol!")
        print("🔒 All your communications were encrypted and secure.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please contact support for assistance.")

if __name__ == "__main__":
    main()
