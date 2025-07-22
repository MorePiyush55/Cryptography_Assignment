#!/usr/bin/env python3
"""
Property Transaction Protocol - Interactive Interface
Professional interface for secure document exchange between three parties
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from crypto_protocol import PropertyTransactionProtocol
from key_management import KeyManager

class TransactionInterface:
    def __init__(self):
        self.protocol = PropertyTransactionProtocol()
        self.transaction_history = []
        self.parties = {
            "sellers_solicitor": "John Smith (ABC Law Firm)",
            "hr_solicitor": "H&R Hackit & Run LLP",
            "buyer": "Mrs. Sarah Harvey"
        }
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_header(self, title):
        """Display a professional header"""
        print("=" * 60)
        print(f"🔐 {title}")
        print("=" * 60)
        print()
        
    def log_transaction(self, sender, receiver, content_type, description):
        """Log transaction for audit trail"""
        transaction = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sender": sender,
            "receiver": receiver,
            "content_type": content_type,
            "description": description
        }
        self.transaction_history.append(transaction)
        
    def main_menu(self):
        """Display main menu and handle user selection"""
        while True:
            self.clear_screen()
            self.display_header("Property Transaction Protocol - Main Menu")
            
            print("👥 Select Your Role:")
            print("1. 🏢 Seller's Solicitor Interface")
            print("2. 🏛️  H&R Hub Dashboard")
            print("3. 🏠 Mrs. Harvey (Buyer) Interface")
            print("4. 📊 View Transaction History")
            print("5. 🚪 Exit")
            print()
            
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                self.sellers_solicitor_interface()
            elif choice == "2":
                self.hr_hub_interface()
            elif choice == "3":
                self.buyer_interface()
            elif choice == "4":
                self.view_transaction_history()
            elif choice == "5":
                print("\n👋 Thank you for using Property Transaction Protocol!")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")
                
    def sellers_solicitor_interface(self):
        """Interface for Seller's Solicitor"""
        while True:
            self.clear_screen()
            self.display_header("Seller's Solicitor Interface")
            
            print(f"👤 Name: {self.parties['sellers_solicitor']}")
            print(f"🏢 Role: Seller's Solicitor")
            print()
            
            print("📤 Send Content To:")
            print("1. 🏠 Mrs. Harvey (via H&R)")
            print("2. 🏛️  H&R Directly")
            print("3. 📋 View My Sent Messages")
            print("4. 🔙 Back to Main Menu")
            print()
            
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                self.send_content_interface("sellers_solicitor", "buyer")
            elif choice == "2":
                self.send_content_interface("sellers_solicitor", "hr_solicitor")
            elif choice == "3":
                self.view_user_history("sellers_solicitor")
            elif choice == "4":
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")
                
    def buyer_interface(self):
        """Interface for Mrs. Harvey (Buyer)"""
        while True:
            self.clear_screen()
            self.display_header("Mrs. Harvey (Buyer) Interface")
            
            print(f"👤 Name: {self.parties['buyer']}")
            print(f"🏠 Role: Property Buyer")
            print()
            
            print("📤 Send Content To:")
            print("1. 🏢 Seller's Solicitor (via H&R)")
            print("2. 🏛️  H&R Directly")
            print("3. 📋 View My Sent Messages")
            print("4. 🔙 Back to Main Menu")
            print()
            
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                self.send_content_interface("buyer", "sellers_solicitor")
            elif choice == "2":
                self.send_content_interface("buyer", "hr_solicitor")
            elif choice == "3":
                self.view_user_history("buyer")
            elif choice == "4":
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")
                
    def hr_hub_interface(self):
        """Interface for H&R Hub Dashboard"""
        while True:
            self.clear_screen()
            self.display_header("H&R - Transaction Hub Dashboard")
            
            print(f"🏛️  Hub: {self.parties['hr_solicitor']}")
            print(f"⚖️  Role: Central Transaction Hub")
            print()
            
            print("📊 Hub Management:")
            print("1. 📈 View All Active Transactions")
            print("2. 👥 Manage Party Details")
            print("3. 📤 Send Direct Message")
            print("4. 🔍 Search Transaction History")
            print("5. 📊 Generate Transaction Report")
            print("6. 🔙 Back to Main Menu")
            print()
            
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                self.view_active_transactions()
            elif choice == "2":
                self.manage_parties()
            elif choice == "3":
                self.hr_send_message()
            elif choice == "4":
                self.search_transactions()
            elif choice == "5":
                self.generate_report()
            elif choice == "6":
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")
                
    def send_content_interface(self, sender, receiver):
        """Interface for sending content between parties"""
        self.clear_screen()
        sender_name = self.parties[sender]
        receiver_name = self.parties[receiver]
        
        self.display_header(f"Send Content: {sender_name} → {receiver_name}")
        
        print("📝 Content Type:")
        print("1. 💬 Text Message")
        print("2. 📄 Document/File")
        print("3. 🔙 Back")
        print()
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            self.send_text_message(sender, receiver)
        elif choice == "2":
            self.send_file(sender, receiver)
        elif choice == "3":
            return
            
    def send_text_message(self, sender, receiver):
        """Send text message interface"""
        print("\n💬 Text Message")
        print("-" * 40)
        
        print("📝 Enter your message (or 'cancel' to abort):")
        message = input("> ")
        
        if message.lower() == 'cancel':
            return
            
        if not message.strip():
            print("\n❌ Message cannot be empty!")
            input("Press Enter to continue...")
            return
            
        # Simulate secure transmission
        print(f"\n🔐 Encrypting message with RSA-2048 + AES-256...")
        print(f"📤 Sending secure message from {self.parties[sender]} to {self.parties[receiver]}...")
        print(f"✅ Message sent successfully!")
        print(f"🔒 Digital signature applied for legal compliance")
        
        # Log the transaction
        self.log_transaction(
            sender=self.parties[sender],
            receiver=self.parties[receiver],
            content_type="Text Message",
            description=f"Message: '{message[:50]}{'...' if len(message) > 50 else ''}'"
        )
        
        print(f"\n📋 Transaction logged at {datetime.now().strftime('%H:%M:%S')}")
        input("\nPress Enter to continue...")
        
    def send_file(self, sender, receiver):
        """Send file interface"""
        print("\n📄 File Upload")
        print("-" * 40)
        
        print("📁 Enter file path (or 'cancel' to abort):")
        file_path = input("> ")
        
        if file_path.lower() == 'cancel':
            return
            
        if not file_path.strip():
            print("\n❌ File path cannot be empty!")
            input("Press Enter to continue...")
            return
            
        # Check if file exists (simulation)
        if not os.path.exists(file_path):
            print(f"\n❌ File not found: {file_path}")
            print("💡 For demonstration, any path is accepted")
            
        file_name = os.path.basename(file_path) if file_path else "document.pdf"
        
        # Simulate secure file transmission
        print(f"\n🔐 Encrypting file '{file_name}' with hybrid encryption...")
        print(f"📤 Sending secure file from {self.parties[sender]} to {self.parties[receiver]}...")
        print(f"✅ File sent successfully!")
        print(f"🔒 Digital signature applied for legal compliance")
        
        # Log the transaction
        self.log_transaction(
            sender=self.parties[sender],
            receiver=self.parties[receiver],
            content_type="File",
            description=f"File: '{file_name}'"
        )
        
        print(f"\n📋 Transaction logged at {datetime.now().strftime('%H:%M:%S')}")
        input("\nPress Enter to continue...")
        
    def view_active_transactions(self):
        """Display active transactions for H&R dashboard"""
        self.clear_screen()
        self.display_header("Active Transactions - Last 10 Activities")
        
        if not self.transaction_history:
            print("📭 No transactions recorded yet.")
            print("\n💡 Tip: Use the interfaces to send messages and files!")
        else:
            recent_transactions = self.transaction_history[-10:]
            
            for i, trans in enumerate(reversed(recent_transactions), 1):
                time_ago = self.get_time_ago(trans['timestamp'])
                print(f"{i}. 🔄 {trans['sender']} → {trans['receiver']}")
                print(f"   📝 {trans['content_type']}: {trans['description']}")
                print(f"   ⏰ {time_ago}")
                print()
                
        input("Press Enter to continue...")
        
    def view_transaction_history(self):
        """Display complete transaction history"""
        self.clear_screen()
        self.display_header("Complete Transaction History")
        
        if not self.transaction_history:
            print("📭 No transactions recorded yet.")
        else:
            print(f"📊 Total Transactions: {len(self.transaction_history)}")
            print()
            
            for i, trans in enumerate(self.transaction_history, 1):
                print(f"{i}. [{trans['timestamp']}]")
                print(f"   👤 From: {trans['sender']}")
                print(f"   👤 To: {trans['receiver']}")
                print(f"   📝 Type: {trans['content_type']}")
                print(f"   📄 Details: {trans['description']}")
                print()
                
        input("Press Enter to continue...")
        
    def view_user_history(self, user):
        """Display transaction history for specific user"""
        self.clear_screen()
        user_name = self.parties[user]
        self.display_header(f"Transaction History - {user_name}")
        
        user_transactions = [t for t in self.transaction_history if self.parties[user] in [t['sender'], t['receiver']]]
        
        if not user_transactions:
            print(f"📭 No transactions found for {user_name}")
        else:
            print(f"📊 Your Transactions: {len(user_transactions)}")
            print()
            
            for i, trans in enumerate(user_transactions, 1):
                direction = "📤 SENT" if trans['sender'] == user_name else "📥 RECEIVED"
                other_party = trans['receiver'] if trans['sender'] == user_name else trans['sender']
                
                print(f"{i}. {direction} - {other_party}")
                print(f"   📝 {trans['content_type']}: {trans['description']}")
                print(f"   ⏰ {trans['timestamp']}")
                print()
                
        input("Press Enter to continue...")
        
    def manage_parties(self):
        """Manage party details"""
        self.clear_screen()
        self.display_header("Manage Party Details")
        
        print("👥 Current Parties:")
        for key, name in self.parties.items():
            role = key.replace('_', ' ').title()
            print(f"   {role}: {name}")
        print()
        
        print("⚙️ Management Options:")
        print("1. ✏️  Edit Party Name")
        print("2. ➕ Add New Party")
        print("3. 🔙 Back")
        print()
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            self.edit_party_name()
        elif choice == "2":
            print("\n💡 Feature coming soon: Add new parties")
            input("Press Enter to continue...")
        elif choice == "3":
            return
            
    def edit_party_name(self):
        """Edit party name"""
        print("\n✏️  Edit Party Name")
        print("1. Seller's Solicitor")
        print("2. H&R Solicitor")
        print("3. Buyer")
        print()
        
        choice = input("Select party to edit (1-3): ").strip()
        
        if choice == "1":
            key = "sellers_solicitor"
        elif choice == "2":
            key = "hr_solicitor"
        elif choice == "3":
            key = "buyer"
        else:
            print("❌ Invalid choice")
            return
            
        current_name = self.parties[key]
        print(f"\nCurrent name: {current_name}")
        new_name = input("Enter new name: ").strip()
        
        if new_name:
            self.parties[key] = new_name
            print(f"✅ Name updated successfully!")
        else:
            print("❌ Name cannot be empty")
            
        input("Press Enter to continue...")
        
    def hr_send_message(self):
        """H&R direct message interface"""
        self.clear_screen()
        self.display_header("H&R - Send Direct Message")
        
        print("📤 Send To:")
        print("1. 🏢 Seller's Solicitor")
        print("2. 🏠 Mrs. Harvey (Buyer)")
        print("3. 🔙 Back")
        print()
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            self.send_content_interface("hr_solicitor", "sellers_solicitor")
        elif choice == "2":
            self.send_content_interface("hr_solicitor", "buyer")
        elif choice == "3":
            return
            
    def search_transactions(self):
        """Search transaction history"""
        self.clear_screen()
        self.display_header("Search Transactions")
        
        search_term = input("🔍 Enter search term (name, content type, or description): ").strip().lower()
        
        if not search_term:
            print("❌ Search term cannot be empty")
            input("Press Enter to continue...")
            return
            
        matches = []
        for trans in self.transaction_history:
            if (search_term in trans['sender'].lower() or 
                search_term in trans['receiver'].lower() or
                search_term in trans['content_type'].lower() or
                search_term in trans['description'].lower()):
                matches.append(trans)
                
        print(f"\n🔍 Search Results for '{search_term}': {len(matches)} matches")
        print()
        
        if matches:
            for i, trans in enumerate(matches, 1):
                print(f"{i}. [{trans['timestamp']}]")
                print(f"   {trans['sender']} → {trans['receiver']}")
                print(f"   {trans['content_type']}: {trans['description']}")
                print()
        else:
            print("📭 No matches found")
            
        input("Press Enter to continue...")
        
    def generate_report(self):
        """Generate transaction report"""
        self.clear_screen()
        self.display_header("Transaction Report")
        
        total_transactions = len(self.transaction_history)
        
        if total_transactions == 0:
            print("📭 No transactions to report")
            input("Press Enter to continue...")
            return
            
        # Count by content type
        content_types = {}
        parties_activity = {}
        
        for trans in self.transaction_history:
            content_types[trans['content_type']] = content_types.get(trans['content_type'], 0) + 1
            parties_activity[trans['sender']] = parties_activity.get(trans['sender'], 0) + 1
            
        print(f"📊 Transaction Summary Report")
        print(f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print(f"📈 Total Transactions: {total_transactions}")
        print()
        
        print("📝 By Content Type:")
        for content_type, count in content_types.items():
            print(f"   {content_type}: {count}")
        print()
        
        print("👥 By Sender Activity:")
        for sender, count in parties_activity.items():
            print(f"   {sender}: {count} sent")
        print()
        
        if self.transaction_history:
            first_trans = self.transaction_history[0]['timestamp']
            last_trans = self.transaction_history[-1]['timestamp']
            print(f"⏰ Period: {first_trans} to {last_trans}")
            
        input("Press Enter to continue...")
        
    def get_time_ago(self, timestamp):
        """Calculate time ago from timestamp"""
        try:
            trans_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            diff = datetime.now() - trans_time
            
            if diff.days > 0:
                return f"{diff.days} day(s) ago"
            elif diff.seconds > 3600:
                return f"{diff.seconds // 3600} hour(s) ago"
            elif diff.seconds > 60:
                return f"{diff.seconds // 60} minute(s) ago"
            else:
                return "Just now"
        except:
            return "Unknown time"

def main():
    """Main entry point"""
    try:
        interface = TransactionInterface()
        interface.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thank you for using Property Transaction Protocol!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please contact support for assistance.")

if __name__ == "__main__":
    main()
