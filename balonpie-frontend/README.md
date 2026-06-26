# balonpie-frontend

Frontend React + TypeScript + Vite de BalonPie.

Consume el backend local de `balonpie-api` y muestra:

- inicio con navegacion entre fechas
- tabla de posiciones
- listado de equipos
- perfil de equipo
- detalle de partido

## Requisitos

- Node.js
- backend corriendo en `http://127.0.0.1:8000`
- `VITE_API_URL` configurado en `.env.local`

## Desarrollo local

1. Instalar dependencias: `npm install`
2. Revisar `VITE_API_URL` en `.env.local`
3. Levantar Vite: `npm run dev`

URL local esperada: `http://127.0.0.1:4173`

## Scripts

- `npm run dev`
- `npm run build`
- `npm run lint`
- `npm run preview`

## Notas del estado actual

- El frontend ya no es el template vacio de Vite; el README anterior habia quedado obsoleto.
- La UI ya incorpora escudos, rediseno principal y ajustes responsive del dock.
- La vista que mas margen de mejora tiene hoy es el detalle de partido.
