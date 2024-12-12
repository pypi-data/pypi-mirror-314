#!/usr/bin/env python3
# qq.py

import sys
import argparse
import json
import os
from rich.console import Console
from rich.panel import Panel
import time
import asyncio
if sys.platform != 'win32':
    import termios
    import tty
import subprocess
from rich import box
from rich.text import Text
from rich.terminal_theme import TerminalTheme
from typing import List, Type
from pathlib import Path
from datetime import datetime
from quickquestion.llm_provider import (
    LLMProvider, 
    LMStudioProvider, 
    OllamaProvider, 
    OpenAIProvider,
    AnthropicProvider,
    GroqProvider
)
from quickquestion.settings_manager import SettingsManager, get_settings
from quickquestion.utils import getch
from quickquestion.utils import clear_screen
from quickquestion.cache import provider_cache
from quickquestion.utils import enable_debug_printing, disable_debug_printing


class QuickQuestion:
    def __init__(self, debug=False, settings=None):
        self.console = Console()
        self.debug = debug
        self.history_file = Path.home() / '.qq_history.json'
        self.settings = settings or get_settings(debug=debug)
        
        # Show immediate feedback
        if not debug:
            self.console.print("[bold blue]Initializing...[/bold blue]")
            
        # Check cache before any provider initialization
        self.providers = self._get_cached_or_new_providers()
        
        if not self.providers:
            self.console.print("[red]Error: No LLM providers available")
            self.console.print("[yellow]Please make sure either LM Studio or Ollama is running")
            sys.exit(1)
        
        # Clear the "Initializing..." message if we got here
        if not debug:
            self.console.clear()
            
        # Set the provider based on settings
        default_provider = self.settings["default_provider"]
        self.provider = next(
            (p for p in self.providers 
            if self.get_provider_name(p) == default_provider),
            self.providers[0]
        )

    def _get_cached_or_new_providers(self) -> List[LLMProvider]:
        """Get providers from cache or initialize new ones"""
        # First check the cache
        cached_providers = provider_cache.get('available_providers')
        if cached_providers is not None:
            if self.debug:
                cache_info = provider_cache.get_cache_info()
                print("\nDEBUG: Using cached providers")
                print(f"DEBUG: Cache age: {cache_info['available_providers']['age_seconds']:.1f} seconds")
                print(f"DEBUG: Cache expires in: {cache_info['available_providers']['expires_in_seconds']:.1f} seconds")
                for p in cached_providers:
                    print(f"DEBUG: Cached provider: {self.get_provider_name(p)}")
                    if hasattr(p, 'current_model'):
                        print(f"DEBUG: Provider model: {p.current_model}")
            return cached_providers
            
        if self.debug:
            print("\nDEBUG: No valid cache found, checking providers")
            
        # If no cache, do the full provider check
        providers = self._get_available_providers()
        
        # Cache the results if we found any providers
        if providers:
            if self.debug:
                print("\nDEBUG: Caching newly found providers:")
                for p in providers:
                    print(f"DEBUG: Caching provider: {self.get_provider_name(p)}")
                    if hasattr(p, 'current_model'):
                        print(f"DEBUG: Provider model: {p.current_model}")
            provider_cache.set('available_providers', providers)
            
        return providers
    
    def debug_print(self, message: str, data: any = None):
        """Print debug information if debug mode is enabled"""
        if self.debug:
            self.console.print(f"[cyan]DEBUG: {message}[/cyan]")
            if data is not None:
                if isinstance(data, (dict, list)):
                    self.console.print(Panel(
                        json.dumps(data, indent=2),
                        title="Debug Data",
                        border_style="cyan"
                    ))
                else:
                    self.console.print(Panel(
                        str(data),
                        title="Debug Data",
                        border_style="cyan"
                    ))
        
    def _get_available_providers(self) -> List[LLMProvider]:
        """Get available providers with enhanced caching"""
        if self.debug:
            print("\nDEBUG: Starting provider initialization")
            
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            providers = loop.run_until_complete(self._check_providers_async())
            loop.close()
            
            # Cache the results if we found any providers
            if providers:
                provider_cache.set('available_providers', providers)
                if self.debug:
                    print("\nDEBUG: Cached new provider configuration")
                    cache_info = provider_cache.get_cache_info()
                    print(f"DEBUG: Cache will expire in: {cache_info['available_providers']['expires_in_seconds']} seconds")
            
            return providers
            
        except Exception as e:
            if self.debug:
                print(f"\nDEBUG: Error checking providers: {str(e)}")
                import traceback
                print("DEBUG: Full traceback:")
                traceback.print_exc()
            return []
                
    def is_cloud_provider(self, provider: LLMProvider) -> bool:
        """Check if the provider is cloud-based"""
        return isinstance(provider, (OpenAIProvider, AnthropicProvider))
        
    def get_provider_name(self, provider=None) -> str:
        """Get the friendly name of the provider"""
        provider = provider or self.provider
        if isinstance(provider, OpenAIProvider):
            return "OpenAI"
        elif isinstance(provider, LMStudioProvider):
            return "LM Studio"
        elif isinstance(provider, OllamaProvider):
            return "Ollama"
        elif isinstance(provider, AnthropicProvider):
            return "Anthropic"
        elif isinstance(provider, GroqProvider):
            return "Groq"
        return "Unknown Provider"
    
    def get_provider_type_message(self) -> str:
        """Get the provider type message with appropriate color and provider name"""
        provider_name = self.get_provider_name()
        
        if self.is_cloud_provider(self.provider):
            return f"[red]-- Cloud Based Provider --[/red]\n"
        return f"[green]-- Local Provider --[/green]\n"
    
    def print_banner(self):
        # Check if configured provider is available
        default_provider = self.settings['default_provider']
        provider_available = any(self.get_provider_name(p) == default_provider for p in self.providers)
        
        # Get current provider type message
        provider_type = self.get_provider_type_message()
        
        # Create provider info with availability status
        if provider_available:
            provider_info = f"[yellow]Provider: {default_provider}[/yellow]"
        else:
            fallback_provider = self.get_provider_name()
            provider_info = f"[red]Provider: {default_provider} (Not Available) → Using: {fallback_provider}[/red]"
        
        action_info = f"[yellow]Command Action: {self.settings.get('command_action', 'Run Command')}[/yellow]"
        
        website_text = Text.assemble(
            "",  # Empty string for spacing
            ("(https://southbrucke.com)", "dim")
        )
        
        title_text = f"""[purple]Quick Question[/purple] by [bold white]Southbrucke[/bold white] - {website_text}
{provider_info}
{provider_type}{action_info}
        """
        self.console.print(Panel(title_text, box=box.ROUNDED, style="white", expand=False))
        print()

    def load_history(self) -> List[dict]:
        """Load command history from file"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_to_history(self, command: str, question: str):
        """Save command to history with timestamp and question"""
        history = self.load_history()
        history.append({
            'timestamp': datetime.now().isoformat(),
            'command': command,
            'question': question
        })
        # Keep only last 100 commands
        history = history[-100:]
        
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)

    def display_history(self):
        """Display command history with interactive selection"""
        history = self.load_history()
        if not history:
            self.console.print("[yellow]No command history found[/yellow]")
            return

        selected = 0
        # Get last 10 entries in reverse order
        entries = list(reversed(history[-10:]))
        
        def render_screen():
            if not self.debug:  # Only clear screen if not in debug mode
                clear_screen()
            self.print_banner()
            self.console.print("[bold]Command History:[/bold]\n")
            
            # Show instructions
            self.console.print("\n[dim]↑/↓ to select, Enter to execute, [/dim][red]q[/red][dim] to cancel[/dim]\n")
            
            # Display each history entry
            for i, entry in enumerate(entries):
                timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M')
                style = "bold white on blue" if i == selected else "blue"
                self.console.print(
                    Panel(
                        f"[dim]{timestamp}[/dim]\nQ: {entry['question']}\n[green]$ {entry['command']}[/green]",
                        title=f"Entry {i+1}",
                        border_style=style
                    )
                )
            
            # Add cancel option
            cancel_style = "bold white on red" if selected == len(entries) else "red"
            self.console.print(Panel("Cancel", title="Exit", border_style=cancel_style))

        while True:
            render_screen()
            
            c = self.getch()
            
            if self.debug:
                print(f"\nDEBUG UI - Received key: {repr(c)}")

            # Simple arrow key handling
            if c == '\x1b[A':  # Up arrow
                if self.debug:
                    print(f"DEBUG UI - Up arrow - Current selection: {selected}")
                if selected > 0:
                    selected -= 1
                    if self.debug:
                        print(f"DEBUG UI - New selection: {selected}")

            elif c == '\x1b[B':  # Down arrow
                if self.debug:
                    print(f"DEBUG UI - Down arrow - Current selection: {selected}")
                if selected < len(entries):
                    selected += 1
                    if self.debug:
                        print(f"DEBUG UI - New selection: {selected}")
            
            elif c == '\r':  # Enter key
                if selected == len(entries):  # If cancel is selected
                    clear_screen()
                    sys.exit(0)
                else:
                    clear_screen()
                    self.print_banner()
                    selected_entry = entries[selected]
                    command = selected_entry['command']
                    self.console.print(f"\n[green]Executing command:[/green] {command}")
                    # Don't add to history again since it's already there
                    subprocess.run(command, shell=True)
                    break
            
            elif c == 'q':  # Quick exit
                clear_screen()
                sys.exit(0)

    def display_help(self):
        """Display help information"""
        clear_screen()
        self.print_banner()
        
        help_text = """[bold white]Usage:[/bold white]
        qq "your question here"    Ask for command suggestions
        qq --history              Show command history
        qq --settings            Configure application settings
        qq --debug               Enable debug mode

    [bold white]Examples:[/bold white]
        qq "how to find files containing text"
        qq "show running processes"
        qq "check disk space"

    [bold white]Navigation:[/bold white]
        ↑/↓ arrows               Select options
        Enter                    Execute/Select
        q                        Quit/Cancel

    [bold white]Current Configuration:[/bold white]
        Provider: [green]{provider}[/green]
        Action: [green]{action}[/green]
        Model: [green]{model}[/green]

    For more information, visit: [blue]https://southbrucke.com[/blue]
    """.format(
            provider=self.get_provider_name(),
            action=self.settings.get('command_action', 'Run Command'),
            model=self.provider.get_model_info() or 'Not Set'
        )

        self.console.print(Panel(
            help_text,
            title="Quick Question Help",
            border_style="blue",
            expand=False
        ))

    def generate_prompt(self, question: str) -> str:
        os_type = "Windows" if sys.platform == "win32" else "macOS"
        return f"""You are a helpful command-line expert. Provide exactly 3 different command-line solutions for the following question: {question}

    Rules:
    1. Provide exactly 3 command options
    2. Each command must be a single line
    3. Do not provide explanations
    4. Format the response as a JSON array with 3 strings
    5. Focus on {os_type} terminal commands
    6. Keep commands concise and practical

    Example response format:
    ["command1", "command2", "command3"]"""

    def get_command_suggestions(self, question: str) -> List[str]:
        clear_screen()
        self.print_banner()
        
        current_model = self.provider.get_model_info()
        if current_model:
            self.console.print(f"[green]Using model: {current_model}")
            
        try:
            prompt = self.generate_prompt(question)
            self.debug_print("Generated prompt:", prompt)
            
            # Create and start the spinner
            with self.console.status(
                "[bold blue]Thinking...[/bold blue]",
                spinner="dots",
                spinner_style="blue"
            ):
                raw_response = self.provider.generate_response_with_debug(prompt) if self.debug else self.provider.generate_response(prompt)
                
                if self.debug:
                    self.debug_print("Raw LLM response:", raw_response)
                    
                return raw_response
                
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}")
            if self.debug:
                import traceback
                self.debug_print("Full traceback:", traceback.format_exc())
            self.console.print("[yellow]Please make sure your LLM provider is running and configured correctly.")
            sys.exit(1)

    def getch(self):
        return getch(debug=self.debug)

    async def _check_providers_async(self) -> List[LLMProvider]:
        """Async provider checking with enhanced debugging"""
        available_providers = []
        default_model = self.settings.get('default_model')
        
        if self.debug:
            print("\nDEBUG: Starting async provider checks")
            print(f"DEBUG: Default model from settings: {default_model}")
        
        # Check cache first
        cached_providers = provider_cache.get('available_providers')
        if cached_providers is not None:
            if self.debug:
                print("DEBUG: Using cached providers")
                for p in cached_providers:
                    print(f"DEBUG: Cached provider: {self.get_provider_name(p)}")
            return cached_providers

        # Create all provider instances
        providers = [
            LMStudioProvider(),
            OllamaProvider(),
            OpenAIProvider(),
            AnthropicProvider(),
            GroqProvider()
        ]

        if self.debug:
            print("\nDEBUG: Created provider instances")
            for p in providers:
                print(f"DEBUG: Initialized {p.__class__.__name__}")

        # Check all providers concurrently
        async def check_provider(provider):
            if self.debug:
                print(f"\nDEBUG: Checking {provider.__class__.__name__}")
            
            if await provider.async_check_status(debug=self.debug):
                if self.debug:
                    print(f"DEBUG: {provider.__class__.__name__} is available")
                
                if default_model and self.get_provider_name(provider) == self.settings['default_provider']:
                    provider.current_model = default_model
                    if self.debug:
                        print(f"DEBUG: Set default model to {default_model}")
                return provider
                
            if self.debug:
                print(f"DEBUG: {provider.__class__.__name__} is not available")
            return None

        if self.debug:
            print("\nDEBUG: Starting concurrent provider checks")

        # Run all checks concurrently
        tasks = [check_provider(p) for p in providers]
        results = await asyncio.gather(*tasks)
        
        if self.debug:
            print("\nDEBUG: Completed concurrent provider checks")
        
        # Filter out None results
        available_providers = [p for p in results if p is not None]
        
        if self.debug:
            print(f"\nDEBUG: Found {len(available_providers)} available providers:")
            for p in available_providers:
                print(f"DEBUG: - {self.get_provider_name(p)}")
        
        # Cache the results
        provider_cache.set('available_providers', available_providers)
        
        if self.debug:
            print("\nDEBUG: Cached available providers")
            if not available_providers:
                print("\nDEBUG: No providers available")
                print("DEBUG: Please ensure either LM Studio or Ollama is running")
                print("DEBUG: LM Studio should be running on http://localhost:1234")
                print("DEBUG: Ollama should be running on http://localhost:11434")
        
        return available_providers

    def _get_available_providers(self) -> List[LLMProvider]:
        """Sync wrapper for async provider checking"""
        try:
            if self.debug:
                print("\nDEBUG: Setting up async loop for provider checks")
                
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            if self.debug:
                print("DEBUG: Created new event loop")
                
            providers = loop.run_until_complete(self._check_providers_async())
            
            if self.debug:
                print("DEBUG: Completed async provider checks")
                
            loop.close()
            
            if self.debug:
                print("DEBUG: Closed event loop")
                
            return providers
        except Exception as e:
            if self.debug:
                print(f"\nDEBUG: Error checking providers: {str(e)}")
                import traceback
                print("DEBUG: Full traceback:")
                traceback.print_exc()
            return []

    def display_suggestions(self, suggestions: List[str], question: str):
        selected = 0
        
        def render_screen():
            if not self.debug:  # Only clear screen if not in debug mode
                clear_screen()
            self.print_banner()
            current_model = self.provider.get_model_info()
            if current_model:
                self.console.print(f"[green]Using model: {current_model}")
            
            # Show action type in instructions
            action_type = self.settings.get('command_action', 'Run Command')
            self.console.print(f"\n[dim]↑/↓ to select, Enter to {action_type.lower()}, [/dim][red]q[/red][dim] to cancel[/dim]\n")
            
            # First show all command options
            for i, cmd in enumerate(suggestions):
                style = "bold white on blue" if i == selected else "blue"
                self.console.print(Panel(cmd, title=f"Option {i+1}", border_style=style))
            
            # Add cancel option at the bottom
            cancel_style = "bold white on red" if selected == len(suggestions) else "red"
            self.console.print(Panel("Cancel", title="Exit", border_style=cancel_style))

        while True:
            render_screen()
            
            c = self.getch()
            
            if self.debug:
                print(f"\nDEBUG UI - Received key: {repr(c)}")

            # Simple arrow key handling
            if c == '\x1b[A':  # Up arrow
                if self.debug:
                    print(f"DEBUG UI - Up arrow - Current selection: {selected}")
                if selected > 0:
                    selected -= 1
                    if self.debug:
                        print(f"DEBUG UI - New selection: {selected}")

            elif c == '\x1b[B':  # Down arrow
                if self.debug:
                    print(f"DEBUG UI - Down arrow - Current selection: {selected}")
                if selected < len(suggestions):
                    selected += 1
                    if self.debug:
                        print(f"DEBUG UI - New selection: {selected}")
            
            elif c == '\r':  # Enter key
                if selected == len(suggestions):  # If cancel is selected
                    clear_screen()
                    sys.exit(0)
                else:
                    clear_screen()
                    self.print_banner()
                    selected_command = suggestions[selected]
                    
                    # Check command action setting
                    if self.settings.get('command_action') == 'Copy Command':
                        try:
                            copy_to_clipboard(selected_command)
                            self.console.print(f"\n[green]Command copied to clipboard:[/green] {selected_command}")
                            # Save to history before exiting
                            self.save_to_history(selected_command, question)
                            time.sleep(1)  # Brief pause to show the message
                            sys.exit(0)
                        except Exception as e:
                            self.console.print(f"\n[red]Error: {str(e)}")
                            sys.exit(1)
                    else:
                        self.console.print(f"\n[green]Executing command:[/green] {selected_command}")
                        # Save to history before executing
                        self.save_to_history(selected_command, question)
                        subprocess.run(selected_command, shell=True)
                        break
            
            elif c == 'q':  # Quick exit
                clear_screen()
                sys.exit(0)
    
def copy_to_clipboard(text: str):
    """Cross-platform clipboard copy"""
    try:
        import pyperclip
        pyperclip.copy(text)
    except ImportError:
        if sys.platform == 'darwin':
            subprocess.run('pbcopy', input=text.encode(), env={'LANG': 'en_US.UTF-8'})
        elif sys.platform == 'win32':
            import win32clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text)
            win32clipboard.CloseClipboard()


def main():
    parser = argparse.ArgumentParser(description="Quick Question - Command Line Suggestions")
    parser.add_argument("question", nargs="*", help="Your command-line question")
    parser.add_argument("--settings", action="store_true", help="Open settings menu")
    parser.add_argument("--history", action="store_true", help="Show command history")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--clear-cache", action="store_true", help="Clear the provider cache")
    
    args = parser.parse_args()
    
    if args.debug:
        enable_debug_printing()
    
    if args.clear_cache:
        provider_cache.clear()
        print("Cache cleared successfully")
        return
    
    if not args.debug:
        print("Loading Quick Question...")
    
    # Only clear cache when entering settings
    should_clear_cache = args.settings
    
    if args.settings:
        SettingsManager(debug=args.debug, clear_cache=True).display_settings_ui()
        return
    
    # Pass clear_cache=False for normal operation
    settings_manager = SettingsManager(debug=args.debug, clear_cache=False)
    settings = settings_manager.load_settings()
    
    qq = QuickQuestion(debug=args.debug, settings=settings)
    
    try:
        if args.history:
            qq.display_history()
            return
            
        if not args.question:
            # Show help if no arguments provided
            qq.display_help()
        else:
            question = " ".join(args.question)
            suggestions = qq.get_command_suggestions(question)
            qq.display_suggestions(suggestions, question)
    finally:
        if args.debug:
            disable_debug_printing()

if __name__ == "__main__":
    main()