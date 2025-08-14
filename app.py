# app.py - Backend with Python Flask

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # For session management

# Translations
LANGS = {
    'en': {
        'app': 'Bachat Gat',
        'login': 'Login',
        'email': 'Email',
        'password': 'Password',
        'signIn': 'Sign in',
        'dashboard': 'Dashboard',
        'savingsLedger': 'Savings Ledger',
        'loans': 'Loan Management',
        'historyReports': 'History & Reports',
        'adminPanel': 'Admin Panel',
        'settings': 'Settings',
        'help': 'Help & Support',
        'role': 'Role',
        'member': 'Member',
        'admin': 'Admin',
        'superAdmin': 'Super Admin',
        'addSavings': 'Add Savings',
        'requestLoan': 'Request Loan',
        'totalSavings': 'Total Savings',
        'activeLoans': 'Active Loans',
        'repaymentRate': 'Repayment Rate',
        'export': 'Export',
        'emiSchedule': 'EMI Schedule',
        'payNow': 'Pay Now',
        'paid': 'Paid',
        'pending': 'Pending',
        'failed': 'Failed',
        'language': 'Language',
        'theme': 'Theme',
        'light': 'Light',
        'dark': 'Dark',
        'notifications': 'Notifications',
        'logout': 'Logout',
    },
    'hi': {
        'app': 'बचत गट',
        'login': 'लॉगिन',
        'email': 'ईमेल',
        'password': 'पासवर्ड',
        'signIn': 'साइन इन',
        'dashboard': 'डैशबोर्ड',
        'savingsLedger': 'सेविंग्स लेजर',
        'loans': 'ऋण प्रबंधन',
        'historyReports': 'इतिहास और रिपोर्ट्स',
        'adminPanel': 'एडमिन पैनल',
        'settings': 'सेटिंग्स',
        'help': 'मदद',
        'role': 'भूमिका',
        'member': 'मेंबर',
        'admin': 'एडमिन',
        'superAdmin': 'सुपर एडमिन',
        'addSavings': 'सेविंग्स जोड़ें',
        'requestLoan': 'लोन रिक्वेस्ट',
        'totalSavings': 'कुल बचत',
        'activeLoans': 'सक्रिय ऋण',
        'repaymentRate': 'भुगतान दर',
        'export': 'एक्सपोर्ट',
        'emiSchedule': 'ईएमआई शेड्यूल',
        'payNow': 'अभी भुगतान करें',
        'paid': 'भुगतान हुआ',
        'pending': 'लंबित',
        'failed': 'असफल',
        'language': 'भाषा',
        'theme': 'थीम',
        'light': 'लाइट',
        'dark': 'डार्क',
        'notifications': 'सूचनाएँ',
        'logout': 'लॉगआउट',
    },
    'mr': {
        'app': 'बचत गट',
        'login': 'लॉगिन',
        'email': 'ईमेल',
        'password': 'पासवर्ड',
        'signIn': 'साइन इन',
        'dashboard': 'डॅशबोर्ड',
        'savingsLedger': 'बचत लेजर',
        'loans': 'कर्ज व्यवस्थापन',
        'historyReports': 'इतिहास व अहवाल',
        'adminPanel': 'अॅडमिन पॅनेल',
        'settings': 'सेटिंग्स',
        'help': 'मदत',
        'role': 'भूमिका',
        'member': 'सदस्य',
        'admin': 'अॅडमिन',
        'superAdmin': 'सुपर अॅडमिन',
        'addSavings': 'बचत जोडा',
        'requestLoan': 'कर्ज विनंती',
        'totalSavings': 'एकूण बचत',
        'activeLoans': 'सक्रिय कर्ज',
        'repaymentRate': 'परतफेड दर',
        'export': 'एक्सपोर्ट',
        'emiSchedule': 'ईएमआय वेळापत्रक',
        'payNow': 'आता भरा',
        'paid': 'भरणा झाला',
        'pending': 'प्रलंबित',
        'failed': 'अयशस्वी',
        'language': 'भाषा',
        'theme': 'थीम',
        'light': 'लाइट',
        'dark': 'डार्क',
        'notifications': 'सूचना',
        'logout': 'लॉगआउट',
    },
}

