import uuid
from datetime import datetime, timedelta

# In-memory storage for active sessions (for illustration purposes)
active_sessions = {}


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def authenticate(username, password):
    # Simulate user authentication (replace with actual authentication logic)
    user = User(username, password)
    return user


def create_session(user):
    # Generate a unique session ID (UUID for simplicity)
    session_id = str(uuid.uuid4())

    # Store the session ID and user credentials in active sessions
    active_sessions[user.username] = {
        'session_id': session_id,
        'expiry_time': datetime.now() + timedelta(hours=1)  # Example: session expires in 1 hour
    }

    return session_id


def check_existing_sessions(username):
    # Check if there is an active session for the given username
    if username in active_sessions:
        session_data = active_sessions[username]
        # Check if the session is still valid (not expired)
        if session_data['expiry_time'] > datetime.now():
            return session_data['session_id']

    return None


def authenticate_user(username, password):
    # Check if there is already an active session for the given credentials
    existing_session_id = check_existing_sessions(username)
    if existing_session_id:
        return f"Authentication failed: User already authenticated with session ID {existing_session_id}."

    # Authenticate the user (replace with actual authentication logic)
    user = authenticate(username, password)
    if user:
        # Create a new session for the authenticated user
        session_id = create_session(user)
        return f"Authentication successful. Session ID: {session_id}"
    else:
        return "Authentication failed: Invalid credentials."


# Example usage
if __name__ == "__main__":
    # Simulate authentication attempts
    print(authenticate_user("user1", "password123"))  # Should authenticate successfully
    print(authenticate_user("user1", "password123"))  # Should fail as user is already authenticated
    print(authenticate_user("user2", "password456"))  # Should authenticate successfully
