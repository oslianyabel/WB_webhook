import requests
import json
import os
from typing import Optional, Dict, Any


class WhatsAppSender:
    def __init__(self, access_token: str, phone_number_id: str):
        """
        Initialize WhatsApp Business API sender

        Args:
            access_token: Your WhatsApp Business API access token
            phone_number_id: Your WhatsApp Business phone number ID
        """
        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.base_url = f"https://graph.facebook.com/v22.0/{phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    def send_template_message(
        self,
        to: str,
        template_name: str,
        language_code: str = "en_US",
        template_parameters: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Send a template message

        Args:
            to: Recipient phone number (with country code, no + sign)
            template_name: Name of the approved template
            language_code: Language code (default: en_US)
            template_parameters: List of parameters for the template

        Returns:
            API response as dictionary
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {"name": template_name, "language": {"code": language_code}},
        }

        # Add parameters if provided
        if template_parameters:
            payload["template"]["components"] = [
                {"type": "body", "parameters": template_parameters}
            ]

        return self._send_request(payload)

    def send_text_message(self, to: str, message: str) -> Dict[str, Any]:
        """
        Send a text message

        Args:
            to: Recipient phone number (with country code, no + sign)
            message: Text message to send

        Returns:
            API response as dictionary
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": message},
        }

        return self._send_request(payload)

    def send_media_message(
        self, to: str, media_type: str, media_id: str, caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a media message (image, document, audio, video)

        Args:
            to: Recipient phone number
            media_type: Type of media (image, document, audio, video)
            media_id: Media ID from uploaded media
            caption: Optional caption for the media

        Returns:
            API response as dictionary
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": media_type,
            media_type: {"id": media_id},
        }

        if caption and media_type in ["image", "document", "video"]:
            payload[media_type]["caption"] = caption

        return self._send_request(payload)

    def _send_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send HTTP request to WhatsApp API

        Args:
            payload: Request payload

        Returns:
            API response as dictionary
        """
        try:
            response = requests.post(
                self.base_url, headers=self.headers, data=json.dumps(payload)
            )

            response_data = response.json()

            if response.status_code == 200:
                print(f"✅ Message sent successfully!")
                print(
                    f"Message ID: {response_data.get('messages', [{}])[0].get('id', 'N/A')}"
                )
            else:
                print(f"❌ Error sending message:")
                print(f"Status Code: {response.status_code}")
                print(f"Error: {response_data}")

            return response_data

        except requests.exceptions.RequestException as e:
            error_response = {"error": f"Request failed: {str(e)}"}
            print(f"❌ Request failed: {e}")
            return error_response
        except json.JSONDecodeError as e:
            error_response = {"error": f"Invalid JSON response: {str(e)}"}
            print(f"❌ Invalid JSON response: {e}")
            return error_response


def main():
    """
    Example usage of the WhatsApp sender
    """
    # Configuration - Replace with your actual values
    ACCESS_TOKEN = "EAAeai7oRo0MBPJkOMEfu0hmfsAWjGVEUHJIpgG9SEFYlmYCJWdN16HLW3p1ZC9DeImZCoSzLz7GcHTfeMD2i4fVhR89ZAgcAs8RU09v9nTTAcciRDwYZCNp8gFovJgfPQoZBTOKupOWhg5Qhd3LZANcaFQOOrWIkiDOtuI3ZASuoflRnF0Xn6LNDLrRU0CZBXhtJ5VcddcVfFZB9fNv2OmcYau3QupZA1zuO97JOti6ONaFikFmEU3YsBekI4CMwZDZD"
    PHONE_NUMBER_ID = "623728147496373"
    RECIPIENT = "18352353226"

    # Initialize sender
    wa_sender = WhatsAppSender(ACCESS_TOKEN, PHONE_NUMBER_ID)

    print("WhatsApp Business API Message Sender")
    print("====================================\n")

    # Example 1: Send template message (like your curl example)
    print("1. Sending template message...")
    template_response = wa_sender.send_template_message(
        to=RECIPIENT, template_name="hello_world", language_code="en_US"
    )
    print(f"Response: {json.dumps(template_response, indent=2)}\n")

    # Example 2: Send text message
    print("2. Sending text message...")
    text_response = wa_sender.send_text_message(
        to=RECIPIENT, message="¡Hola! Este es un mensaje de prueba desde Python 🐍"
    )
    print(f"Response: {json.dumps(text_response, indent=2)}\n")


if __name__ == "__main__":
    main()
