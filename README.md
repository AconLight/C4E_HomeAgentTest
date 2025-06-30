# C4E Home Agent Test

This project implements an intelligent home agent system with energy optimization capabilities.

## Quick Start

After cloning the repository, run the setup script:

```bash
bash setup.sh
```

This will:
1. Check for required system dependencies (Python 3.10+, pip)
2. Create a Python virtual environment
3. Install all project dependencies

### Alternative: Manual Setup

If you prefer not to use the shell script, you can set up manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Project Structure

```
├── core/                     # Reusable logic, abstractions, interfaces
│   ├── agents/              # LLM-based agents, planners, decision modules
│   ├── strategy/            # Strategy suggestion & evaluation logic
│   ├── models/              # ML models: training, prediction, pipelines
│   ├── simulation/          # Abstract sensor/actuator simulation logic
│   ├── interfaces/          # Common interfaces (e.g. Sensor, Agent)
│   └── utils/               # Logging, config loader, shared tools
├── data/                    # Local data, logs, datasets, sensor dumps
├── services/                # Integration-specific code
└── tests/                   # Test suites
```

## Running Tests

After setting up the environment:

```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate

# Run all tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=core

# Run specific test file
python -m pytest tests/unit/test_environment.py
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your configuration values:
- API settings
- Home Assistant connection details
- Hedera network settings
- Model paths and parameters

## Development

- Run simulation: `python scripts/run_simulation.py`
- Train model: `python scripts/train_model.py`
- Test agent: `python scripts/test_agent.py`
- Visualize results: `python scripts/visualize_results.py`

## Requirements

- Python 3.10 or higher
- See `requirements.txt` for Python package dependencies