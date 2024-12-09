# MCP Server Memos 📝

[![PyPI version](https://img.shields.io/pypi/v/mcp-server-memos.svg)](https://pypi.org/project/mcp-server-memos/)
[![Python Version](https://img.shields.io/pypi/pyversions/mcp-server-memos.svg)](https://pypi.org/project/mcp-server-memos/)
[![License](https://img.shields.io/github/license/RyoJerryYu/mcp-server-memos-py.svg)](https://github.com/RyoJerryYu/mcp-server-memos-py/blob/master/LICENSE)

A Python package that provides LLM models with the ability to interact with [Memos](https://github.com/usememos/memos) server through the [MCP (Model Control Protocol)](https://github.com/mcp-plugins) interface.

## 🚀 Features

- 🔍 Search memos with keywords
- ✨ Create new memos with customizable visibility
- 📖 Retrieve memo content by ID
- 🏷️ List and manage memo tags
- 🔐 Secure authentication using access tokens

## 🛠️ Usage

You can include this package in your config file as bellow, just as you use other Python MCP plugins.

```jsonc
{
  ...,
  "mcpServers": {
    "fetch": { // other mcp servers
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    },
    "memos": {
      "command": "uvx",
      "args": [
        "mcp-server-memos",
        "--host",
        "localhost",
        "--port",
        "5230",
        "--token",
        "your-access-token-here"
      ]
    }
  }
}
```

<details>
<summary>Other ways to use this package</summary>

### 📦 Installation

```bash
pip install mcp-server-memos
```

### Command Line

```bash
mcp-server-memos --host localhost --port 8080 --token YOUR_ACCESS_TOKEN
```

### As a Library

```python
from mcp_server_memos import Config, serve_stdio

config = Config(
    host="localhost",
    port=8080,
    token="YOUR_ACCESS_TOKEN"
)

await serve_stdio(config=config)
```

</details>

## 🔧 Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `host` | Memos server hostname | `localhost` |
| `port` | Memos server port | `8080` |
| `token` | Access token for authentication | `""` |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Memos](https://github.com/usememos/memos) - A lightweight, self-hosted memo hub
- [MCP (Model Control Protocol)](https://github.com/mcp-plugins) - Protocol for LLM model control
```

This README includes:

1. Project title with an emoji
2. Shields.io badges for PyPI version, Python version, and license
3. Brief description with links to related projects
4. Features section with emojis
5. Installation instructions
6. Usage examples for both CLI and library use
7. Configuration table
8. Contributing section
9. License information
10. Acknowledgments

The badges will automatically update based on your PyPI package and GitHub repository information. You may need to adjust some of the URLs and badge parameters to match your actual repository and package details.
