"""CLI interface for prompt-bench."""

import json
import os
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from . import __version__
from .core import (
    BenchmarkResult,
    calculate_summary,
    display_results_table,
    display_summary,
    load_config,
    run_benchmark,
    save_results_json,
)

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="prompt-bench")
def cli():
    """Benchmark and compare LLM prompts across different providers."""
    pass


@cli.command()
@click.option(
    "--provider", "-p",
    type=click.Choice(["openai", "anthropic", "all"]),
    default="all",
    help="LLM provider to use (default: all)",
)
@click.option(
    "--model", "-m",
    default=None,
    help="Specific model to use (overrides provider defaults)",
)
@click.option(
    "--prompt", "-P",
    default=None,
    help="Prompt to test (or use --file)",
)
@click.option(
    "--file", "-f",
    "prompt_file",
    default=None,
    help="File containing the prompt",
)
@click.option(
    "--system-prompt", "-s",
    default=None,
    help="System prompt to use",
)
@click.option(
    "--output", "-o",
    default=None,
    help="Output JSON file path",
)
@click.option(
    "--runs", "-n",
    default=1,
    help="Number of runs per configuration (default: 1)",
)
def run(
    provider: str,
    model: str,
    prompt: str,
    prompt_file: str,
    system_prompt: str,
    output: str,
    runs: int,
):
    """Run benchmark with specified parameters.

    Examples:

        prompt-bench run --prompt "What is 2+2?"

        prompt-bench run --file prompt.txt --provider openai

        prompt-bench run --prompt "Explain AI" --runs 3
    """
    # Get prompt
    if prompt_file:
        with open(prompt_file, "r") as f:
            prompt = f.read()
    elif prompt:
        pass
    else:
        console.print("[red]Error: Provide --prompt or --file[/red]")
        sys.exit(1)

    # Define provider configurations
    provider_configs = {
        "openai": {"provider": "openai", "model": model or "gpt-4o-mini"},
        "anthropic": {"provider": "anthropic", "model": model or "claude-3-5-sonnet-20241022"},
    }

    # Select providers
    if provider == "all":
        providers_to_test = list(provider_configs.values())
    else:
        providers_to_test = [provider_configs[provider]]

    # Run benchmarks
    results = []
    console.print(f"\n[bold blue]Running benchmark ({runs} runs per config)[/bold blue]\n")

    for config in providers_to_test:
        for run_num in range(runs):
            with console.status(f"[bold green]Testing {config['provider']}/{config['model']} (run {run_num + 1}/{runs})..."):
                result = run_benchmark(
                    provider=config["provider"],
                    model=config["model"],
                    prompt=prompt,
                    system_prompt=system_prompt,
                )
                results.append(result)

    # Display results
    console.print()
    display_results_table(results)
    console.print()
    display_summary(calculate_summary(results))

    # Save results
    if output:
        save_results_json(results, output)


@cli.command()
@click.argument("config_file")
@click.option(
    "--output", "-o",
    default=None,
    help="Output JSON file path",
)
def bench(config_file: str, output: str):
    """Run benchmark from YAML configuration file.

    Examples:

        prompt-bench bench config.yaml

        prompt-bench bench config.yaml --output results.json
    """
    # Load config
    try:
        config = load_config(config_file)
    except Exception as e:
        console.print(f"[red]Error loading config: {e}[/red]")
        sys.exit(1)

    # Extract config
    prompts = config.get("prompts", [])
    providers = config.get("providers", [])
    system_prompt = config.get("system_prompt")
    runs = config.get("runs", 1)

    if not prompts:
        console.print("[red]Error: No prompts defined in config[/red]")
        sys.exit(1)

    if not providers:
        console.print("[red]Error: No providers defined in config[/red]")
        sys.exit(1)

    # Run benchmarks
    results = []
    console.print(f"\n[bold blue]Running benchmark from config: {config_file}[/bold blue]\n")

    for prompt_config in prompts:
        prompt_text = prompt_config.get("text", "")
        prompt_name = prompt_config.get("name", "unnamed")

        console.print(f"[bold cyan]Prompt: {prompt_name}[/bold cyan]")

        for provider_config in providers:
            provider = provider_config.get("provider")
            model = provider_config.get("model")

            for run_num in range(runs):
                with console.status(f"[bold green]Testing {provider}/{model} (run {run_num + 1}/{runs})..."):
                    result = run_benchmark(
                        provider=provider,
                        model=model,
                        prompt=prompt_text,
                        system_prompt=system_prompt,
                    )
                    results.append(result)

    # Display results
    console.print()
    display_results_table(results)
    console.print()
    display_summary(calculate_summary(results))

    # Save results
    if output:
        save_results_json(results, output)


@cli.command()
def providers():
    """List available providers and models."""
    table = Table(title="🔌 Available Providers", border_style="blue")
    table.add_column("Provider", style="bold")
    table.add_column("Default Model")
    table.add_column("API Key Env Var")

    table.add_row("openai", "gpt-4o-mini", "OPENAI_API_KEY")
    table.add_row("anthropic", "claude-3-5-sonnet-20241022", "ANTHROPIC_API_KEY")

    console.print(table)

    console.print("\n[bold]Supported Models:[/bold]")
    console.print("  OpenAI: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo")
    console.print("  Anthropic: claude-3-5-sonnet-20241022, claude-3-opus-20240229, claude-3-haiku-20240307")


@cli.command()
def example():
    """Show example configuration file."""
    example_config = """# Example benchmark configuration

# System prompt (optional)
system_prompt: "You are a helpful assistant."

# Prompts to test
prompts:
  - name: "Math"
    text: "What is 2 + 2?"
  - name: "Code"
    text: "Write a Python function to calculate factorial"
  - name: "Explanation"
    text: "Explain quantum computing in simple terms"

# Providers to test
providers:
  - provider: openai
    model: gpt-4o-mini
  - provider: openai
    model: gpt-4o
  - provider: anthropic
    model: claude-3-5-sonnet-20241022

# Number of runs per configuration
runs: 3
"""
    syntax = Syntax(example_config, "yaml", theme="monokai")
    console.print(Panel(syntax, title="Example Config", border_style="green"))


if __name__ == "__main__":
    cli()
