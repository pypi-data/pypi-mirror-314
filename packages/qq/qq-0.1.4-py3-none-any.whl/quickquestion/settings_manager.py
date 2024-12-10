import json
from pathlib import Path
from typing import Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich import box
import termios
import tty
import sys
import os
from quickquestion.llm_provider import (
    LLMProvider, 
    LMStudioProvider, 
    OllamaProvider, 
    OpenAIProvider,
    AnthropicProvider,
    GroqProvider
)

class SettingsManager:
    def __init__(self):
        self.console = Console()
        self.settings_file = Path.home() / '.qq_settings.json'
        self.default_settings = {
            "default_provider": "LM Studio",
            "provider_options": ["LM Studio", "Ollama", "OpenAI", "Anthropic", "Groq"],
            "command_action": "Run Command",
            "command_action_options": ["Run Command", "Copy Command"],
            "default_model": None,  # Will be set based on provider
            "available_models": []  # Will be populated based on provider
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

    def getch(self) -> str:
        """Get a single character from the terminal"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    
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
            os.system('clear')
            
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
            
            if is_editing_provider:
                if c == '\x1b':  # Arrow keys
                    next1, next2 = self.getch(), self.getch()
                    if next1 == '[':
                        if next2 == 'D' and selected_provider_index > 0:  # Left arrow
                            selected_provider_index -= 1
                        elif next2 == 'C' and selected_provider_index < len(settings["provider_options"]) - 1:  # Right arrow
                            selected_provider_index += 1
                elif c == '\r':  # Enter
                    new_provider = settings["provider_options"][selected_provider_index]
                    if new_provider != settings["default_provider"]:
                        settings["default_provider"] = new_provider
                        # Update available models for new provider
                        self.update_available_models(settings, new_provider)
                        selected_model_index = 0  # Reset model selection
                    is_editing_provider = False
                elif c == 'q':
                    is_editing_provider = False
            elif is_editing_model:
                if settings["available_models"]:
                    if c == '\x1b':  # Arrow keys
                        next1, next2 = self.getch(), self.getch()
                        if next1 == '[':
                            if next2 == 'D' and selected_model_index > 0:  # Left arrow
                                selected_model_index -= 1
                            elif next2 == 'C' and selected_model_index < len(settings["available_models"]) - 1:  # Right arrow
                                selected_model_index += 1
                    elif c == '\r':  # Enter
                        settings["default_model"] = settings["available_models"][selected_model_index]
                        is_editing_model = False
                    elif c == 'q':
                        is_editing_model = False
            elif is_editing_action:
                if c == '\x1b':  # Arrow keys
                    next1, next2 = self.getch(), self.getch()
                    if next1 == '[':
                        if next2 == 'D' and selected_action_index > 0:  # Left arrow
                            selected_action_index -= 1
                        elif next2 == 'C' and selected_action_index < len(settings["command_action_options"]) - 1:  # Right arrow
                            selected_action_index += 1
                elif c == '\r':  # Enter
                    settings["command_action"] = settings["command_action_options"][selected_action_index]
                    is_editing_action = False
                elif c == 'q':
                    is_editing_action = False
            else:
                if c == '\x1b':  # Arrow keys
                    next1, next2 = self.getch(), self.getch()
                    if next1 == '[':
                        if next2 == 'A' and selected_option > 0:  # Up arrow
                            selected_option -= 1
                        elif next2 == 'B' and selected_option < 4:  # Down arrow
                            selected_option += 1
                elif c == '\r':  # Enter
                    if selected_option == 0:
                        is_editing_provider = True
                    elif selected_option == 1:
                        if settings["available_models"]:
                            is_editing_model = True
                    elif selected_option == 2:
                        is_editing_action = True
                    elif selected_option == 3:  # Save
                        self.save_settings(settings)
                        os.system('clear')
                        self.console.print("[green]Settings saved successfully![/green]")
                        return
                    elif selected_option == 4:  # Cancel
                        os.system('clear')
                        return
                elif c == 'q':
                    os.system('clear')
                    return

def get_settings() -> Dict[str, Any]:
    """Helper function to get current settings"""
    return SettingsManager().load_settings()