"""
Session Expiration Handling Component for Agentic Travel Planner
Implements session expiration with redirect to login and resume option
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import time


class SessionHandler:
    """Manages session expiration and resume functionality"""
    
    def __init__(self):
        self.session_timeout = 3600  # 1 hour in seconds
        self.session_key = "travel_planner_session"
        self.resume_key = "travel_planner_resume_data"
    
    def create_session(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new session with user data.
        
        Args:
            user_data: User session data
        
        Returns:
            Session information dictionary
        """
        now = datetime.now()
        expires_at = now + timedelta(seconds=self.session_timeout)
        
        session = {
            "session_id": self._generate_session_id(),
            "created_at": now.isoformat(),
            "expires_at": expires_at.isoformat(),
            "last_activity": now.isoformat(),
            "user_data": user_data,
            "is_active": True
        }
        
        return session
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def check_session_expired(self, session: Dict[str, Any]) -> bool:
        """
        Check if session has expired.
        
        Args:
            session: Session dictionary
        
        Returns:
            True if session is expired
        """
        if not session:
            return True
        
        expires_at = session.get("expires_at")
        if not expires_at:
            return True
        
        try:
            expires_datetime = datetime.fromisoformat(expires_at)
            return datetime.now() > expires_datetime
        except (ValueError, TypeError):
            return True
    
    def get_session_status(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get detailed session status.
        
        Args:
            session: Session dictionary
        
        Returns:
            Session status dictionary
        """
        is_expired = self.check_session_expired(session)
        
        if is_expired:
            return {
                "is_expired": True,
                "status": "expired",
                "message": "Your session has expired. Please log in again.",
                "can_resume": False,
                "redirect_to": "login"
            }
        
        expires_at = session.get("expires_at")
        expires_datetime = datetime.fromisoformat(expires_at)
        remaining = (expires_datetime - datetime.now()).total_seconds()
        
        return {
            "is_expired": False,
            "status": "active",
            "message": "Session is active",
            "remaining_seconds": int(remaining),
            "can_resume": True,
            "redirect_to": None
        }
    
    def create_resume_data(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create resume data from session.
        
        Args:
            session: Session dictionary
        
        Returns:
            Resume data dictionary
        """
        if not session:
            return {}
        
        return {
            "session_id": session.get("session_id"),
            "user_data": session.get("user_data", {}),
            "created_at": session.get("created_at"),
            "resume_timestamp": datetime.now().isoformat()
        }
    
    def get_resume_html(self, resume_data: Dict[str, Any]) -> str:
        """
        Generate HTML for session expiration with resume option.
        
        Args:
            resume_data: Resume data dictionary
        
        Returns:
            HTML string for session expiration message
        """
        return f"""
        <div class="session-expired" style="
            background-color: #FEF3C7;
            border-left: 4px solid #F59E0B;
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 1rem;">⏰</div>
            <h3 style="color: #1E3A5F; margin: 0 0 0.5rem 0;">Session Expired</h3>
            <p style="color: #1F2937; margin: 0.5rem 0 1rem 0;">
                Your session has expired. Please log in again to continue.
            </p>
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                <a href="/login" style="
                    background: linear-gradient(135deg, #1E3A5F 0%, #008080 100%);
                    color: white;
                    text-decoration: none;
                    padding: 0.75rem 1.5rem;
                    border-radius: 8px;
                    font-weight: 500;
                    transition: all 0.2s ease;
                ">Log In</a>
                <button class="resume-btn" style="
                    background: transparent;
                    border: 2px solid #1E3A5F;
                    color: #1E3A5F;
                    padding: 0.75rem 1.5rem;
                    border-radius: 8px;
                    font-weight: 500;
                    cursor: pointer;
                    transition: all 0.2s ease;
                ">Resume Session</button>
            </div>
            <p style="color: #6B7280; margin-top: 1rem; font-size: 0.85rem;">
                Your previous trip details will be available after logging in.
            </p>
        </div>
        """
    
    def get_css(self) -> str:
        """
        Get CSS for session expiration message.
        
        Returns:
            CSS string for styling
        """
        return """
        .session-expired {
            animation: fadeIn 0.3s ease;
        }
        
        .session-expired button:hover,
        .session-expired a:hover {
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        """
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "session_timeout": self.session_timeout,
            "session_key": self.session_key,
            "resume_key": self.resume_key
        }
