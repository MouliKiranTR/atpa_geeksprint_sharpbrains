"""
OpenArena Service for program generation using AI

This service provides functionality to generate programs using the 
OpenArena API with the Claude Sonnet model.
"""

from typing import Dict, Any, Optional
import requests

from app.utils.openarena_authenticator import OpenArenaAuthenticator


class OpenArenaService:
    """Service for interacting with OpenArena API for program generation"""
    
    def __init__(self):
        self.auth = OpenArenaAuthenticator()
        self.workflow_id = "592081d1-0a6e-4b5f-93b1-a08a674bf4bc"
        self.base_url = (
            "https://aiopenarena.gcs.int.thomsonreuters.com/v1/inference"
        )
        self.model_name = "anthropic_direct.claude-v4-sonnet"
    
    def _get_default_model_params(self) -> Dict[str, Any]:
        """Get default model parameters for Claude Sonnet"""
        return {
            "temperature": "0.7",
            "top_p": "1",
            "max_tokens": "63999",
            "top_k": "250",
            "system_prompt": (
                "You are an experienced Python developer. "
                "Write efficient, clean, and well-documented programs."
            ),
            "enable_reasoning": "true",
            "budget_tokens": "35425"
        }
    
    def _create_payload(
        self, 
        user_input: str, 
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create request payload for OpenArena API
        
        Args:
            user_input: User's program description
            system_prompt: Optional custom system prompt
            
        Returns:
            API request payload
        """
        model_params = self._get_default_model_params()
        
        if system_prompt:
            model_params["system_prompt"] = system_prompt
        
        return {
            "workflow_id": self.workflow_id,
            "query": user_input,
            "is_persistence_allowed": True,
            "modelparams": {
                self.model_name: model_params
            }
        }
    
    def _extract_response_data(
        self, response_json: Dict[str, Any]
    ) -> tuple[str, Optional[float]]:
        """
        Extract program and cost from API response
        
        Args:
            response_json: JSON response from OpenArena API
            
        Returns:
            Tuple of (program_code, cost)
        """
        try:
            result = response_json.get('result', {})
            answer = result.get('answer', {})
            program = answer.get(self.model_name, '')
            
            cost_track = result.get('cost_track', {})
            cost = cost_track.get('total_cost')
            
            return program, cost
        except (KeyError, TypeError) as e:
            print(f"⚠️ Error extracting response data: {e}")
            return '', None
    
    def generate_program(
        self, 
        user_input: str, 
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a program based on user input using OpenArena API
        
        Args:
            user_input: User's description of the desired program
            system_prompt: Optional custom system prompt
            
        Returns:
            Dictionary with program, cost, and status information
        """
        try:
            # Get authentication token
            openarena_token = self.auth.authenticate_and_get_token()
            
            # Prepare headers and payload
            headers = {
                'Authorization': f'Bearer {openarena_token}',
                'Content-Type': 'application/json'
            }
            
            payload = self._create_payload(user_input, system_prompt)
            
            # Make API request
            print("🚀 Sending request to OpenArena API...")
            response = requests.post(
                self.base_url, headers=headers, json=payload
            )
            
            print(f"📡 OpenArena API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                program, cost = self._extract_response_data(response_data)
                
                program_preview = (
                    program[:100] + "..." if len(program) > 100 else program
                )
                print("💬 Generated Program:", program_preview)
                print("💲 Estimated Query Cost:", cost)
                
                return {
                    "program": program,
                    "cost": cost,
                    "status": "success"
                }
            else:
                error_msg = (
                    f"API returned status {response.status_code}: "
                    f"{response.text}"
                )
                print(f"⚠️ OpenArena Error: {error_msg}")
                
                return {
                    "program": "",
                    "cost": None,
                    "status": "error",
                    "error": error_msg
                }
                
        except requests.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            print(f"🚨 Failed to Generate Program: {error_msg}")
            
            return {
                "program": "",
                "cost": None,
                "status": "error",
                "error": error_msg
            }
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"🚨 Failed to Generate Program: {error_msg}")
            
            return {
                "program": "",
                "cost": None,
                "status": "error",
                "error": error_msg
            }


# Global service instance
open_arena_service = OpenArenaService()


# Legacy function for backward compatibility
def generate_program(user_input: str) -> Dict[str, Any]:
    """
    Legacy function for backward compatibility
    
    Args:
        user_input: User's program description
        
    Returns:
        Generated program result
    """
    return open_arena_service.generate_program(user_input)
