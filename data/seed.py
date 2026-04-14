import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.freelance_tax_mcp.memory.db import get_connection


def seed_data(db_path: Path):
    conn = get_connection(db_path)
    user_id = "user_001"
    
    with conn:
        conn.execute(
            "INSERT OR IGNORE INTO user_profiles (user_id, full_name, gst_number, tax_regime, tax_year) VALUES (?, ?, ?, ?, ?)",
            (user_id, "Jane Doe (Freelancer)", "22AAAAA0000A1Z5", "new", "2025-2026")
        )
        
        conn.execute(
            "INSERT OR IGNORE INTO clients (user_id, client_name, client_email) VALUES (?, ?, ?)",
            (user_id, "Acme Corp", "accounts@acme.com")
        )
        conn.execute(
            "INSERT OR IGNORE INTO clients (user_id, client_name, client_email) VALUES (?, ?, ?)",
            (user_id, "Globex Inc", "finance@globex.com")
        )
        
        conn.execute(
            "INSERT OR IGNORE INTO invoices (user_id, invoice_number, client_name, amount, issue_date, due_date, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, "INV-2026-001", "Acme Corp", 50000.0, "2026-04-01", "2026-04-15", "issued")
        )
        conn.execute(
            "INSERT OR IGNORE INTO invoices (user_id, invoice_number, client_name, amount, issue_date, due_date, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, "INV-2026-002", "Globex Inc", 75000.0, "2026-04-10", "2026-04-25", "paid")
        )
        
        conn.execute(
            "INSERT OR IGNORE INTO transactions (user_id, txn_type, amount, txn_date, notes) VALUES (?, ?, ?, ?, ?)",
            (user_id, "expense", 2500.0, "2026-04-05", "Software subscriptions")
        )
        conn.execute(
            "INSERT OR IGNORE INTO transactions (user_id, txn_type, amount, txn_date, notes) VALUES (?, ?, ?, ?, ?)",
            (user_id, "expense", 12000.0, "2026-04-12", "New Monitor and accessories")
        )
        
        conn.execute(
            "INSERT OR IGNORE INTO reminders (user_id, title, due_date) VALUES (?, ?, ?)",
            (user_id, "File Advance Tax for Q1", "2026-06-15")
        )
        conn.execute(
            "INSERT OR IGNORE INTO reminders (user_id, title, due_date) VALUES (?, ?, ?)",
            (user_id, "Review Q1 Expenses", "2026-06-30")
        )
        
    conn.close()

if __name__ == "__main__":
    db_path = Path("data/tax.db")
    seed_data(db_path)
    print("Database seeded with sample data successfully!")
