@AGENTS.md

# BalonPie

Estadísticas en tiempo real de la Liga Profesional Argentina — partidos, equipos, tablas de posiciones y alineaciones tácticas. Pieza de portfolio para búsqueda de pasantía/trabajo en Data Science/dev.

## Claude's Role

Mantener y extender el producto: features pendientes (selector de temporada, vista táctica de formación, búsqueda de equipos en tiempo real), debugging contra las limitaciones reales del plan gratuito de API-Football, sostener los tests en verde.

If a session is drifting without moving toward una de las features pendientes o un fix real, nudge me back: "¿Esto suma al roadmap (selector de temporada / vista táctica / búsqueda de equipos), o es una distracción del día?"

## Process

1. La idea sale de lo que falta en el README (`En desarrollo / In progress`) o de un bug encontrado al usar la app
2. Se implementa en `balonpie-api` (backend) y/o `balonpie-frontend` (frontend)
3. Tests de backend corren en verde antes de dar por cerrada una feature
4. Deploy: push a `main` → Render (backend) + Vercel (frontend) redeploy automático

## Key People

Solo yo (Matías).

## Folder Structure

- `balonpie-api/` — backend FastAPI (Python), consume API-Football
- `balonpie-frontend/` — frontend React/TS/Vite
- `00 System/` — scripts/config reusables de este proyecto (vacío por ahora)
- `01 Skills/` — skills en markdown de este proyecto (vacío por ahora)
- `02 Attachments/` — screenshots; `playwright-output/` son capturas de sesiones de testing visual (gitignored)
- `03 Iteration Logs/` — notas de qué mejorar entre iteraciones (vacío por ahora)

## Rules & Conventions

- **`(C)` prefix** — Archivos creados por Claude llevan prefijo `(C)`
- **Editing rule** — Antes de editar un archivo sin el prefijo `(C)`, pedir permiso primero
- **Skills** — Automatizaciones reusables de este proyecto van en `01 Skills/` como markdown, no como Claude Code skills
- API-Football (free tier): 100 requests/día, solo temporadas 2022-2024, sin endpoints `next`/`last` ni búsqueda de fixtures por nombre — no asumir que hay más data disponible

## Current Status

> **Last updated:** 2026-07-13
> **Status:** Activo. 47 tests de backend pasando. Último commit real: 2026-07-06 ("fix: add missing FootballFabPrototype component").

Pendiente: selector de temporada, vista táctica de formación, búsqueda de equipos en tiempo real.
