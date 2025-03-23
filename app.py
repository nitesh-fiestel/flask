from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from service.auth_service import AuthService
from service.request import Request
from service.user_service import UserService

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for session management

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page if unauthorized access

# Mock database of users
users = Request.getAllUsers("http://localhost:8080/api/users/all")

# User class
class User(UserMixin):
    def __init__(self, id, username, name):
        self.id = username
        self.userId = id
        self.name = name

# User loader function
@login_manager.user_loader
def load_user(username):
    if username in users:
        id = users[username]["id"]
        return User(str(id), username, users[username]["name"])
    return None

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        auth = AuthService.authenticate(username, password)
        if(auth["authenticated"]):
            user = User(auth["id"], username, auth["name"])
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            return render_template('login.html')
    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    print(UserService.getFollowing(current_user.userId), "qqqqqqqqqqq")
    followingIds = [obj["followingId"]for obj in UserService.getFollowing(current_user.userId)["followers"]]
    emails = []
    for user in users:
        if users[user]["id"] in followingIds:
            emails.append(users[user]["email"])

    feed = UserService.getFeed(current_user.userId, users)
    return render_template('dashboard.html', name=current_user.name, items = feed, sidebar_items = emails, users = users)

# Logout route
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Home route
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/follow', methods=['POST'])
@login_required
def follow():
    username_to_follow = request.form.get('username_to_follow')
    if username_to_follow:
        # Implement the logic to follow the user here
        # For example, call a service function to handle the follow action
        success = UserService.follow(current_user.userId, users[username_to_follow]["id"])
        if success:
            flash(f'Successfully followed {username_to_follow}!', 'success')
        else:
            flash(f'Failed to follow {username_to_follow}.', 'danger')
    else:
        flash('No username provided.', 'warning')
    return redirect(url_for('dashboard'))

@app.route('/unfollow', methods=['POST'])
@login_required
def unfollow():
    email_to_unfollow = request.form.get('unfollow_id')
    print(email_to_unfollow, "unfollow")
    if email_to_unfollow:
        # Implement the logic to follow the user here
        # For example, call a service function to handle the follow action
        success = UserService.unfollow(current_user.userId, users[email_to_unfollow]["id"])
        if success:
            flash(f'Successfully followed {email_to_unfollow}!', 'success')
        else:
            flash(f'Failed to follow {email_to_unfollow}.', 'danger')
    else:
        flash('No username provided.', 'warning')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