# In-memory data (for demo)
members = [
    {'id': 1, 'name': 'Asha Patil', 'phone': '98xxxx1234'},
    {'id': 2, 'name': 'Neha Joshi', 'phone': '98xxxx5678'},
    {'id': 3, 'name': 'Kiran More', 'phone': '99xxxx1010'},
]

savings = [
    {'id': 1, 'memberId': 1, 'amount': 500, 'date': '2025-07-01'},
    {'id': 2, 'memberId': 2, 'amount': 500, 'date': '2025-07-01'},
    {'id': 3, 'memberId': 3, 'amount': 500, 'date': '2025-07-01'},
    {'id': 4, 'memberId': 1, 'amount': 500, 'date': '2025-08-01'},
]

loans = [
    {
        'id': 101,
        'memberId': 2,
        'amount': 5000,
        'status': 'approved',
        'interest': 12,
        'schedule': [
            {'due': '2025-08-10', 'amount': 1000, 'status': 'pending'},
            {'due': '2025-09-10', 'amount': 1000, 'status': 'pending'},
            {'due': '2025-10-10', 'amount': 1000, 'status': 'pending'},
            {'due': '2025-11-10', 'amount': 1000, 'status': 'pending'},
            {'due': '2025-12-10', 'amount': 1000, 'status': 'pending'},
        ],
    },
    {
        'id': 102,
        'memberId': 1,
        'amount': 3000,
        'status': 'pending',
        'interest': 10,
        'schedule': [],
    },
]

audit = [
    {'ts': '2025-08-01 10:20', 'action': 'Member added: Kiran More', 'by': 'Admin'},
    {'ts': '2025-08-02 14:05', 'action': 'Loan approved: #101 (Neha Joshi)', 'by': 'Admin'},
    {'ts': '2025-08-05 09:30', 'action': 'Savings recorded: Asha Patil ₹500', 'by': 'Treasurer'},
]

notifications = [
    {'id': 1, 'text': 'EMI due on 10 Aug for Loan #101', 'unread': True},
    {'id': 2, 'text': 'Monthly meeting on 15 Aug', 'unread': False},
]

def now_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M')

def role_label(r):
    if r == 'member': return 'Member'
    if r == 'admin': return 'Admin'
    return 'Super Admin'

@app.before_request
def load_session_defaults():
    if 'lang' not in session:
        session['lang'] = 'en'
    if 'theme_dark' not in session:
        session['theme_dark'] = True
    if 'role' not in session:
        session['role'] = 'member'
    if 'logged_in' not in session:
        session['logged_in'] = False

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Simple mock login
        session['logged_in'] = True
        session['role'] = 'member'
        return redirect(url_for('dashboard'))
    t = LANGS[session['lang']]
    return render_template('login.html', t=t, theme_dark=session['theme_dark'])

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

@app.route('/change_lang/<lang>')
def change_lang(lang):
    if lang in LANGS:
        session['lang'] = lang
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/toggle_theme')
def toggle_theme():
    session['theme_dark'] = not session['theme_dark']
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/change_role/<role>')
def change_role(role):
    if role in ['member', 'admin', 'super']:
        session['role'] = role
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/mark_read/<int:notif_id>')
def mark_read(notif_id):
    global notifications
    notifications = [n if n['id'] != notif_id else {**n, 'unread': False} for n in notifications]
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/')
@app.route('/dashboard')
def dashboard():
    if not session['logged_in']:
        return redirect(url_for('login'))
    t = LANGS[session['lang']]
    total_savings = sum(s['amount'] for s in savings)
    active_loans = len([l for l in loans if l['status'] != 'paid'])
    total_emis = sum(len(l['schedule']) for l in loans)
    paid_emis = sum(len([s for s in l['schedule'] if s['status'] == 'paid']) for l in loans)
    repayment_rate = round((paid_emis / total_emis * 100) if total_emis else 0)
    recent_savings = sorted(savings, key=lambda x: x['date'], reverse=True)[:5]
    return render_template('dashboard.html', t=t, theme_dark=session['theme_dark'], role=session['role'],
                           members=members, savings=savings, loans=loans, notifications=notifications,
                           total_savings=total_savings, active_loans=active_loans, repayment_rate=repayment_rate,
                           recent_savings=recent_savings)

