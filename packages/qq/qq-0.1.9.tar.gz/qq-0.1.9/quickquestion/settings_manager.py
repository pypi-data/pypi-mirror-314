import sys
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich import box
if sys.platform != 'win32':
    import termios
    import tty
from quickquestion.llm_provider import (
    LLMProvider, 
    LMStudioProvider, 
    OllamaProvider, 
    OpenAIProvider,
    AnthropicProvider,
    GroqProvider
)
from quickquestion.utils import getch

class SettingsManager:
    def __init__(self, debug=False):
        self.console = Console()
        self.settings_file = Path.home() / '.qq_settings.json'
        self.debug = debug
        self.default_settings = {
            "default_provider": "LM Studio",
            "provider_options": ["LM Studio", "Ollama", "OpenAI", "Anthropic", "Groq"],
            "command_action": "Run Command",
            "command_action_options": ["Run Command", "Copy Command"],
            "default_model": None,
            "available_models": []
        }
        
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file or return defaults if no file exists"""
        settings = self.default_settings.copy()
        
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    saved_settings = json.load(f)
                    
                # Check if there are new provider options to add
                if "provider_options" in saved_settings:
                    new_providers = [p for p in self.default_settings["provider_options"] 
                                if p not in saved_settings["provider_options"]]
                    if new_providers:
                        saved_settings["provider_options"].extend(new_providers)
                        # Save the updated settings back to file
                        with open(self.settings_file, 'w') as f:
                            json.dump(saved_settings, f, indent=2)
                
                # Update the default settings with saved values
                settings.update(saved_settings)
                
            except json.JSONDecodeError:
                return self.default_settings
                
        return settings

    def save_settings(self, settings: Dict[str, Any]):
        """Save settings to file"""
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f, indent=2)

    def getch(self):
        return getch(debug=self.debug)

    def get_provider_instance(self, provider_name: str) -> Optional[LLMProvider]:
        """Create a provider instance based on name"""
        provider_map = {
            "LM Studio": LMStudioProvider,
            "Ollama": OllamaProvider,
            "OpenAI": OpenAIProvider,
            "Anthropic": AnthropicProvider,
            "Groq": GroqProvider
        }
        provider_class = provider_map.get(provider_name)
        if provider_class:
            return provider_class()
        return None
    
    def update_available_models(self, settings: dict, provider_name: str):
        """Update available models list for the selected provider"""
        provider = self.get_provider_instance(provider_name)
        if provider and provider.check_status():
            models = provider.get_available_models()
            settings["available_models"] = models
            # If no default model is set or current default isn't in available models,
            # select the best model
            if not settings["default_model"] or settings["default_model"] not in models:
                settings["default_model"] = provider.select_best_model(models)
        else:
            settings["available_models"] = []
            settings["default_model"] = None

    def display_settings_ui(self):
        """Display interactive settings UI"""
        settings = self.load_settings()
        selected_option = 0
        selected_provider_index = settings["provider_options"].index(settings["default_provider"])
        selected_action_index = settings["command_action_options"].index(settings["command_action"])
        selected_model_index = 0
        
        # Update models for current provider
        self.update_available_models(settings, settings["default_provider"])
        if settings["default_model"] and settings["default_model"] in settings["available_models"]:
            selected_model_index = settings["available_models"].index(settings["default_model"])
        
        is_editing_provider = False
        is_editing_action = False
        is_editing_model = False

        def render_screen():
            if not self.debug:  # Only clear screen if not in debug mode
                os.system('cls' if sys.platform == 'win32' else 'clear')
            
            # Title
            self.console.print(Panel(
                "[purple]Quick Question Settings[/purple]",
                box=box.ROUNDED,
                style="white",
                expand=False
            ))
            print()
            
            # Instructions
            if any([is_editing_provider, is_editing_action, is_editing_model]):
                self.console.print("\n[dim]←/→ to select, Enter to confirm, [/dim][red]q[/red][dim] to cancel[/dim]\n")
            else:
                self.console.print("\n[dim]↑/↓ to navigate, Enter to edit/save, [/dim][red]q[/red][dim] to exit[/dim]\n")
            
            # Default Provider Setting
            provider_style = "bold white on blue" if selected_option == 0 else "blue"
            provider_panel_content = (
                f"Current: [green]{settings['default_provider']}[/green]\n"
                "Available: " + ", ".join(
                    f"[{'white on cyan' if is_editing_provider and i == selected_provider_index else 'white'}]{p}[/]"
                    for i, p in enumerate(settings["provider_options"])
                )
            )
            self.console.print(Panel(
                provider_panel_content,
                title="Default LLM Provider",
                border_style=provider_style
            ))
            
            # Default Model Setting
            model_style = "bold white on blue" if selected_option == 1 else "blue"
            model_panel_content = (
                f"Current: [green]{settings.get('default_model', 'Not Set')}[/green]\n"
            )
            if settings["available_models"]:
                model_panel_content += "Available: " + ", ".join(
                    f"[{'white on cyan' if is_editing_model and i == selected_model_index else 'white'}]{m}[/]"
                    for i, m in enumerate(settings["available_models"])
                )
            else:
                model_panel_content += "[red]No models available for selected provider[/red]"
            
            self.console.print(Panel(
                model_panel_content,
                title="Default Model",
                border_style=model_style
            ))
            
            # Command Action Setting
            action_style = "bold white on blue" if selected_option == 2 else "blue"
            action_panel_content = (
                f"Current: [green]{settings['command_action']}[/green]\n"
                "Available: " + ", ".join(
                    f"[{'white on cyan' if is_editing_action and i == selected_action_index else 'white'}]{a}[/]"
                    for i, a in enumerate(settings["command_action_options"])
                )
            )
            self.console.print(Panel(
                action_panel_content,
                title="Command Action",
                border_style=action_style
            ))
            
            # Save/Cancel Options
            save_style = "bold white on blue" if selected_option == 3 else "blue"
            cancel_style = "bold white on blue" if selected_option == 4 else "blue"
            
            self.console.print(Panel("Save Changes", title="Save", border_style=save_style))
            self.console.print(Panel("Exit Without Saving", title="Cancel", border_style=cancel_style))

        while True:
            render_screen()
            c = self.getch()
            
            if self.debug:
                print(f"\nDEBUG UI - Received key: {repr(c)}")

            # Simple arrow key handling
            if c == '\x1b[A':  # Up arrow
                if self.debug:
                    print(f"DEBUG UI - Up arrow - Current option: {selected_option}")
                if not is_editing_provider and not is_editing_action and not is_editing_model:
                    if selected_option > 0:
                        selected_option -= 1
                        if self.debug:
                            print(f"DEBUG UI - New option: {selected_option}")

            elif c == '\x1b[B':  # Down arrow
                if self.debug:
                    print(f"DEBUG UI - Down arrow - Current option: {selected_option}")
                if not is_editing_provider and not is_editing_action and not is_editing_model:
                    if selected_option < 4:
                        selected_option += 1
                        if self.debug:
                            print(f"DEBUG UI - New option: {selected_option}")

            elif c == '\x1b[C':  # Right arrow
                if is_editing_provider and selected_provider_index < len(settings["provider_options"]) - 1:
                    selected_provider_index += 1
                elif is_editing_action and selected_action_index < len(settings["command_action_options"]) - 1:
                    selected_action_index += 1
                elif is_editing_model and settings["available_models"] and selected_model_index < len(settings["available_models"]) - 1:
                    selected_model_index += 1

            elif c == '\x1b[D':  # Left arrow
                if is_editing_provider and selected_provider_index > 0:
                    selected_provider_index -= 1
                elif is_editing_action and selected_action_index > 0:
                    selected_action_index -= 1
                elif is_editing_model and settings["available_models"] and selected_model_index > 0:
                    selected_model_index -= 1

            elif c == '\r':  # Enter
                if is_editing_provider:
                    new_provider = settings["provider_options"][selected_provider_index]
                    if new_provider != settings["default_provider"]:
                        settings["default_provider"] = new_provider
                        self.update_available_models(settings, new_provider)
                        selected_model_index = 0
                    is_editing_provider = False
                elif is_editing_model and settings["available_models"]:
                    settings["default_model"] = settings["available_models"][selected_model_index]
                    is_editing_model = False
                elif is_editing_action:
                    settings["command_action"] = settings["command_action_options"][selected_action_index]
                    is_editing_action = False
                else:
                    if selected_option == 0:
                        is_editing_provider = True
                    elif selected_option == 1 and settings["available_models"]:
                        is_editing_model = True
                    elif selected_option == 2:
                        is_editing_action = True
                    elif selected_option == 3:  # Save
                        self.save_settings(settings)
                        os.system('cls' if sys.platform == 'win32' else 'clear')
                        self.console.print("[green]Settings saved successfully![/green]")
                        return
                    elif selected_option == 4:  # Cancel
                        os.system('cls' if sys.platform == 'win32' else 'clear')
                        return

            elif c == 'q':  # Quick exit
                os.system('cls' if sys.platform == 'win32' else 'clear')
                return
            
def get_settings(debug=False):
    """Helper function to get current settings"""
    return SettingsManager(debug=debug).load_settings()