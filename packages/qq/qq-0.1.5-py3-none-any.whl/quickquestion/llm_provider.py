#!/usr/bin/env python3
# llm_provider.py

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
import requests
import json
import os

class LLMProvider(ABC):
    """Base class for LLM providers"""
    
    PREFERRED_MODELS = [
        "mistral", 
        "llama2", 
        "codellama", 
        "openhermes", 
        "neural-chat",
        "stable-beluga",
        "qwen",
        "yi"
    ]

    def _check_special_characters(self, content: str) -> dict:
        """Check content for special characters in a Python-version-compatible way"""
        null_byte = chr(0)  # Instead of using \x00
        newline = chr(10)   # Instead of using \n
        carriage_return = chr(13)  # Instead of using \r
        tab = chr(9)        # Instead of using \t
        
        return {
            "length": len(content),
            "first_chars": [ord(c) for c in content[:10]],
            "has_null_bytes": null_byte in content,
            "has_newlines": newline in content,
            "has_carriage_returns": carriage_return in content,
            "has_tabs": tab in content,
            "starts_with_markdown": content.startswith('```'),
            "ends_with_markdown": content.endswith('```'),
            "starts_with_bracket": content.startswith('['),
            "ends_with_bracket": content.endswith(']')
        }
    
    def _parse_llm_response(self, content: str) -> List[str]:
        """
        Enhanced response parser for LLM outputs.
        Handles complex escape sequences and nested quotes.
        """
        def sanitize_command(cmd: str) -> str:
            """Helper function to clean up individual commands"""
            # Replace escaped quotes with temporary markers
            cmd = cmd.replace('\\"', '¤¤QUOTE¤¤')
            # Replace escaped parentheses
            cmd = cmd.replace('\\(', '(').replace('\\)', ')')
            # Replace back the quotes
            cmd = cmd.replace('¤¤QUOTE¤¤', '"')
            return cmd

        try:
            # Get the content from the LLM response
            if isinstance(content, str):
                # Handle raw string to avoid escape character issues
                content = content.encode().decode('unicode-escape')
                
                # Handle markdown code blocks
                if content.startswith('```') and content.endswith('```'):
                    content = content.strip('`')
                    if content.startswith('json\n'):
                        content = content[5:]
                content = content.strip()
                
                try:
                    # Parse the outer JSON structure
                    commands = json.loads(content)
                    # Clean up each command
                    return [sanitize_command(cmd) for cmd in commands]
                except json.JSONDecodeError:
                    # If JSON parsing fails, try to extract commands manually
                    if content.startswith('[') and content.endswith(']'):
                        # Remove outer brackets
                        content = content[1:-1]
                        # Split by commas not inside quotes
                        import re
                        commands = re.findall(r'"([^"]*)"', content)
                        return [sanitize_command(cmd) for cmd in commands]
                    else:
                        raise Exception("Invalid response format")
            else:
                raise Exception("Unexpected response type")
                
        except Exception as e:
            raise Exception(f"Error parsing response: {str(e)}\nRaw content: {content}")

    @abstractmethod
    def check_status(self) -> bool:
        """Check if the provider is available and ready"""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Optional[str]:
        """Get information about the currently loaded model"""
        pass
    
    @abstractmethod
    def generate_response(self, prompt: str) -> List[str]:
        """Generate a response from the model"""
        pass

    @abstractmethod
    def generate_response_with_debug(self, prompt: str) -> List[str]:
        """Generate a response from the model with debug information"""
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        pass
    
    def select_best_model(self, available_models: List[str]) -> Optional[str]:
        """Select the best model from available ones based on preferences"""
        available_lower = [m.lower() for m in available_models]
        
        for preferred in self.PREFERRED_MODELS:
            for available in available_lower:
                if preferred in available:
                    return available_models[available_lower.index(available)]
        
        return available_models[0] if available_models else None

