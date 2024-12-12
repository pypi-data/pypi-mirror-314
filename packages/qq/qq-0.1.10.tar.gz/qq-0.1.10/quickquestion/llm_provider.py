#!/usr/bin/env python3
# llm_provider.py

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
import requests
import json
import os
import asyncio
import aiohttp
import sys
import ssl

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

    async def async_check_status(self, debug=False) -> bool:
        """Async version of status check with enhanced debugging"""
        if debug:
            print(f"\nDEBUG Provider: Starting async status check for {self.__class__.__name__}")
        
        try:
            # For SDK-based providers that don't use HTTP endpoints
            if not hasattr(self, 'api_url'):
                if debug:
                    print(f"DEBUG Provider: Using direct SDK connection")
                # Use get_available_models directly for SDK-based providers
                models = self.get_available_models()
                if models:
                    self.current_model = self.select_best_model(models)
                    if debug:
                        print(f"DEBUG Provider: Found models: {models}")
                        print(f"DEBUG Provider: Selected model: {self.current_model}")
                    return True
                if debug:
                    print(f"DEBUG Provider: No models found")
                return False
            
            # For HTTP API-based providers
            if debug:
                print(f"DEBUG Provider: API URL = {self.api_url}")
            
            try:
                async with aiohttp.ClientSession() as session:
                    if debug:
                        print("DEBUG Provider: Established aiohttp session")
                        print(f"DEBUG Provider: Attempting connection to {self.api_url}")
                    
                    try:
                        async with session.get(self.api_url, timeout=2.0) as response:
                            if debug:
                                print(f"DEBUG Provider: Response status: {response.status}")
                                print(f"DEBUG Provider: Response headers: {dict(response.headers)}")
                            return response.status == 200
                    except asyncio.TimeoutError:
                        if debug:
                            print("DEBUG Provider: Connection timeout")
                        return False
                    except aiohttp.ClientError as e:
                        if debug:
                            print(f"DEBUG Provider: Connection error: {str(e)}")
                        return False
            except Exception as e:
                if debug:
                    print(f"DEBUG Provider: Connection error: {str(e)}")
                return False
                
        except Exception as e:
            if debug:
                print(f"DEBUG Provider: Unexpected error: {str(e)}")
                import traceback
                print("DEBUG Provider: Full traceback:")
                traceback.print_exc()
            return False
        
    def check_status(self, debug=False) -> bool:
        """Sync wrapper for async status check with debugging"""
        try:
            if debug:
                print(f"\nDEBUG Provider: Setting up async loop for {self.__class__.__name__}")
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            if debug:
                print("DEBUG Provider: Created new event loop")
                
            result = loop.run_until_complete(self.async_check_status(debug=debug))
            
            if debug:
                print(f"DEBUG Provider: Async check completed with result: {result}")
                
            loop.close()
            
            if debug:
                print("DEBUG Provider: Closed event loop")
                
            return result
        except Exception as e:
            if debug:
                print(f"DEBUG Provider: Error in async wrapper: {str(e)}")
                import traceback
                print("DEBUG Provider: Full traceback:")
                traceback.print_exc()
            return False
    
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
        # Initialize with a default model
        self.default_model = "model"  # LM Studio requires any non-null value
    
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
            "model": self.current_model or self.default_model  # Use default if no model set
        }
        
        try:
            response = requests.post(f"{self.api_url}/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return self._parse_llm_response(content)
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            raise Exception(f"Error generating response: {str(e)}")

    def generate_response_with_debug(self, prompt: str) -> List[str]:
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
            "model": self.current_model or self.default_model  # Use default if no model set
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
    
class OllamaProvider(LLMProvider):
    """Ollama implementation of LLM provider"""
    
    def __init__(self):
        self.api_url = "http://localhost:11434/api"
        self.current_model = None
    
    def get_available_models(self) -> List[str]:
        """Get available models with better error handling"""
        try:
            response = requests.get(f"{self.api_url}/tags", timeout=2.0)
            
            if response.status_code == 200:
                models = response.json()
                if models.get('models'):
                    return [model['name'] for model in models['models']]
            return []
            
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Ollama: {str(e)}")
            return []

    def select_best_model(self, available_models: List[str]) -> Optional[str]:
        """Enhanced model selection for Ollama"""
        available_lower = [m.lower() for m in available_models]
        
        # First try exact matches with preferred models
        for preferred in self.PREFERRED_MODELS:
            for available in available_lower:
                if preferred == available:
                    return available_models[available_lower.index(available)]
        
        # Then try partial matches
        for preferred in self.PREFERRED_MODELS:
            for available in available_lower:
                if preferred in available:
                    return available_models[available_lower.index(available)]
        
        # If no matches, return first available
        return available_models[0] if available_models else None
    
    async def async_check_status(self, debug=False) -> bool:
        """Async version of status check with enhanced error handling"""
        if debug:
            print(f"\nDEBUG Provider: Starting async status check for {self.__class__.__name__}")
            print(f"DEBUG Provider: API URL = {self.api_url}")
        
        try:
            async with aiohttp.ClientSession() as session:
                if debug:
                    print("DEBUG Provider: Established aiohttp session")
                    print(f"DEBUG Provider: Attempting connection to {self.api_url}/tags")
                
                try:
                    # Ollama uses /api/tags to list models
                    async with session.get(f"{self.api_url}/tags", timeout=2.0) as response:
                        if debug:
                            print(f"DEBUG Provider: Response status: {response.status}")
                            print(f"DEBUG Provider: Response headers: {dict(response.headers)}")
                            
                            if response.status != 200:
                                text = await response.text()
                                print(f"DEBUG Provider: Error response: {text}")
                        
                        # Only consider 200 as success
                        if response.status == 200:
                            models_data = await response.json()
                            if models_data.get('models'):
                                available_models = [m['name'] for m in models_data['models']]
                                if debug:
                                    print(f"DEBUG Provider: Found models: {available_models}")
                                self.current_model = self.select_best_model(available_models)
                                if debug:
                                    print(f"DEBUG Provider: Selected model: {self.current_model}")
                                return True
                            else:
                                if debug:
                                    print("DEBUG Provider: No models found in response")
                                return False
                        
                        if debug:
                            print("DEBUG Provider: Unsuccessful status code")
                        return False
                        
                except asyncio.TimeoutError:
                    if debug:
                        print("DEBUG Provider: Connection timeout")
                    return False
                except aiohttp.ClientError as e:
                    if debug:
                        print(f"DEBUG Provider: Connection error: {str(e)}")
                        print(f"DEBUG Provider: Is Ollama running at {self.api_url}?")
                    return False
                
        except Exception as e:
            if debug:
                print(f"DEBUG Provider: Unexpected error: {str(e)}")
                import traceback
                print("DEBUG Provider: Full traceback:")
                traceback.print_exc()
            return False

    def check_status(self, debug=False) -> bool:
        """Sync version of status check"""
        if debug:
            print(f"\nDEBUG Provider: Checking Ollama status")
        
        try:
            available_models = self.get_available_models()
            if available_models:
                self.current_model = self.select_best_model(available_models)
                if debug:
                    print(f"DEBUG Provider: Found models: {available_models}")
                    print(f"DEBUG Provider: Selected model: {self.current_model}")
                return True
            return False
        except Exception as e:
            if debug:
                print(f"DEBUG Provider: Error checking status: {str(e)}")
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
        self.client = None
        self.available_models = []

        if not self.api_key:
            if self.debug:
                print("DEBUG: No Anthropic API key found in environment")
            return

        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
            
            # Define default models - these will be used if we can't get them from the SDK
            self.available_models = [
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307",
                "claude-2.1",
                "claude-2.0",
                "claude-instant-1.2"
            ]

            # Try to get models from the SDK if possible
            try:
                from anthropic.types import Model
                if hasattr(Model, '__args__'):
                    union_args = Model.__args__
                    if len(union_args) > 1:
                        literal_type = union_args[1]
                        sdk_models = list(literal_type.__args__)
                        if sdk_models:
                            self.available_models = sdk_models
            except (ImportError, AttributeError, IndexError) as e:
                if self.debug:
                    print(f"DEBUG: Using default models list due to error: {str(e)}")

        except ImportError as e:
            if "anthropic" in str(e):
                print("Anthropic SDK not installed. Please install with: pip install anthropic")
            else:
                print(f"Error importing Anthropic SDK: {str(e)}")
            self.client = None
            self.available_models = []
        except Exception as e:
            print(f"Error initializing Anthropic client: {str(e)}")
            self.client = None
            self.available_models = []
    
    def get_available_models(self) -> List[str]:
        if not self.api_key or not self.client:
            return []
        return self.available_models
    
    async def async_get_available_models(self, debug=False) -> List[str]:
        """Async version of get_available_models"""
        if debug:
            print("DEBUG Anthropic: Checking available models")
        return self.get_available_models()
    
    def check_status(self) -> bool:
        if not self.api_key or not self.client:
            return False
            
        try:
            if self.available_models:
                self.current_model = self.select_best_model(self.available_models)
                return True
            return False
        except Exception as e:
            if self.debug:
                print(f"DEBUG: Error checking Anthropic status: {str(e)}")
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
        
        # Initialize SSL context
        self.ssl_context = self._create_ssl_context()
        
        self.available_models = [
            "gpt-4",
            "gpt-4-turbo-preview",
            "gpt-3.5-turbo"
        ]

    def _create_ssl_context(self) -> Optional[ssl.SSLContext]:
        """Create SSL context with proper certificate handling"""
        if sys.platform == 'darwin':
            # Try to find the certificates
            cert_paths = [
                '/usr/local/etc/openssl/cert.pem',  # Homebrew OpenSSL
                '/usr/local/etc/openssl@3/cert.pem',  # Homebrew OpenSSL 3
                '/etc/ssl/cert.pem',  # System SSL
                '/Library/Developer/CommandLineTools/usr/lib/python3/cert.pem'  # Python SSL
            ]
            
            for cert_path in cert_paths:
                if os.path.exists(cert_path):
                    ctx = ssl.create_default_context()
                    ctx.load_verify_locations(cert_path)
                    return ctx
        
        # For non-macOS or if no cert found, use default
        return None

    async def async_check_status(self, debug=False) -> bool:
        """Enhanced async status check with proper SSL handling"""
        if debug:
            print(f"\nDEBUG OpenAI: Starting async status check")
            print(f"DEBUG OpenAI: Using API URL: {self.api_url}")
            print(f"DEBUG OpenAI: API key status: {'Present' if self.api_key else 'Missing'}")
            if self.ssl_context:
                print("DEBUG OpenAI: Using custom SSL context")
            else:
                print("DEBUG OpenAI: Using default SSL context")

        if not self.api_key:
            if debug:
                print("DEBUG OpenAI: Cannot proceed without API key")
            return False

        try:
            connector = None
            if self.ssl_context:
                connector = aiohttp.TCPConnector(ssl=self.ssl_context)

            timeout = aiohttp.ClientTimeout(total=10)  # Increased timeout
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                if debug:
                    print("DEBUG OpenAI: Testing API key validity with models endpoint")
                
                async with session.get(f"{self.api_url}/models", headers=headers) as response:
                    if debug:
                        print(f"DEBUG OpenAI: Models endpoint response status: {response.status}")
                        if response.status != 200:
                            text = await response.text()
                            print(f"DEBUG OpenAI: Error response: {text}")
                    
                    return response.status == 200

        except aiohttp.ClientError as e:
            if debug:
                print(f"DEBUG OpenAI: Connection error: {str(e)}")
            return False
        except asyncio.TimeoutError:
            if debug:
                print("DEBUG OpenAI: Request timed out")
            return False
        except Exception as e:
            if debug:
                print(f"DEBUG OpenAI: Unexpected error: {str(e)}")
                import traceback
                print("DEBUG OpenAI: Full traceback:")
                traceback.print_exc()
            return False
        
    def get_available_models(self) -> List[str]:
        """Get list of available models with enhanced error handling"""
        if not self.api_key:
            return self.available_models

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                f"{self.api_url}/models",
                headers=headers,
                timeout=5.0
            )
            
            if response.status_code == 200:
                models = response.json()
                chat_models = [
                    model['id'] for model in models['data']
                    if any(preferred in model['id'] for preferred in ['gpt-4', 'gpt-3.5'])
                ]
                return chat_models if chat_models else self.available_models
            elif response.status_code == 401:
                print("OpenAI API key is invalid or expired")
                return self.available_models
            else:
                return self.available_models
                
        except requests.exceptions.RequestException:
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
        """Generate a response with proper SSL handling"""
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
            response = requests.post(
                f"{self.api_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=10,
                verify=True if not self.ssl_context else False
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return self._parse_llm_response(content)
        except requests.exceptions.RequestException as e:
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
            
            response.raise_for_status()
            response_json = response.json()
            
            # Only log essential parts of the response
            debug_response = {
                'choices': [{
                    'message': response_json['choices'][0]['message']
                }],
                'usage': response_json['usage']
            }
            print(f"DEBUG: Response (truncated): {json.dumps(debug_response, indent=2)}")
            
            content = response_json["choices"][0]["message"]["content"]
            print(f"\nDEBUG: Raw content before parsing: {content}")
            
            # Check for special characters using the base class method
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
            print("DEBUG: Full traceback:", traceback.print_exc())
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
            print(f"DEBUG: Response JSON: {json.dumps(response_json, indent=2)}")
            
            content = response_json["choices"][0]["message"]["content"]
            print("\nDEBUG: Raw content before parsing:", content)
            
            # Check for special characters using the base class method
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