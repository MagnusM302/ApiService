from datetime import datetime, timedelta
import secrets

class UserSessionManagement:
    def __init__(self, db):
        self.sessions = db.get_collection('user_sessions')

    def create_session(self, user_id):
        session_token = self.generate_session_token()
        session = {"user_id": user_id, "session_token": session_token, "created_at": datetime.utcnow()}
        self.sessions.insert_one(session)
        return session_token

    def generate_session_token(self):
        # Generer en unik session token
        return secrets.token_urlsafe()

    def verify_session(self, session_token):
        # Verificér om sessionen er gyldig
        session = self.sessions.find_one({"session_token": session_token})
        return session is not None

    def end_session(self, session_token):
        # Afslut en given session
        result = self.sessions.delete_one({"session_token": session_token})
        return result.deleted_count > 0
