# 🧪 prompt-bench

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)]()

> Benchmark and compare LLM prompts across different providers (OpenAI, Anthropic).

## ✨ Features

- 🔌 **Multi-Provider** - Support OpenAI and Anthropic APIs
- 📊 **Detailed Metrics** - Latency, token usage, response comparison
- 📝 **YAML Config** - Define complex benchmark scenarios in YAML
- 🔄 **Multiple Runs** - Run benchmarks multiple times for accuracy
- 📈 **Summary Stats** - Average latency, total tokens, success rates
- 💾 **JSON Export** - Export results for further analysis
- 🎨 **Beautiful Output** - Rich terminal tables and formatting
- ⚡ **Fast** - Parallel execution where possible

## 📦 Installation

### From PyPI (recommended)

```bash
pip install prompt-bench
```

### From source

```bash
git clone https://github.com/Alex-2Code/prompt-bench.git
cd prompt-bench
pip install -e .
```

## 🔧 Setup

1. Get API keys:
   - OpenAI: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Anthropic: [console.anthropic.com](https://console.anthropic.com/)

2. Set the API keys:

```bash
export OPENAI_API_KEY="sk-your-openai-key"
export ANTHROPIC_API_KEY="sk-ant-your-anthropic-key"
```

## 🚀 Usage

### Quick Start

```bash
# Test a simple prompt
prompt-bench run --prompt "What is 2+2?"

# Test with specific provider
prompt-bench run --prompt "Explain AI" --provider openai

# Test multiple runs
prompt-bench run --prompt "Hello" --runs 3

# Test from file
prompt-bench run --file prompt.txt
```

### YAML Configuration

Create a `config.yaml` file:

```yaml
system_prompt: "You are a helpful assistant."

prompts:
  - name: "Math"
    text: "What is 2 + 2?"
  - name: "Code"
    text: "Write a Python function to calculate factorial"
  - name: "Explanation"
    text: "Explain quantum computing in simple terms"

providers:
  - provider: openai
    model: gpt-4o-mini
  - provider: openai
    model: gpt-4o
  - provider: anthropic
    model: claude-3-5-sonnet-20241022

runs: 3
```

Run the benchmark:

```bash
prompt-bench bench config.yaml --output results.json
```

### Command Reference

```bash
# Run benchmark with inline prompt
prompt-bench run [OPTIONS]

Options:
  -p, --provider [openai|anthropic|all]  LLM provider (default: all)
  -m, --model TEXT                       Specific model to use
  -P, --prompt TEXT                      Prompt to test
  -f, --file TEXT                        File containing the prompt
  -s, --system-prompt TEXT               System prompt to use
  -o, --output TEXT                      Output JSON file path
  -n, --runs INT                         Number of runs (default: 1)
  --help                                 Show this message and exit

# Run from YAML config
prompt-bench bench [OPTIONS] CONFIG_FILE

Options:
  -o, --output TEXT  Output JSON file path
  --help             Show this message and exit

# List available providers
prompt-bench providers

# Show example config
prompt-bench example
```

## 📖 Examples

### Example 1: Simple Comparison

```bash
$ prompt-bench run --prompt "What is 2+2?" --runs 3

📊 Benchmark Results

┌──────────┬─────────────────────────┬────────┬─────────────┬─────────┬──────────────────────┐
│ Provider │ Model                   │ Status │ Latency (ms)│  Tokens │ Response Preview     │
├──────────┼─────────────────────────┼────────┼─────────────┼─────────┼──────────────────────┤
│ openai   │ gpt-4o-mini             │   ✓    │        234  │      25 │ 2 + 2 = 4...         │
│ openai   │ gpt-4o-mini             │   ✓    │        198  │      25 │ 2 + 2 = 4...         │
│ openai   │ gpt-4o-mini             │   ✓    │        212  │      25 │ 2 + 2 = 4...         │
│ anthropic│ claude-3-5-sonnet-20... │   ✓    │        456  │      30 │ 2 + 2 equals 4...    │
│ anthropic│ claude-3-5-sonnet-20... │   ✓    │        423  │      30 │ 2 + 2 equals 4...    │
│ anthropic│ claude-3-5-sonnet-20... │   ✓    │        445  │      30 │ 2 + 2 equals 4...    │
└──────────┴─────────────────────────┴────────┴─────────────┴─────────┴──────────────────────┘

📈 Summary Statistics

┌─────────────┬─────────┐
│ Metric      │   Value │
├─────────────┼─────────┤
│ Total Runs  │       6 │
│ Successful  │       6 │
│ Failed      │       0 │
│ Avg Latency │    328  │
│ Total Tokens│     165 │
└─────────────┴─────────┘
```

### Example 2: From YAML Config

```bash
$ prompt-bench bench config.yaml --output results.json

Running benchmark from config: config.yaml

Prompt: Math
Prompt: Code
Prompt: Explanation

...

Results saved to results.json
```

### Example 3: Export to JSON

```bash
$ prompt-bench run --prompt "Hello" --output results.json

Results saved to results.json
```

## 📊 Output Format

### JSON Output

```json
{
  "results": [
    {
      "provider": "openai",
      "model": "gpt-4o-mini",
      "prompt": "What is 2+2?",
      "response": "2 + 2 = 4",
      "input_tokens": 10,
      "output_tokens": 15,
      "total_tokens": 25,
      "latency_ms": 234.5,
      "success": true,
      "error": null
    }
  ],
  "summary": {
    "total_runs": 1,
    "successful_runs": 1,
    "failed_runs": 0,
    "avg_latency_ms": 234.5,
    "total_tokens": 25
  }
}
```

## 🔑 Supported Providers

| Provider | Default Model | API Key Env Var |
|----------|---------------|-----------------|
| OpenAI | gpt-4o-mini | `OPENAI_API_KEY` |
| Anthropic | claude-3-5-sonnet-20241022 | `ANTHROPIC_API_KEY` |

### Supported Models

**OpenAI:**
- gpt-4o
- gpt-4o-mini
- gpt-4-turbo
- gpt-3.5-turbo

**Anthropic:**
- claude-3-5-sonnet-20241022
- claude-3-opus-20240229
- claude-3-haiku-20240307

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for the amazing API
- [Anthropic](https://www.anthropic.com/) for Claude
- [Click](https://click.palletsprojects.com/) for the CLI framework
- [Rich](https://rich.readthedocs.io/) for beautiful terminal output

## 📧 Contact

- GitHub: [@Alex-2Code](https://github.com/Alex-2Code)

---

Made with ❤️ by [Alex-2Code](https://github.com/Alex-2Code)
