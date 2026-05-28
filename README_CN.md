[English](README.md) | [中文](README_CN.md)

# 🧪 prompt-bench

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)]()

> 跨多个LLM提供商进行提示词基准测试和对比

## ✨ 功能特性

- 🔌 **多提供商** - 支持OpenAI和Anthropic API
- 📊 **详细指标** - 延迟、token使用量、响应对比
- 📝 **YAML配置** - 在YAML中定义复杂测试场景
- 🔄 **多次运行** - 多次运行测试以提高准确性
- 📈 **统计汇总** - 平均延迟、总token、成功率
- 💾 **JSON导出** - 导出结果用于进一步分析
- 🎨 **美观输出** - 终端表格和彩色格式化
- ⚡ **快速** - 尽可能并行执行

## 📦 安装

### 通过PyPI安装（推荐）

```bash
pip install prompt-bench
```

### 从源码安装

```bash
git clone https://github.com/Alex-2Code/prompt-bench.git
cd prompt-bench
pip install -e .
```

## 🔧 配置

1. 获取API密钥：
   - OpenAI: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Anthropic: [console.anthropic.com](https://console.anthropic.com/)

2. 设置API密钥：

```bash
export OPENAI_API_KEY="sk-your-openai-key"
export ANTHROPIC_API_KEY="sk-ant-your-anthropic-key"
```

## 🚀 使用方法

### 快速开始

```bash
# 测试简单提示词
prompt-bench run --prompt "What is 2+2?"

# 测试指定提供商
prompt-bench run --prompt "Explain AI" --provider openai

# 多次运行测试
prompt-bench run --prompt "Hello" --runs 3

# 从文件测试
prompt-bench run --file prompt.txt
```

### YAML配置

创建 `config.yaml` 文件：

```yaml
system_prompt: "You are a helpful assistant."

prompts:
  - name: "数学"
    text: "What is 2 + 2?"
  - name: "代码"
    text: "Write a Python function to calculate factorial"
  - name: "解释"
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

运行测试：

```bash
prompt-bench bench config.yaml --output results.json
```

### 命令参考

```bash
# 使用内联提示词运行测试
prompt-bench run [OPTIONS]

选项:
  -p, --provider [openai|anthropic|all]  LLM提供商 (默认: all)
  -m, --model TEXT                       指定使用的模型
  -P, --prompt TEXT                      要测试的提示词
  -f, --file TEXT                        包含提示词的文件
  -s, --system-prompt TEXT               系统提示词
  -o, --output TEXT                      输出JSON文件路径
  -n, --runs INT                         运行次数 (默认: 1)
  --help                                 显示帮助信息

# 从YAML配置运行
prompt-bench bench [OPTIONS] CONFIG_FILE

选项:
  -o, --output TEXT  输出JSON文件路径
  --help             显示帮助信息

# 列出可用提供商
prompt-bench providers

# 显示示例配置
prompt-bench example
```

## 📖 使用示例

### 示例 1: 简单对比

```bash
$ prompt-bench run --prompt "What is 2+2?" --runs 3

📊 测试结果

┌──────────┬─────────────────────────┬────────┬─────────────┬─────────┬──────────────────────┐
│ 提供商   │ 模型                    │ 状态   │ 延迟 (ms)   │  Tokens │ 响应预览             │
├──────────┼─────────────────────────┼────────┼─────────────┼─────────┼──────────────────────┤
│ openai   │ gpt-4o-mini             │   ✓    │        234  │      25 │ 2 + 2 = 4...         │
│ openai   │ gpt-4o-mini             │   ✓    │        198  │      25 │ 2 + 2 = 4...         │
│ openai   │ gpt-4o-mini             │   ✓    │        212  │      25 │ 2 + 2 = 4...         │
│ anthropic│ claude-3-5-sonnet-20... │   ✓    │        456  │      30 │ 2 + 2 equals 4...    │
│ anthropic│ claude-3-5-sonnet-20... │   ✓    │        423  │      30 │ 2 + 2 equals 4...    │
│ anthropic│ claude-3-5-sonnet-20... │   ✓    │        445  │      30 │ 2 + 2 equals 4...    │
└──────────┴─────────────────────────┴────────┴─────────────┴─────────┴──────────────────────┘

📈 统计汇总

┌─────────────┬─────────┐
│ 指标        │     数值│
├─────────────┼─────────┤
│ 总运行次数  │       6 │
│ 成功        │       6 │
│ 失败        │       0 │
│ 平均延迟    │    328  │
│ 总Tokens    │     165 │
└─────────────┴─────────┘
```

### 示例 2: 从YAML配置运行

```bash
$ prompt-bench bench config.yaml --output results.json

从配置运行测试: config.yaml

提示词: 数学
提示词: 代码
提示词: 解释

...

结果已保存到 results.json
```

## 🔌 支持的提供商

| 提供商 | 默认模型 | API密钥环境变量 |
|--------|----------|-----------------|
| OpenAI | gpt-4o-mini | `OPENAI_API_KEY` |
| Anthropic | claude-3-5-sonnet-20241022 | `ANTHROPIC_API_KEY` |

### 支持的模型

**OpenAI:**
- gpt-4o
- gpt-4o-mini
- gpt-4-turbo
- gpt-3.5-turbo

**Anthropic:**
- claude-3-5-sonnet-20241022
- claude-3-opus-20240229
- claude-3-haiku-20240307

## 🤝 贡献

欢迎贡献！请随时提交Pull Request。

## 📄 许可证

本项目基于MIT许可证 - 详见 [LICENSE](LICENSE) 文件

## 📧 联系方式

- GitHub: [@Alex-2Code](https://github.com/Alex-2Code)

---

由 [Alex-2Code](https://github.com/Alex-2Code) 用 ❤️ 制作