class LMStudioProvider(LLMProvider):
    """LM Studio implementation of LLM provider"""
    
    def __init__(self):
        self.api_url = "http://localhost:1234/v1"
        self.current_model = None
    
    def get_available_models(self) -> List[str]:
        try:
            response = requests.get(f"{self.api_url}/models")
            if response.status_code == 200:
                models = response.json()
                if models.get('data'):
                    return [model['id'] for model in models['data']]
            return []
        except requests.exceptions.RequestException:
            return []
    
    def check_status(self) -> bool:
        available_models = self.get_available_models()
        if available_models:
            self.current_model = self.select_best_model(available_models)
            return True
        return False
    
    def get_model_info(self) -> Optional[str]:
        return self.current_model
    
    def generate_response(self, prompt: str) -> List[str]:
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200,
            "model": self.current_model
        }
        
        try:
            response = requests.post(f"{self.api_url}/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return self._parse_llm_response(content)
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            raise Exception(f"Error generating response: {str(e)}")

    def generate_response_with_debug(self, prompt: str) -> List[str]:
        """Generate a response from the model with debug information"""
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200,
            "model": self.current_model
        }
        
        try:
            print("\nDEBUG: Making request to LM Studio API...")
            print(f"DEBUG: Request URL: {self.api_url}/chat/completions")
            print(f"DEBUG: Request headers: {json.dumps(headers, indent=2)}")
            print(f"DEBUG: Request data: {json.dumps(data, indent=2)}")
            
            response = requests.post(f"{self.api_url}/chat/completions", headers=headers, json=data)
            print(f"\nDEBUG: Response status code: {response.status_code}")
            print(f"DEBUG: Response headers: {json.dumps(dict(response.headers), indent=2)}")
            
            response.raise_for_status()
            response_json = response.json()
            print(f"DEBUG: Response JSON: {json.dumps(response_json, indent=2)}")
            
            content = response_json["choices"][0]["message"]["content"]
            print(f"\nDEBUG: Raw content before parsing: {content}")
            
            parsed = self._parse_llm_response(content)
            print(f"\nDEBUG: Final parsed commands: {json.dumps(parsed, indent=2)}")
            
            return parsed
            
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"\nDEBUG: Error occurred: {str(e)}")
            if isinstance(e, requests.exceptions.RequestException):
                print(f"DEBUG: Full response text: {e.response.text if hasattr(e, 'response') else 'No response text'}")
            raise Exception(f"Error generating response: {str(e)}")

class OllamaProvider(LLMProvider):
    """Ollama implementation of LLM provider"""
    
    def __init__(self):
        self.api_url = "http://localhost:11434/api"
        self.current_model = None
    
    def get_available_models(self) -> List[str]:
        try:
            response = requests.get(f"{self.api_url}/tags")
            if response.status_code == 200:
                models = response.json()
                if models.get('models'):
                    return [model['name'] for model in models['models']]
            return []
        except requests.exceptions.RequestException:
            return []
    
    def check_status(self) -> bool:
        available_models = self.get_available_models()
        if available_models:
            self.current_model = self.select_best_model(available_models)
            return True
        return False
    
    def get_model_info(self) -> Optional[str]:
        return self.current_model
    
    def generate_response(self, prompt: str) -> List[str]:
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.current_model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(f"{self.api_url}/generate", headers=headers, json=data)
            response.raise_for_status()
            content = response.json()["response"]
            return self._parse_llm_response(content)
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            raise Exception(f"Error generating response: {str(e)}")

    def generate_response_with_debug(self, prompt: str) -> List[str]:
        """Generate a response from the model with debug information"""
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.current_model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.7
        }
        
        try:
            print("\nDEBUG: Making request to Ollama API...")
            print(f"DEBUG: Request URL: {self.api_url}/generate")
            print(f"DEBUG: Request headers: {json.dumps(headers, indent=2)}")
            print(f"DEBUG: Request data: {json.dumps(data, indent=2)}")
            
            response = requests.post(f"{self.api_url}/generate", headers=headers, json=data)
            print(f"\nDEBUG: Response status code: {response.status_code}")
            print(f"DEBUG: Response headers: {json.dumps(dict(response.headers), indent=2)}")
            
            response.raise_for_status()
            response_json = response.json()
            print(f"DEBUG: Response JSON: {json.dumps(response_json, indent=2)}")
            
            content = response_json["response"]
            print(f"\nDEBUG: Raw content before parsing: {content}")
            
            parsed = self._parse_llm_response(content)
            print(f"\nDEBUG: Final parsed commands: {json.dumps(parsed, indent=2)}")
            
            return parsed
            
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"\nDEBUG: Error occurred: {str(e)}")
            if isinstance(e, requests.exceptions.RequestException):
                print(f"DEBUG: Full response text: {e.response.text if hasattr(e, 'response') else 'No response text'}")
            raise Exception(f"Error generating response: {str(e)}")

