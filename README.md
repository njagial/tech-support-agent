# AI-Powered Pocket Mobile Tech Support Agent

A production-grade mobile application with AI-powered diagnostics, multi-modal analysis, and guided troubleshooting.

## Features

- **Conversational AI Support**: Claude-powered agent for natural language tech support
- **Device Telemetry**: Real-time battery, storage, memory, and network diagnostics
- **Multi-Modal Analysis**: Screenshot analysis with Claude Vision for visual diagnostics
- **Knowledge Base**: RAG-powered search over technical documentation
- **Deep Link Navigation**: Direct access to OS settings for guided fixes
- **Privacy-First**: Client-side PII masking with human-in-the-loop approvals

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Mobile App     │────>│  Backend API     │────>│  Claude LLM     │
│  (React Native) │     │  (FastAPI)       │     │  (Anthropic)    │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                           │
┌─────────────────┐     ┌──────────────────┐              │
│  Qdrant DB      │<────│  RAG Knowledge   │              │
│  (Vector Store) │     │  Base            │              │
└─────────────────┘     └──────────────────┘              └────────────────┐
                                                                         │
┌─────────────────┐                                                      │
│  PII Masking    │─────────────────────────────────────────────────────┘
│  (Client-side)  │
└─────────────────┘
```

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Docker and Docker Compose (optional)
- Anthropic API Key

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

# Run with Docker
docker-compose up -d

# Or run locally
uvicorn app.main:app --reload --port 8000
```

### Mobile App Setup

```bash
cd mobile

# Install dependencies
npm install

# Start the app
npx expo start
```

## Project Structure

```
Tech Support/
├── mobile/                    # React Native App
│   ├── src/
│   │   ├── components/       # UI Components
│   │   ├── services/         # API & Services
│   │   ├── store/            # State Management
│   │   ├── hooks/            # Custom Hooks
│   │   └── types/            # TypeScript Types
│   └── package.json
├── backend/                   # Python Backend
│   ├── app/
│   │   ├── api/             # API Routes
│   │   ├── agent/           # LangGraph Agent
│   │   ├── services/        # Business Logic
│   │   ├── models/          # Data Models
│   │   └── utils/           # Utilities
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```

## Development

### Running Tests

```bash
# Backend
cd backend
pytest tests/ --cov=app

# Mobile
cd mobile
npm test
```

### Environment Variables

```bash
# Backend (.env)
ANTHROPIC_API_KEY=your_api_key_here
QDRANT_URL=http://localhost:6333
DEBUG=true
CORS_ORIGINS=http://localhost:8100
```

## Deployment

### Backend (AWS ECS)

```bash
# Build and push Docker image
docker build -t tech-support-agent .
aws ecr create-repository --repository-name tech-support-agent
docker push <account-id>.dkr.ecr.region.amazonaws.com/tech-support-agent:latest
```

### Mobile App

```bash
# Build for iOS
cd mobile
npx expo build:ios

# Build for Android
npx expo build:android
```

## Security

- All PII is masked client-side before transmission
- Human-in-the-loop approval required for destructive actions
- HTTPS enforced for all API communication
- JWT authentication with refresh tokens
- Rate limiting on all public endpoints

## License

MIT License - See LICENSE file for details
