from flask import Flask, jsonify, request, redirect, url_for, render_template, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import docker
import time

app = Flask(__name__)
app.secret_key = 'your-supersecretkey'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

client = docker.from_env()

class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {'your-username': {'password': 'your-password'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def is_blocked():
    block_until = session.get('block_until', 0)
    if time.time() < block_until:
        return True
    return False

def record_failed_attempt():
    session['failed_attempts'] = session.get('failed_attempts', 0) + 1
    if session['failed_attempts'] >= 3:
        session['block_until'] = time.time() + 60  # Block for 1 minute
        session['failed_attempts'] = 0

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated : 
        return redirect(url_for('index'))
    if is_blocked():
        return 'Too many failed attempts. Please try again later.', 403

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            session['failed_attempts'] = 0  # Reset the counter on successful login
            return redirect(url_for('index'))
        else:
            record_failed_attempt()
            return redirect(url_for('index'))

    return '''
       <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6 col-lg-4 mt-5"> <!-- Adjust column sizes as needed -->
                <form action="/login" method="post" class="card p-4 shadow">
                    <div class="mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input type="text" class="form-control" id="username" name="username" placeholder="Enter your username" required>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" name="password" placeholder="Enter your password" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Log In</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>

'''

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return redirect(url_for('list_containers'))

@app.route('/containers', methods=['GET'])
@login_required
def list_containers():
    containers = client.containers.list(all=True)
    container_list = [{'id': c.id, 'name': c.name, 'status': c.status} for c in containers]
    return jsonify(container_list)

@app.route('/containers/<string:name>/start', methods=['GET'])
@login_required
def start_container(name):
    try:
        container = client.containers.get(name)
        container.start()
        return jsonify({'message': f'Container {name} started successfully'}), 200
    except docker.errors.NotFound:
        return jsonify({'error': 'Container not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/containers/<string:name>/stop', methods=['GET'])
@login_required
def stop_container(name):
    try:
        container = client.containers.get(name)
        container.stop()
        return jsonify({'message': f'Container {name} stopped successfully'}), 200
    except docker.errors.NotFound:
        return jsonify({'error': 'Container not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/containers/<string:name>/restart', methods=['GET'])
@login_required
def restart_container(name):
    try:
        container = client.containers.get(name)
        container.restart()
        return jsonify({'message': f'Container {name} restarted successfully'}), 200
    except docker.errors.NotFound:
        return jsonify({'error': 'Container not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/docs', methods=['GET'])
def docs():
    return '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Documentation</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container">
    <h1 class="mt-5">API Documentation</h1>
    <p class="lead">This page provides documentation for the available API endpoints.</p>

    <h2>Endpoints</h2>

    <div class="card mt-3">
        <div class="card-header">
            Login Rules
        </div>
        <div class="card-body">
            <p>After 3 failed login attempts, the user will be blocked for 1 minute.</p>
        </div>
    </div>

    <div class="card mt-3">
        <div class="card-header">
            GET /containers
        </div>
        <div class="card-body">
            <p>List all Docker containers.</p>
            <pre><code>curl https://kelor.id:5050/containers</code></pre>
        </div>
    </div>

    <div class="card mt-3">
        <div class="card-header">
            GET /containers/&lt;name&gt;/restart
        </div>
        <div class="card-body">
            <p>Restart a Docker container by name.</p>
            <pre><code>curl https://kelor.id:5050/containers/&lt;name&gt;/restart</code></pre>
        </div>
    </div>

    <div class="card mt-3">
        <div class="card-header">
            GET /containers/&lt;name&gt;/start
        </div>
        <div class="card-body">
            <p>Start a Docker container by name.</p>
            <pre><code>curl https://kelor.id:5050/containers/&lt;name&gt;/start</code></pre>
        </div>
    </div>

    <div class="card my-3">
        <div class="card-header">
            GET /containers/&lt;name&gt;/stop
        </div>
        <div class="card-body">
            <p>Stop a Docker container by name.</p>
            <pre><code>curl https://kelor.id:5050/containers/&lt;name&gt;/stop</code></pre>
        </div>
    </div>

</div>
</body>
</html>

'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