class AnthropicProvider(LLMProvider):
    """Anthropic implementation of LLM provider using the official SDK"""
    
    def __init__(self):
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')
        self.current_model = None
        try:
            import anthropic
            from anthropic.types import Model
            self.client = anthropic.Anthropic(api_key=self.api_key)
            
            # Get models by inspecting the Model type at runtime
            union_args = Model.__args__
            literal_type = union_args[1]
            self.available_models = list(literal_type.__args__)
        except ImportError:
            print("Anthropic SDK not installed. Please install with: pip install anthropic")
            self.client = None
            self.available_models = []
    
    def get_available_models(self) -> List[str]:
        if not self.api_key or not self.client:
            return []
        return self.available_models
    
    def check_status(self) -> bool:
        if not self.api_key or not self.client:
            return False
            
        try:
            if self.available_models:
                self.current_model = self.select_best_model(self.available_models)
                return True
            return False
        except Exception:
            return False
    
    def get_model_info(self) -> Optional[str]:
        return self.current_model
    
    def generate_response(self, prompt: str) -> List[str]:
        if not self.current_model:
            raise Exception("No model selected")
            
        try:
            message = self.client.messages.create(
                model=self.current_model,
                max_tokens=200,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return self._parse_llm_response(message.content[0].text)
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

    def generate_response_with_debug(self, prompt: str) -> List[str]:
        """Generate a response from the model with debug information"""
        if not self.current_model:
            raise Exception("No model selected")
            
        try:
            print("\nDEBUG: Making request to Anthropic API...")
            print(f"DEBUG: Using model: {self.current_model}")
            print("DEBUG: Request data:", {
                "model": self.current_model,
                "max_tokens": 200,
                "temperature": 0.7,
                "messages": [{"role": "user", "content": prompt}]
            })
            
            message = self.client.messages.create(
                model=self.current_model,
                max_tokens=200,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            print("\nDEBUG: Response received")
            print(f"DEBUG: Raw response: {message}")
            print(f"\nDEBUG: Raw content before parsing: {message.content[0].text}")
            
            parsed = self._parse_llm_response(message.content[0].text)
            print(f"\nDEBUG: Final parsed commands: {json.dumps(parsed, indent=2)}")
            
            return parsed
            
        except Exception as e:
            print(f"\nDEBUG: Error occurred: {str(e)}")
            import traceback
            print(f"DEBUG: Full traceback: {traceback.format_exc()}")
            raise Exception(f"Error generating response: {str(e)}") 
       
class OpenAIProvider(LLMProvider):
    """OpenAI implementation of LLM provider"""
    
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        self.api_url = "https://api.openai.com/v1"
        self.current_model = None
        # Default preferred OpenAI models
        self.available_models = [
            "gpt-4",
            "gpt-4-turbo-preview",
            "gpt-3.5-turbo"
        ]
    
    def get_available_models(self) -> List[str]:
        if not self.api_key:
            return []
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(f"{self.api_url}/models", headers=headers)
            if response.status_code == 200:
                models = response.json()
                # Filter to only get chat models
                chat_models = [
                    model['id'] for model in models['data']
                    if any(preferred in model['id'] for preferred in ['gpt-4', 'gpt-3.5'])
                ]
                return chat_models if chat_models else self.available_models
            return self.available_models
        except requests.exceptions.RequestException:
            # Fallback to default models if API call fails
            return self.available_models
    
    def check_status(self) -> bool:
        if not self.api_key:
            return False
            
        available_models = self.get_available_models()
        if available_models:
            self.current_model = self.select_best_model(available_models)
            return True
        return False
    
    def get_model_info(self) -> Optional[str]:
        return self.current_model
    
    def generate_response(self, prompt: str) -> List[str]:
        """Generate a response from the model"""
        if not self.current_model:
            raise Exception("No model selected")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.current_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }
        
        try:
            response = requests.post(f"{self.api_url}/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            
            # Handle markdown code blocks
            if content.startswith('```') and content.endswith('```'):
                content = content.strip('`')
                if content.startswith('json\n'):
                    content = content[5:]
            content = content.strip()
            
            return self._parse_llm_response(content)
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            raise Exception(f"Error generating response: {str(e)}")

    def generate_response_with_debug(self, prompt: str) -> List[str]:
        """Generate a response from the model with debug information"""
        if not self.current_model:
            raise Exception("No model selected")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.current_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }
        
        try:
            print("\nDEBUG: Making request to OpenAI API...")
            print(f"DEBUG: Request URL: {self.api_url}/chat/completions")
            
            # Mask the API key in debug output
            debug_headers = headers.copy()
            debug_headers["Authorization"] = "Bearer ***"
            print(f"DEBUG: Request headers: {json.dumps(debug_headers, indent=2)}")
            print(f"DEBUG: Request data: {json.dumps(data, indent=2)}")
            
            response = requests.post(f"{self.api_url}/chat/completions", headers=headers, json=data)
            print(f"\nDEBUG: Response status code: {response.status_code}")
            print(f"DEBUG: Response headers: {json.dumps(dict(response.headers), indent=2)}")
            
            response.raise_for_status()
            response_json = response.json()
            print(f"DEBUG: Response JSON: {json.dumps(response_json, indent=2)}")
            
            content = response_json["choices"][0]["message"]["content"]
            print("\nDEBUG: Raw content before parsing:", content)
            
            # Check for special characters
            char_analysis = self._check_special_characters(content)
            print("\nDEBUG: Content analysis:")
            for key, value in char_analysis.items():
                print(f"DEBUG: {key}: {value}")
            
            # Handle markdown code blocks
            if char_analysis["starts_with_markdown"] and char_analysis["ends_with_markdown"]:
                print("DEBUG: Detected markdown code block, cleaning...")
                content = content.strip('`')
                if content.startswith('json\n'):
                    content = content[5:]
                content = content.strip()
                print("DEBUG: Content after markdown cleanup:", content)
            
            try:
                # Try parsing as JSON first
                print("\nDEBUG: Attempting JSON parse...")
                json_data = json.loads(content)
                if isinstance(json_data, list):
                    print("DEBUG: Successfully parsed as JSON array")
                    parsed = [str(cmd) for cmd in json_data]
                else:
                    raise ValueError("JSON data is not an array")
            except json.JSONDecodeError as e:
                print("DEBUG: JSON parse failed:", str(e))
                print("DEBUG: Falling back to manual parsing...")
                # Manual parsing as fallback
                if content.startswith('[') and content.endswith(']'):
                    content = content[1:-1]
                    import re
                    parsed = re.findall(r'"([^"]*)"', content)
                else:
                    raise Exception("Content is not in expected format")
            
            print("\nDEBUG: Final parsed commands:", json.dumps(parsed, indent=2))
            return parsed
            
        except Exception as e:
            print("\nDEBUG: Error occurred:", str(e))
            if isinstance(e, requests.exceptions.RequestException) and hasattr(e, 'response'):
                print("DEBUG: Full response text:", e.response.text)
            import traceback
            print("DEBUG: Full traceback:", traceback.format_exc())
            raise Exception(f"Error generating response: {str(e)}")
        
class GroqProvider(LLMProvider):
    """Groq implementation of LLM provider using their OpenAI-compatible API"""
    
    def __init__(self):
        self.api_key = os.environ.get('GROQ_API_KEY')
        self.api_url = "https://api.groq.com/openai/v1"
        self.current_model = None
    
    def get_available_models(self) -> List[str]:
        """Fetch available models from Groq API"""
        if not self.api_key:
            return []
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(f"{self.api_url}/models", headers=headers)
            response.raise_for_status()
            
            models_data = response.json()
            # Filter to get only text models (exclude whisper and vision models)
            text_models = [
                model["id"] for model in models_data["data"]
                if not any(x in model["id"].lower() for x in ["whisper", "vision"])
                and model["active"]
            ]
            
            # Sort to ensure newer models appear first
            text_models.sort(reverse=True)
            return text_models
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Groq models: {str(e)}")
            return []
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing Groq models response: {str(e)}")
            return []
    
    def check_status(self) -> bool:
        """Check if the provider is available and ready"""
        if not self.api_key:
            return False
            
        try:
            models = self.get_available_models()
            if models:
                self.current_model = self.select_best_model(models)
                return True
            return False
        except Exception:
            return False
    
    def get_model_info(self) -> Optional[str]:
        """Get information about the currently loaded model"""
        return self.current_model
    
    def generate_response(self, prompt: str) -> List[str]:
        """Generate a response from the model"""
        if not self.current_model:
            raise Exception("No model selected")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.current_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }
        
        try:
            response = requests.post(f"{self.api_url}/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            
            # Handle markdown code blocks
            if content.startswith('```') and content.endswith('```'):
                content = content.strip('`')
                if content.startswith('json\n'):
                    content = content[5:]
            content = content.strip()
            
            return self._parse_llm_response(content)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error connecting to Groq API: {str(e)}")
        except (KeyError, json.JSONDecodeError) as e:
            raise Exception(f"Error parsing Groq response: {str(e)}")

    def generate_response_with_debug(self, prompt: str) -> List[str]:
        """Generate a response from the model with debug information"""
        if not self.current_model:
            raise Exception("No model selected")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.current_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }
        
        try:
            print("\nDEBUG: Making request to Groq API...")
            print(f"DEBUG: Request URL: {self.api_url}/chat/completions")
            # Mask the API key in debug output
            debug_headers = headers.copy()
            debug_headers["Authorization"] = "Bearer ***"
            print(f"DEBUG: Request headers: {json.dumps(debug_headers, indent=2)}")
            print(f"DEBUG: Request data: {json.dumps(data, indent=2)}")
            
            response = requests.post(f"{self.api_url}/chat/completions", headers=headers, json=data)
            print(f"\nDEBUG: Response status code: {response.status_code}")
            print(f"DEBUG: Response headers: {json.dumps(dict(response.headers), indent=2)}")
            
            response.raise_for_status()
            response_json = response.json()
            # Mask any sensitive data in response JSON if needed
            print(f"DEBUG: Response JSON: {json.dumps(response_json, indent=2)}")
            
            content = response_json["choices"][0]["message"]["content"]
            print(f"\nDEBUG: Raw content before parsing: {content}")
            
            # Handle markdown code blocks
            if content.startswith('```') and content.endswith('```'):
                print("DEBUG: Detected markdown code block, cleaning...")
                content = content.strip('`')
                if content.startswith('json\n'):
                    content = content[5:]
                content = content.strip()
                print(f"DEBUG: Content after markdown cleanup: {content}")
            
            # Additional debug output for problematic characters
            print("\nDEBUG: Character analysis:")
            print(f"DEBUG: Content length: {len(content)}")
            print(f"DEBUG: First 10 characters: {[ord(c) for c in content[:10]]}")
            print(f"DEBUG: Contains null bytes: {'\\x00' in content}")
            print(f"DEBUG: Contains escape characters: {any(c in content for c in ['\\n', '\\r', '\\t'])}")
            
            try:
                # Try parsing as JSON first
                print("\nDEBUG: Attempting JSON parse...")
                json_data = json.loads(content)
                if isinstance(json_data, list):
                    print("DEBUG: Successfully parsed as JSON array")
                    parsed = [str(cmd) for cmd in json_data]
                else:
                    raise ValueError("JSON data is not an array")
            except json.JSONDecodeError as e:
                print(f"DEBUG: JSON parse failed: {str(e)}")
                print("DEBUG: Falling back to manual parsing...")
                # Manual parsing as fallback
                if content.startswith('[') and content.endswith(']'):
                    content = content[1:-1]
                    import re
                    parsed = re.findall(r'"([^"]*)"', content)
                else:
                    raise Exception("Content is not in expected format")
            
            print(f"\nDEBUG: Final parsed commands: {json.dumps(parsed, indent=2)}")
            return parsed
            
        except Exception as e:
            print(f"\nDEBUG: Error occurred: {str(e)}")
            if isinstance(e, requests.exceptions.RequestException) and hasattr(e, 'response'):
                print(f"DEBUG: Full response text: {e.response.text}")
            import traceback
            print(f"DEBUG: Full traceback: {traceback.format_exc()}")
            raise Exception(f"Error generating response: {str(e)}")