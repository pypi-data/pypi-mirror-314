import africastalking
import ssl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import time
from datetime import datetime, timedelta
from typing import List, Dict, Union, Optional
import logging

class SSLAdapter(HTTPAdapter):
    """Custom SSL Adapter for handling SSL connections."""
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = context
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

class EventNotifier:
    """
    A class to handle event notifications with SMS capabilities using Africa's Talking.
    
    Args:
        username (str): Africa's Talking username
        api_key (str): Africa's Talking API key
        sender_id (str): SMS sender ID
        events (List[Dict], optional): Initial list of events
    """
    
    def __init__(
        self,
        username: str,
        api_key: str,
        sender_id: str,
        events: Optional[List[Dict]] = None
    ):
        self.username = username
        self.api_key = api_key
        self.sender_id = sender_id
        self.events = events or []
        
        # Initialize Africa's Talking
        africastalking.initialize(username, api_key)
        self.sms = africastalking.SMS
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Setup SSL
        self._setup_ssl()
    
    def _setup_ssl(self):
        """Configure SSL settings for requests."""
        import requests
        self.session = requests.Session()
        adapter = SSLAdapter()
        self.session.mount('https://', adapter)
    
    def add_event(self, event: Dict):
        """
        Add a new event to the monitoring list.
        
        Args:
            event (Dict): Event dictionary containing 'name' and 'datetime'
        """
        if not isinstance(event.get('datetime'), datetime):
            try:
                event['datetime'] = datetime.fromisoformat(str(event['datetime']))
            except ValueError as e:
                self.logger.error(f"Invalid datetime format: {e}")
                raise
        
        self.events.append(event)
        self.logger.info(f"Added new event: {event['name']}")
    
    def send_sms(self, recipients: Union[str, List[str]], message: str) -> Dict:
        """
        Send SMS using Africa's Talking.
        
        Args:
            recipients: Phone number(s) to send SMS to (format: "+256XXXXXXXXX" or "256XXXXXXXXX")
            message: SMS content
            
        Returns:
            dict: Response from Africa's Talking API
        """
        print("Debug - Initial recipients:", recipients)
        
        if isinstance(recipients, str):
            recipients = [recipients]
        
        print("Debug - Recipients after list conversion:", recipients)
            
        try:
            # Format phone numbers correctly for Africa's Talking
            formatted_recipients = []
            for r in recipients:
                print("Debug - Processing recipient:", r)
                # Clean the phone number
                r = r.replace(" ", "")  # Remove spaces
                if not r.startswith('+'):
                    r = '+' + r  # Ensure it starts with '+'
                print("Debug - After formatting:", r)
                formatted_recipients.append(r)
            
            print("Debug - Final formatted recipients:", formatted_recipients)
            print("Debug - Message:", message)
            print("Debug - Sender ID:", self.sender_id)
                
            # Try to send SMS
            try:
                response = self.sms.send(message, formatted_recipients, sender_id=self.sender_id)
                print("Debug - API Response:", response)
                self.logger.info(f"SMS sent successfully to {formatted_recipients}")
                return response
            except Exception as api_error:
                print("Debug - API Error details:", str(api_error))
                raise
        except Exception as e:
            self.logger.error(f"Failed to send SMS: {e}")
            print("Debug - Exception details:", str(e))
            raise
    
    def check_events(self) -> Optional[Dict]:
        """
        Check for upcoming events and return the next event if found.
        
        Returns:
            Optional[Dict]: Next upcoming event if found, None otherwise
        """
        current_time = datetime.now()
        upcoming_events = [
            event for event in self.events 
            if event['datetime'] > current_time
        ]
        
        if upcoming_events:
            return min(upcoming_events, key=lambda x: x['datetime'])
        return None
    
    def start_monitoring(
        self,
        recipients: Union[str, List[str]],
        interval_seconds: int = 60,
        message_template: str = "Event {name} at {time}"
    ):
        """
        Start monitoring events and sending notifications.
        
        Args:
            recipients: Phone number(s) to notify
            interval_seconds: Check interval in seconds
            message_template: Template for notification messages
        """
        print("Debug - Start monitoring with recipients:", recipients)  # Debug print
        self.logger.info("Starting event monitoring...")
        
        while True:
            event = self.check_events()
            if event:
                print("Debug - Found event:", event)  # Debug print
                message = message_template.format(
                    name=event['name'],
                    time=event['datetime'].strftime('%Y-%m-%d %H:%M:%S')
                )
                print("Debug - Sending message:", message)  # Debug print
                self.send_sms(recipients, message)
                
            time.sleep(interval_seconds)
    
    def clear_events(self):
        """Clear all events from the monitoring list."""
        self.events = []
        self.logger.info("Cleared all events")