@app.route('/savings', methods=['GET', 'POST'])
def savings_page():
    if not session['logged_in']:
        return redirect(url_for('login'))
    t = LANGS[session['lang']]
    if request.method == 'POST':
        member_id = int(request.form['member_id'])
        amount = int(request.form['amount'])
        new_id = max([s['id'] for s in savings] or [0]) + 1
        entry = {'id': new_id, 'memberId': member_id, 'amount': amount, 'date': datetime.now().strftime('%Y-%m-%d')}
        savings.append(entry)
        m_name = next((m['name'] for m in members if m['id'] == member_id), 'Member')
        audit.insert(0, {'ts': now_str(), 'action': f'Savings recorded: {m_name} ₹{amount}', 'by': role_label(session['role'])})
        return redirect(url_for('savings_page'))
    return render_template('savings.html', t=t, theme_dark=session['theme_dark'], role=session['role'],
                           members=members, savings=sorted(savings, key=lambda x: x['date'], reverse=True), notifications=notifications)

@app.route('/loans', methods=['GET', 'POST'])
def loans_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    t = LANGS.get(session.get('lang', 'en'))

    if request.method == 'POST':
        action = request.form.get('action')
        loan_id = int(request.form.get('loan_id', 0))
        idx = int(request.form.get('idx', -1))

        for l in loans:
            if l['id'] != loan_id:
                continue

            if action == 'approve':
                l['status'] = 'approved'
                if not l.get('schedule'):
                    l['schedule'] = [
                        {'due': '2025-08-10', 'amount': 1000, 'status': 'pending'},
                        {'due': '2025-09-10', 'amount': 1000, 'status': 'pending'},
                        {'due': '2025-10-10', 'amount': 1000, 'status': 'pending'},
                    ]
                audit.insert(0, {
                    'ts': now_str(),
                    'action': f'Loan approved: #{loan_id}',
                    'by': role_label(session.get('role', 'member'))
                })
                break

            elif action == 'pay' and l.get('schedule') and 0 <= idx < len(l['schedule']):
                l['schedule'][idx]['status'] = 'paid'
                if all(s['status'] == 'paid' for s in l['schedule']):
                    l['status'] = 'paid'
                audit.insert(0, {
                    'ts': now_str(),
                    'action': f'EMI paid via Stripe for Loan #{loan_id}',
                    'by': 'System'
                })
                break

        return redirect(url_for('loans_page'))

    return render_template(
        'loans.html',
        t=t,
        theme_dark=session.get('theme_dark', False),
        role=session.get('role', 'member'),
        members=members,
        loans=loans,
        notifications=notifications
    )


@app.route('/history')
def history():
    if not session['logged_in']:
        return redirect(url_for('login'))
    t = LANGS[session['lang']]
    return render_template('history.html', t=t, theme_dark=session['theme_dark'], role=session['role'],
                           members=members, savings=savings, loans=loans, audit=audit, notifications=notifications)

@app.route('/export/<kind>')
def export(kind):
    data = {'savings': savings, 'loans': loans, 'audit': audit}
    return jsonify(data)  # For demo, return JSON. In real, generate PDF/Excel

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session['logged_in'] or session['role'] == 'member':
        return redirect(url_for('dashboard'))
    t = LANGS[session['lang']]
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        new_id = max([m['id'] for m in members] or [0]) + 1
        members.append({'id': new_id, 'name': name, 'phone': phone})
        audit.insert(0, {'ts': now_str(), 'action': f'Member added: {name}', 'by': role_label(session['role'])})
        return redirect(url_for('admin'))
    active_loans = len([l for l in loans if l['status'] != 'paid'])
    return render_template('admin.html', t=t, theme_dark=session['theme_dark'], role=session['role'],
                           members=members, loans=loans, audit=audit, notifications=notifications,
                           num_groups=3, num_members=len(members), active_loans=active_loans)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if not session['logged_in']:
        return redirect(url_for('login'))
    t = LANGS[session['lang']]
    return render_template('settings.html', t=t, theme_dark=session['theme_dark'], role=session['role'],
                           lang=session['lang'], notifications=notifications)

@app.route('/help')
def help_page():
    if not session['logged_in']:
        return redirect(url_for('login'))
    t = LANGS[session['lang']]
    return render_template('help.html', t=t, theme_dark=session['theme_dark'], role=session['role'],
                           notifications=notifications)

if __name__ == '__main__':
    app.run(debug=True)