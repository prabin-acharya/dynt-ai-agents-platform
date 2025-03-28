# DYNT AI Agents

A platform that uses AI agents to provide automated financial insights and recommendations for businesses.

## Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API key
- AgentsOPS API key

### Setup

1. Clone and install dependencies:
```bash
git clone https://github.com/your-org/dynt-ai-agents.git
cd dynt-ai-agents
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env

# Add to .env:
OPENAI_API_KEY=your-key-here
AGENTSOPS_API_KEY=your-key-here
```

3. Run the application:
```bash
python app.py
```

## Available Agents

### Financial Advisor Agent
- Analyzes transaction data and provides financial recommendations
- Supports human-in-the-loop review process

### Coming Soon
- Cash Flow Agent
- Compliance Agent

## Testing

Run tests with:
```bash
# Run all tests
pytest

# Test specific agent
pytest tests/test_financial_advisor.py
```

## Development

1. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Test your changes:
```bash
pytest
```

3. Create a pull request

## Support

Need help? Create an issue in the repository.

## Version History

- v0.1.0 - Initial release with Financial Advisor Agent
- v0.2.0 - Added production data testing capabilities 