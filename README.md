![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite&logoColor=white)
![Deploy](https://img.shields.io/badge/deploy-Render%20%2B%20Vercel-black?style=flat)
# BalonPie

Estadísticas en tiempo real de la Liga Profesional Argentina — partidos, equipos, tablas de posiciones y alineaciones tácticas.

🔗 **Demo:** [balon-pie.vercel.app](https://balon-pie.vercel.app)
🔗 **API:** [balonpie-api.onrender.com](https://balonpie-api.onrender.com)

Real-time stats for the Argentine Liga Profesional — matches, teams, standings, and tactical lineups.

🔗 **Live demo:** [balon-pie.vercel.app](https://balon-pie.vercel.app)
🔗 **API:** [balonpie-api.onrender.com](https://balonpie-api.onrender.com)

---

## Stack

- **Backend:** Python, FastAPI
- **Frontend:** React, TypeScript, Vite
- **Deploy:** Render (backend) · Vercel (frontend)
- **Fuente de datos / Data source:** [API-Football](https://www.api-football.com/)
- **Testing:** 47 tests pasando · 47 passing tests

## Funcionalidades / Features

- Listado de partidos por fecha con resultado en vivo
- Perfiles de equipo con plantel y estadísticas
- Tabla de posiciones actualizada
- Vista de detalle de partido (alineaciones, formación, suplentes, DT)

- Match listings by date with live scores
- Team profiles with roster and stats
- Live standings table
- Match detail view (lineups, formation, substitutes, coach)

## En desarrollo / In progress

- [ ] Selector de temporada / Season selector
- [ ] Vista táctica de formación / Tactical formation view
- [ ] Búsqueda de equipos en tiempo real / Real-time team search

## Correr el proyecto localmente / Running locally

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

> Nota: verificá los nombres exactos de carpetas y comandos contra tu `AGENTS.md` / package.json antes de publicar, por si difieren de este ejemplo.
> Note: check exact folder names and scripts against your `AGENTS.md` / package.json before publishing, in case they differ from this example.

## Limitaciones conocidas / Known limitations

Corre sobre el plan gratuito de API-Football: 100 requests/día, temporadas 2022–2024 únicamente, sin endpoints `next`/`last`, sin búsqueda de fixtures por nombre.

Runs on API-Football's free tier: 100 requests/day, seasons 2022–2024 only, no `next`/`last` endpoints, no fixture search by name.

## Licencia / License

MIT
