import json
import os
from typing import Dict, Optional

class PersonalityManager:
    """
    Manager class for handling AI personality configurations.
    """
    
    def __init__(self, personalities_file: str = "personalities.json"):
        self.personalities_file = personalities_file
        self._personalities = None
        self._load_personalities()
    
    def _load_personalities(self):
        """
        Load personalities from JSON file.
        """
        try:
            if os.path.exists(self.personalities_file):
                with open(self.personalities_file, 'r', encoding='utf-8') as file:
                    self._personalities = json.load(file)
            else:
                # Create default personalities if file doesn't exist
                self._personalities = self._get_default_personalities()
                self._save_personalities()
        except Exception as e:
            print(f"Error loading personalities: {e}")
            self._personalities = self._get_default_personalities()
    
    def _save_personalities(self):
        """
        Save personalities to JSON file.
        """
        try:
            with open(self.personalities_file, 'w', encoding='utf-8') as file:
                json.dump(self._personalities, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving personalities: {e}")
    
    def _get_default_personalities(self) -> Dict:
        """
        Get default personality configurations.
        
        Returns:
            Dict: Default personalities
        """
        return {
            "1": {
                "name": "Pepper Amigable",
                "system_prompt": "Eres un asistente de IA el cual potencia al robot Pepper. Responde a las preguntas de los usuarios de manera clara y concisa como si fueras dicho robot Pepper. En la medida de lo posible, responde en español y que sean alrededor de 15-20 palabras."
            }
        }
    
    def get_personality(self, personality_id: str) -> Optional[Dict]:
        """
        Get personality configuration by ID.
        
        Args:
            personality_id (str): ID of the personality
            
        Returns:
            Optional[Dict]: Personality configuration (name, system_prompt) or (None, None) if not found
        """
        return self._personalities.get(str(personality_id))
    
    def get_available_personalities(self) -> Dict:
        """
        Get all available personalities.
        
        Returns:
            Dict: All personality configurations
        """
        return self._personalities.copy()

if __name__ == "__main__":
    pm = PersonalityManager()
    print(pm.get_personality(2))