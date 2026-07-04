"""Core functionality for benchmarking LLM prompts."""

import os
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.table import Table

console = Console()


@dataclass
class BenchmarkResult:
    """Result of a single benchmark run."""
    provider: str
    model: str
    prompt: str
    response: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    latency_ms: float
    success: bool
    error: Optional[str] = None


@dataclass
class BenchmarkSummary:
    """Summary of multiple benchmark runs."""
    results: List[BenchmarkResult] = field(default_factory=list)
    total_runs: int = 0
    successful_runs: int = 0
    failed_runs: int = 0
    avg_latency_ms: float = 0.0
    total_tokens: int = 0


def run_openai_benchmark(
    prompt: str,
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
    system_prompt: Optional[str] = None,
) -> BenchmarkResult:
    """Run benchmark using OpenAI API."""
    from openai import OpenAI

    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return BenchmarkResult(
            provider="openai",
            model=model,
            prompt=prompt,
            response="",
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
            latency_ms=0,
            success=False,
            error="OPENAI_API_KEY not set",
        )

    client = OpenAI(api_key=api_key)
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    start_time = time.time()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        latency_ms = (time.time() - start_time) * 1000

        return BenchmarkResult(
            provider="openai",
            model=model,
            prompt=prompt,
            response=response.choices[0].message.content,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
            latency_ms=latency_ms,
            success=True,
        )
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        return BenchmarkResult(
            provider="openai",
            model=model,
            prompt=prompt,
            response="",
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
            latency_ms=latency_ms,
            success=False,
            error=str(e),
        )


