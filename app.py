from flask import Flask, render_template, redirect, url_for, request, session
import json
import os

app = Flask(__name__)
app.secret_key = 'b4c29b27d96895e78b15a4f7bbdb99d2'  # Replace with a secure key in production

# Load questions from JSON file
with open('data/questions.json', 'r') as file:
    questions_data = json.load(file)["questions"]

# Predefined users (for simplicity, using a dictionary)
users = {
    "sj": {"name": "Sudhir Jangala", "password": "sj"},
    "sk": {"name": "Saurabh Kumar", "password": "sk"},
    "ma": {"name": "Mushahid Ali", "password": "ma"},
    "spk": {"name": "Suresh Panda Harekrishna", "password": "spk"},
    "pb": {"name": "Pranav Belgaonkar", "password": "pb"},
    "ha": {"name": "Hasib Alam", "password": "ha"},
    "kpk": {"name": "Kuppala Pavan Kumar", "password": "kpk"},
    "ag": {"name": "Amal George", "password": "ag"},
    "aps": {"name": "Anand Prakash Singh", "password": "aps"},
    # Add more users up to user9...
}

# Store user results
user_results = {}


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        
        # Debugging: Print the received form data
        print(f"Received user_id: {user_id}, password: {password}")

        # Authenticate user
        if user_id in users and users[user_id]['password'] == password:
            session['user_id'] = user_id
            session['current_question'] = 0
            user_results[user_id] = {"name": users[user_id]['name'], "answers": [], "score": 0}
            return redirect(url_for('quiz'))
        else:
            # Debugging: Print failure reason
            print(f"Invalid login attempt for user_id: {user_id}")
            return render_template('login.html', error="Invalid user ID or password.")
    
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_user = request.form['admin_user']
        admin_password = request.form['admin_password']
        
        # Simple check for admin credentials
        if admin_user == 'admin' and admin_password == 'adminpassword':
            session['admin'] = True
            return redirect(url_for('view_results'))
        else:
            return render_template('admin_login.html', error="Invalid admin credentials.")
    
    return render_template('admin_login.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    current_question_index = session.get('current_question', 0)

    # Ensure the `questions_data` is a list and access by index
    if current_question_index >= len(questions_data):
        return redirect(url_for('result'))
    
    # Correctly access the current question using the index
    question = questions_data[current_question_index]
    
    # Handle the answer submission
    if request.method == 'POST':
        selected_option = request.form.get('option')
        correct_answer = question['correct_answer']
        user_results[user_id]['answers'].append(selected_option)

        # Check if the answer is correct and update score
        if selected_option == correct_answer:
            user_results[user_id]['score'] += 1
        
        # Move to the next question
        session['current_question'] = current_question_index + 1
        return redirect(url_for('quiz'))
    
    # Render the current question
    return render_template('quiz.html', question=question, index=current_question_index + 1)


@app.route('/view-results')
def view_results():
    if 'admin' not in session:  # Simple check to make sure only an admin can view results
        return redirect(url_for('login'))
    
    return render_template('view_results.html', results=user_results)

@app.route('/result')
def result():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user_info = user_results[user_id]
    return render_template('result.html', user=user_info)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('current_question', None)
    session.pop('admin', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
