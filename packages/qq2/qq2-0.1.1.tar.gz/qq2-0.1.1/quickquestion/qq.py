#!/usr/bin/env python3
# qq.py

import sys
import argparse
import json
import os
from rich.console import Console
from rich.panel import Panel
import time
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

class QuickQuestion:
    def __init__(self):
        self.console = Console()
        self.history_file = Path.home() / '.qq_history.json'
        self.settings = get_settings()
        self.providers = self._get_available_providers()
        if not self.providers:
            self.console.print("[red]Error: No LLM providers available")
            self.console.print("[yellow]Please make sure either LM Studio or Ollama is running")
            sys.exit(1)
        # Set the provider based on settings
        default_provider = self.settings["default_provider"]
        self.provider = next(
            (p for p in self.providers 
            if self.get_provider_name(p) == default_provider),
            self.providers[0]
        )
        
    def _get_available_providers(self) -> List[LLMProvider]:
        available_providers = []
        default_model = self.settings.get('default_model')
        
        # Try LM Studio first
        lmstudio = LMStudioProvider()
        if lmstudio.check_status():
            if default_model and self.settings['default_provider'] == "LM Studio":
                lmstudio.current_model = default_model
            available_providers.append(lmstudio)
        
        # Then try Ollama
        ollama = OllamaProvider()
        if ollama.check_status():
            if default_model and self.settings['default_provider'] == "Ollama":
                ollama.current_model = default_model
            available_providers.append(ollama)

        # Then try OpenAI
        openai = OpenAIProvider()
        if openai.check_status():
            if default_model and self.settings['default_provider'] == "OpenAI":
                openai.current_model = default_model
            available_providers.append(openai)

        # Then try Anthropic
        anthropic = AnthropicProvider()
        if anthropic.check_status():
            if default_model and self.settings['default_provider'] == "Anthropic":
                anthropic.current_model = default_model
            available_providers.append(anthropic)
            
        # Then try Groq
        groq = GroqProvider()
        if groq.check_status():
            if default_model and self.settings['default_provider'] == "Groq":
                groq.current_model = default_model
            available_providers.append(groq)
            
        return available_providers

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
            os.system('clear')
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
            
            if c == '\x1b':  # Arrow keys
                next1, next2 = self.getch(), self.getch()
                if next1 == '[':
                    if next2 == 'A':  # Up arrow
                        if selected > 0:
                            selected -= 1
                    elif next2 == 'B':  # Down arrow
                        if selected < len(entries):  # Include cancel option
                            selected += 1
            
            elif c == '\r':  # Enter key
                if selected == len(entries):  # If cancel is selected
                    os.system('clear')
                    sys.exit(0)
                else:
                    os.system('clear')
                    self.print_banner()
                    selected_entry = entries[selected]
                    command = selected_entry['command']
                    self.console.print(f"\n[green]Executing command:[/green] {command}")
                    # Don't add to history again since it's already there
                    subprocess.run(command, shell=True)
                    break
            
            elif c == 'q':  # Quick exit
                os.system('clear')
                sys.exit(0)

    def generate_prompt(self, question: str) -> str:
        return f"""You are a helpful command-line expert. Provide exactly 3 different command-line solutions for the following question: {question}

Rules:
1. Provide exactly 3 command options
2. Each command must be a single line
3. Do not provide explanations
4. Format the response as a JSON array with 3 strings
5. Focus on macOS terminal commands
6. Keep commands concise and practical

Example response format:
["command1", "command2", "command3"]"""

    def get_command_suggestions(self, question: str) -> List[str]:
        os.system('clear')
        self.print_banner()
        
        current_model = self.provider.get_model_info()
        if current_model:
            self.console.print(f"[green]Using model: {current_model}")
            
        try:
            # Create and start the spinner
            with self.console.status(
                "[bold blue]Thinking...[/bold blue]",
                spinner="dots",
                spinner_style="blue"
            ):
                return self.provider.generate_response(self.generate_prompt(question))
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}")
            self.console.print("[yellow]Please make sure your LLM provider is running and configured correctly.")
            sys.exit(1)

    def getch(self):
        """Get a single character from the terminal"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def display_suggestions(self, suggestions: List[str], question: str):
        selected = 0
        
        def render_screen():
            os.system('clear')
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
            
            if c == '\x1b':  # Arrow keys
                next1, next2 = self.getch(), self.getch()
                if next1 == '[':
                    if next2 == 'A':  # Up arrow
                        if selected > 0:
                            selected -= 1
                    elif next2 == 'B':  # Down arrow
                        if selected < len(suggestions):  # Now include the cancel option
                            selected += 1
            
            elif c == '\r':  # Enter key
                if selected == len(suggestions):  # If cancel is selected
                    os.system('clear')
                    sys.exit(0)
                else:
                    os.system('clear')
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
                os.system('clear')
                sys.exit(0)
    
def copy_to_clipboard(text: str):
    """Copy text to clipboard using pbcopy (macOS)"""
    try:
        process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(text.encode('utf-8'))
    except Exception as e:
        raise Exception(f"Failed to copy to clipboard: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="Quick Question - Command Line Suggestions")
    parser.add_argument("question", nargs="*", help="Your command-line question")
    parser.add_argument("--settings", action="store_true", help="Open settings menu")
    
    args = parser.parse_args()
    
    if args.settings:
        SettingsManager().display_settings_ui()
        return
        
    qq = QuickQuestion()
    
    if not args.question:
        # If no question provided, show history
        qq.display_history()
    else:
        question = " ".join(args.question)
        suggestions = qq.get_command_suggestions(question)
        qq.display_suggestions(suggestions, question)

if __name__ == "__main__":
    main()