def run_anthropic_benchmark(
    prompt: str,
    model: str = "claude-3-5-sonnet-20241022",
    api_key: Optional[str] = None,
    system_prompt: Optional[str] = None,
) -> BenchmarkResult:
    """Run benchmark using Anthropic API."""
    import anthropic

    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return BenchmarkResult(
            provider="anthropic",
            model=model,
            prompt=prompt,
            response="",
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
            latency_ms=0,
            success=False,
            error="ANTHROPIC_API_KEY not set",
        )

    client = anthropic.Anthropic(api_key=api_key)

    start_time = time.time()
    try:
        kwargs = {
            "model": model,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        response = client.messages.create(**kwargs)
        latency_ms = (time.time() - start_time) * 1000

        return BenchmarkResult(
            provider="anthropic",
            model=model,
            prompt=prompt,
            response=response.content[0].text,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.input_tokens + response.usage.output_tokens,
            latency_ms=latency_ms,
            success=True,
        )
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        return BenchmarkResult(
            provider="anthropic",
            model=model,
            prompt=prompt,
            response="",
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
            latency_ms=latency_ms,
            success=False,
            error=str(e),
        )


def run_benchmark(
    provider: str,
    model: str,
    prompt: str,
    system_prompt: Optional[str] = None,
) -> BenchmarkResult:
    """Run benchmark for a specific provider and model."""
    if provider == "openai":
        return run_openai_benchmark(prompt, model, system_prompt=system_prompt)
    elif provider == "anthropic":
        return run_anthropic_benchmark(prompt, model, system_prompt=system_prompt)
    else:
        return BenchmarkResult(
            provider=provider,
            model=model,
            prompt=prompt,
            response="",
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
            latency_ms=0,
            success=False,
            error=f"Unknown provider: {provider}",
        )


def calculate_summary(results: List[BenchmarkResult]) -> BenchmarkSummary:
    """Calculate summary statistics from benchmark results."""
    successful = [r for r in results if r.success]
    failed = [r for r in results if not r.success]

    return BenchmarkSummary(
        results=results,
        total_runs=len(results),
        successful_runs=len(successful),
        failed_runs=len(failed),
        avg_latency_ms=sum(r.latency_ms for r in successful) / len(successful) if successful else 0,
        total_tokens=sum(r.total_tokens for r in successful),
    )


def display_results_table(results: List[BenchmarkResult]) -> None:
    """Display benchmark results in a table."""
    table = Table(title="📊 Benchmark Results", border_style="blue")
    table.add_column("Provider", style="bold cyan")
    table.add_column("Model", style="bold")
    table.add_column("Status", justify="center")
    table.add_column("Latency (ms)", justify="right")
    table.add_column("Tokens", justify="right")
    table.add_column("Response Preview", max_width=40)

    for result in results:
        status = "[green]✓[/green]" if result.success else "[red]✗[/red]"
        latency = f"{result.latency_ms:.0f}"
        tokens = f"{result.total_tokens:,}"
        preview = result.response[:40] + "..." if len(result.response) > 40 else result.response

        table.add_row(
            result.provider,
            result.model,
            status,
            latency,
            tokens,
            preview,
        )

    console.print(table)


def display_summary(summary: BenchmarkSummary) -> None:
    """Display benchmark summary."""
    table = Table(title="📈 Summary Statistics", border_style="green")
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")

    table.add_row("Total Runs", str(summary.total_runs))
    table.add_row("Successful", f"[green]{summary.successful_runs}[/green]")
    table.add_row("Failed", f"[red]{summary.failed_runs}[/red]")
    table.add_row("Avg Latency", f"{summary.avg_latency_ms:.0f} ms")
    table.add_row("Total Tokens", f"{summary.total_tokens:,}")

    console.print(table)


def load_config(config_path: str) -> Dict[str, Any]:
    """Load benchmark configuration from YAML file."""
    import yaml

    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def save_results_json(results: List[BenchmarkResult], output_path: str) -> None:
    """Save benchmark results to JSON file."""
    import json

    data = {
        "results": [
            {
                "provider": r.provider,
                "model": r.model,
                "prompt": r.prompt,
                "response": r.response,
                "input_tokens": r.input_tokens,
                "output_tokens": r.output_tokens,
                "total_tokens": r.total_tokens,
                "latency_ms": r.latency_ms,
                "success": r.success,
                "error": r.error,
            }
            for r in results
        ],
        "summary": {
            "total_runs": len(results),
            "successful_runs": sum(1 for r in results if r.success),
            "failed_runs": sum(1 for r in results if not r.success),
            "avg_latency_ms": sum(r.latency_ms for r in results if r.success) / sum(1 for r in results if r.success) if any(r.success for r in results) else 0,
            "total_tokens": sum(r.total_tokens for r in results if r.success),
        },
    }

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    console.print(f"[green]Results saved to {output_path}[/green]")


def run_gemini_benchmark(
    prompt: str,
    model: str = "gemini-2.0-flash",
    api_key: Optional[str] = None,
    system_prompt: Optional[str] = None,
) -> BenchmarkResult:
    """Run benchmark using Google Gemini API."""
    api_key = api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return BenchmarkResult(
            provider="gemini", model=model, prompt=prompt,
            response="", input_tokens=0, output_tokens=0, total_tokens=0,
            latency_ms=0, success=False, error="GEMINI_API_KEY not set",
        )
    
    import time
    start = time.time()
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        contents = [{"role": "user", "parts": [{"text": prompt}]}]
        if system_prompt:
            contents.insert(0, {"role": "model", "parts": [{"text": system_prompt}]})
        
        payload = {"contents": contents, "generationConfig": {"temperature": 0.3}}
        resp = requests.post(url, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        
        response_text = data["candidates"][0]["content"]["parts"][0]["text"]
        usage = data.get("usageMetadata", {})
        
        return BenchmarkResult(
            provider="gemini", model=model, prompt=prompt,
            response=response_text,
            input_tokens=usage.get("promptTokenCount", 0),
            output_tokens=usage.get("candidatesTokenCount", 0),
            total_tokens=usage.get("totalTokenCount", 0),
            latency_ms=(time.time() - start) * 1000,
            success=True,
        )
    except Exception as e:
        return BenchmarkResult(
            provider="gemini", model=model, prompt=prompt,
            response="", input_tokens=0, output_tokens=0, total_tokens=0,
            latency_ms=(time.time() - start) * 1000,
            success=False, error=str(e),
        )
