# Private Mobile Search Engine

A private, self-hosted search engine starter for mobile apps. This project includes:
- a private backend API using FastAPI
- a full-text engine powered by Meilisearch
- a polite crawler for indexing a curated list of sites
- a Flutter mobile client for Android/iOS
- Docker-based local setup

## Architecture

- API: FastAPI
- Search index: Meilisearch
- Crawler: Python + BeautifulSoup
- Mobile app: Flutter

## Quick start

### 1) Start the search stack

```bash
docker compose up --build
```

This starts:
- Meilisearch on http://localhost:7700
- API on http://localhost:8000

### 2) Index a site

```bash
python3 crawler/crawler.py --url https://example.com --api-url http://localhost:8000 --api-key change-me
```

### 3) Search from the API

```bash
curl -H "x-api-key: change-me" "http://localhost:8000/search?q=example"
```

### 4) Run the mobile app

```bash
cd mobile/flutter_app
flutter pub get
flutter run
```

Note: for Android emulator use `http://10.0.2.2:8000` in the app config. For a physical device, use your LAN IP.

## Configuration

Edit the environment variables in `docker-compose.yml`:
- `MEILI_MASTER_KEY`
- `MEILI_API_KEY`
- `API_KEY`

## Security notes

- run behind HTTPS in production
- use a real secret instead of `change-me`
- restrict API access to your mobile app / VPN / trusted IPs
- respect robots.txt and website terms

## Roadmap

- add semantic search with embeddings
- add per-user indexing and history
- add site filters and bookmarks
- add search result ranking controls
- add offline mode and cached results

## License

MIT