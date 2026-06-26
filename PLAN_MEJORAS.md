# Plan de mejoras — BalonPie

**Fecha:** 2026-06-24
**Estado:** Investigación completa, sin implementar — pendiente de tu revisión.

Este documento investiga qué datos están realmente disponibles en el plan Free de API-Football para las 4 competiciones de BalonPie, propone cómo expandir el backend en base a eso, propone un rediseño visual inspirado en 4 referencias reales, y sugiere un orden de implementación.

---

## 1. Datos disponibles en el plan Free

Investigado contra la API real (no documentación genérica) con la key del `.env`, hoy 2026-06-24. Cuenta: Free, 100 requests/día (quedan ~59 al cerrar esta investigación), límite también por minuto (~10-15/min, lo pegué una vez).

### 1.1 Seasons: lo que existe vs. lo que el plan Free deja consultar

`/leagues?id=X` devuelve el historial completo de seasons de cada competición (esto no depende del plan, es metadata pública). Pero **consultar datos** (`/standings`, `/fixtures`, `/teams/statistics`) en una season fuera de rango devuelve `errors.plan` sin tirar error HTTP — la respuesta es 200 OK con `response: []`.

| Liga | Seasons que existen (API) | Seasons consultables en Free | Season actual real |
|---|---|---|---|
| Liga Profesional (128) | 2021–2026 | **2022, 2023, 2024** (confirmado: error exacto es *"Free plans do not have access to this season, try from 2022 to 2024"*) | 2026 |
| Copa Argentina (130) | 2020, 2022–2026 | 2022, 2023, 2024 (mismo rango, es restricción de cuenta, no de liga) | 2026 |
| Copa Libertadores (13) | 2021–2026 | 2022, 2023, 2024 (confirmado explícitamente, mismo mensaje de error) | 2026 |
| Copa Sudamericana (14) | 2020 (sin cobertura), 2021–2025 | 2022, 2023, 2024 | 2025 |

**Conclusión clave:** el límite de seasons (2022-2024) es **de la cuenta, no de cada liga** — confirmado probando el mismo error en Liga Profesional y en Libertadores. No hay forma de acceder a la season actual (2025/2026) sin upgradear el plan, sin importar qué endpoint o competición.

### 1.2 Parámetros bloqueados — confirmado que es global, no por liga

| Parámetro | Estado en Free | Evidencia |
|---|---|---|
| `next` (próximos N fixtures) | **Bloqueado siempre**, cualquier season, cualquier liga | Error idéntico en league=128 y league=13: *"Free plans do not have access to the Next parameter"* |
| `last` (últimos N fixtures) | **Bloqueado siempre**, mismo patrón | Mismo tipo de error, confirmado en `get_last_fixtures` |
| `from` / `to` (rango de fechas) | **Funciona en las 4 competiciones**, season 2022-2024 | Ver tabla 1.3 |
| `round` (fecha/jornada por nombre) | **Funciona** — alternativa más precisa que `from`/`to` para Liga Profesional | Ver 1.4 |
| `live=all` (snapshot en vivo) | **Funciona sin restricción de season** — esto ya está en producción y no cambia | Ya implementado en `api_football.get_live_snapshot` |
| `team` + `league` + `season` (stats de equipo) | **Funciona**, incluida en copas | Ver 1.5 |

### 1.3 `from`/`to` probado en las 4 competiciones (season 2024, rango 2024-01-01 a 2024-12-31)

| Liga | Resultado | Nota |
|---|---|---|
| Liga Profesional (128) | ✅ funciona (ya en producción tras el cambio de season a 2024) | — |
| Copa Argentina (130) | ✅ 63 fixtures | Torneo de eliminación directa, partidos repartidos todo el año |
| Copa Libertadores (13) | ✅ 155 fixtures | Incluye fase de grupos + eliminación directa |
| Copa Sudamericana (14) | ✅ 192 fixtures | Idem |

Confirmado en los 3: el campo `logo` del equipo viene presente en cada fixture (ej. `"logo": "https://media.api-sports.io/football/teams/2827.png"`), sin costo de request adicional.

### 1.4 `round` — alternativa mejor que `from`/`to` para "última fecha" en Liga Profesional

Descubrimiento durante la investigación: `/fixtures/rounds?league=128&season=2024` devuelve la lista completa de fechas/jornadas (27 rounds, ej. `"2nd Phase - 27"`), **sin bloqueo de plan**. Pidiendo después `/fixtures?league=128&season=2024&round=<nombre>` devuelve exactamente los partidos de esa fecha (probado: 14 fixtures, una fecha completa de 28 equipos).

Esto es más preciso que adivinar un rango de fechas: en vez de "dame partidos entre estas dos fechas" (que puede cortar una fecha a la mitad o traer dos fechas mezcladas), se pide "dame la fecha N completa". Para `/ultima-fecha` esto es la opción correcta para Liga Profesional. Para las copas (formato de llave, no de fechas numeradas) el concepto de "round" es otro — son nombres como "Quarter-finals", no aplica el mismo patrón semanalmente.

### 1.5 Standings por competición — estructuras distintas, no es "una tabla para todas"

| Liga | `/standings` con season 2024 | Forma de los datos |
|---|---|---|
| Liga Profesional (128) | ✅ 28 equipos, tabla plana | Un solo array, como ya está implementado |
| Copa Argentina (130) | `results: 0` (vacío, sin error) | **No tiene standings** — es eliminación directa, no existe tabla. El `coverage.standings` de `/leagues` ya lo marca como `false` para todas sus seasons. No es un bug a arreglar, es que conceptualmente no aplica. |
| Copa Libertadores (13) | ✅ pero **8 grupos de 4 equipos**, no una tabla única | `response[0].league.standings` es un array de 8 arrays (Group A...H), cada uno con su propia mini-tabla, campo `form`, etc. |
| Copa Sudamericana (14) | `results: 0` para season 2024 específicamente | Inconsistente por año: `coverage.standings` es `true` en 2021 y 2025, `false` en 2022/2023/2024. Para la season que vamos a usar (2024) **no hay standings**, aunque conceptualmente el torneo sí tiene fase de grupos. |

### 1.6 Estadísticas y plantilla de equipo — funciona igual en copas

`/teams/statistics?team=450&league=130&season=2024` (un equipo de Copa Argentina) funcionó igual que para Liga Profesional — mismo endpoint, misma forma de respuesta, sin restricción adicional. `/teams?league=128&season=2024` devuelve el plantel completo (28 equipos confirmados) con `logo` por equipo.

### 1.7 Resumen ejecutivo de la sección

- **Season 2024 es el techo real** del plan Free — no hay forma de mostrar la temporada actual (2026) sin pagar.
- **`next`/`last` están muertos en Free** sin importar qué se intente — la única vía es `from`/`to` (genérico) o `round` (preciso, solo tiene sentido en formato liga).
- **Las copas no tienen "tabla" en el sentido tradicional** — Copa Argentina nunca, Sudamericana depende del año. Diseñar la UI asumiendo que siempre hay una tabla por competición es incorrecto.
- **Equipos, logos y estadísticas funcionan igual en las 4 competiciones** — esto es lo más sólido para expandir.

---

## 2. Plan de expansión de datos

### 2.1 Usar todas las seasons disponibles (2022, 2023, 2024)

Hoy `teams.SEASON` es una sola constante global (2024). Para aprovechar 2022-2024:

- Cambiar `SEASON` de constante fija a **parámetro de query opcional** en los endpoints que lo permitan (`?season=2023`), default 2024. Bajo riesgo, son ~4 líneas por endpoint en `main.py`.
- El frontend podría agregar un selector de temporada en `Tabla.tsx` y `Equipo.tsx` (no en `Inicio.tsx`/`Partido.tsx`, que dependen de "última fecha" puntual).
- **Decisión a tomar con vos:** ¿esto suma valor real, o es complejidad para mostrar 3 años de una liga que ya no se puede ver "en vivo"? Mi lectura: bajo prioridad comparado con el resto de esta lista.

### 2.2 Agregar todos los equipos de cada liga (no solo Boca y River)

`scripts/fetch_teams.py` ya existe y ya apunta a `SEASON=2024` (lo actualicé junto con el backend), pero solo se diseñó pensando en Liga Profesional. Plan concreto:

1. Extender el script para llamar `/teams?league=X&season=2024` por **cada una de las 4 competiciones** (4 requests, no 1).
2. Mergear por `team.id` — un mismo equipo (ej. Boca) aparece en varias competiciones. Esto rompe el supuesto actual de `Team.liga_id` como campo único: **hay que cambiarlo a `liga_ids: list[int]`** (o a una tabla de relación equipo↔competición separada) para que `/equipo/boca-juniors` pueda, por ejemplo, mostrar estadísticas de Liga Profesional y resultados recientes de Libertadores a la vez.
3. Slugify ya existe en el script (con manejo de acentos) — reusarlo tal cual.
4. Esto sale del free-tier rate limit por minuto fácilmente (4 ligas × ~28-50 equipos no son 4 requests, son 4 requests *de listado*, no uno por equipo — confirmado, `/teams?league=X` devuelve todos de una). Bajo costo: 4 requests totales.

**Pendiente de decisión:** ¿el perfil de un equipo que juega 2+ competiciones muestra stats de cuál por default? Propuesta: Liga Profesional si participa, sino la primera copa en que aparece.

### 2.3 Reemplazar `next`/`last` por alternativas reales

Esto es el cambio de mayor impacto y el que más conversación necesita, porque **no hay una alternativa que preserve el significado original** ("próximos partidos" reales no existen en una season 2024 ya terminada). Tres piezas separadas:

- **`/ultima-fecha`** → usar `round` (sección 1.4) para Liga Profesional: pedir `/fixtures/rounds`, tomar el último, pedir esa fecha completa. Para las copas, usar `from`/`to` sobre una ventana razonable (ej. último mes con partidos jugados) ya que no tienen "rounds" numerados de la misma forma.
- **`/proximos-partidos`** → **no tiene solución real dentro del plan Free + season histórica**. Las opciones honestas son:
  - (a) Sacarlo de la UI mientras estemos en season histórica, dejando solo "Última fecha" en Inicio.
  - (b) Resignificarlo como "Próxima fecha de la temporada 2024" (la fecha cronológicamente siguiente a la última mostrada) — sigue siendo pasado real, pero al menos tiene una progresión lógica navegable fecha por fecha.
  - (c) Upgradear el plan de API-Football (la única forma de tener próximos partidos *reales*).

  **Necesito que elijas (a), (b) o (c) antes de tocar código** — son UX distintos, no un detalle de implementación.
- **`resultados_recientes` en `/equipo/{nombre}`** → mismo problema que `last`. Reemplazar `get_team_fixtures` (que usa `last`) por una consulta `from`/`to` acotada a, por ejemplo, los últimos 60 días *dentro de la season 2024* (no del calendario real), o usar `round` si el equipo juega en Liga Profesional.

### 2.4 Incorporar escudos de equipos

Confirmado en 1.3 y 1.6: el campo `logo` ya viene en toda respuesta que incluye un equipo (fixtures, standings, `/teams`), sin costo extra. Cambios necesarios:

- `teams.py`: agregar campo `logo_url: str` a `Team`.
- `api_football.py`: todas las funciones `transform_*` que devuelven datos de equipo (`transform_fixture`, `transform_standing`, `transform_team_statistics`) deben agregar el campo `escudo` (nombre en español, consistente con el resto del backend) leyendo `equipo["logo"]`.
- `api.ts` (frontend): agregar `escudo: string` a `Partido`, `PosicionTabla`, `EquipoResumen`, `EstadisticasEquipo`.
- Componentes a tocar: `PartidoCard`, `Dock` no, `Tabla.tsx` (columna equipo), `Equipos.tsx` (grid), `Equipo.tsx` (header).

Esto es independiente de todo lo demás de esta sección — se puede hacer aunque no se resuelva nada de `next`/`last`.

---

## 3. Plan de rediseño visual del frontend

Visité las 4 referencias hoy (capturas reales, no memoria). Resumen de cada una y qué patrón concreto vale la pena traer.

### 3.1 Qué hace a cada referencia "verse profesional"

**Sofascore** — la más "app", no "página":
- Ticker superior con banderas de país + competición + hora/resultado, mucho más rico que un scroll de texto.
- Header de equipo/liga: escudo grande (~80px) a la izquierda, nombre + seguidores al lado, selector de season como dropdown (no como texto fijo).
- Estadísticas de partido como **barras horizontales comparativas** (no texto lado a lado): cada stat es una barra dividida en 2 colores según el % de cada equipo, con el valor numérico en cada extremo.
- Tabla de posiciones: escudo circular chico inline antes del nombre, chips de forma coloreados (W verde / D gris / L rojo) — esto ya lo tenemos.
- Fila del equipo actual resaltada con borde de color cuando se está viendo su perfil dentro de una tabla de grupo.

**Promiedos** — la más "diario deportivo", densidad de datos:
- Fondo verde sólido oscuro, sin gradientes ni cards flotando — todo es lista/tabla.
- Grid de equipos: escudo circular + nombre + **contador de títulos ganados** (🏆35 River) como dato curioso/identidad, no solo navegación.
- Perfil de equipo: dos tablas compactas lado a lado (Próximos partidos / Resultados), columnas Día-L/V-Rival-Hora — sin adornos.
- Timeline de partido ("Minuto a minuto"): eventos en 2 columnas según el equipo (local a la izquierda, visitante a la derecha en rojo), minuto al centro, ícono chico para amarilla/roja/VAR/cambio.

**ElNine** — entre Promiedos y algo más moderno:
- Mismo espíritu denso que Promiedos pero con sidebar de competiciones colapsable por país (bandera + nombre + cantidad de torneos), pills redondeadas para filtros (Todos/En vivo/Próximos/Finalizados).
- Selector de tema claro/oscuro visible en el header — dato menor pero confirma que el dark mode es la norma en este rubro, no la excepción.

**OneFootball** — la más "editorial/transmisión deportiva":
- Header de equipo/liga con el escudo real a tamaño grande (no genérico) sobre un **fondo con patrón geométrico diagonal oscuro** — es la firma visual más distintiva de las 4.
- Tipografía título: condensada, peso pesado, mayúsculas, mucho más grande que cualquier otro texto de la página (jerarquía agresiva).
- "Último resultado" / "Siguiente partido" como cards oscuras redondeadas con el escudo, marcador y una pill inferior con el nombre+ícono de la competición — patrón muy reusable para nuestra `PartidoCard`.

### 3.2 Por qué BalonPie hoy se ve "genérico" — diagnóstico concreto

Comparando contra las 4 referencias, lo que falta no es paleta (la nuestra está bien — verde césped + dorado + fondo oscuro es un lenguaje válido), sino:

1. **No hay escudos en ningún lado** — es lo que más diferencia a un sitio de fútbol de cualquier dashboard genérico. Las 4 referencias usan el escudo como elemento gráfico principal, no como detalle.
2. **Tipografía plana** — usamos Archivo Black para títulos, pero a un tamaño moderado y sin jerarquía agresiva. Las 4 referencias (sobre todo OneFootball y Sofascore) usan títulos *mucho* más grandes que el resto del contenido.
3. **Estadísticas como texto, no como comparación visual** — ya mejoramos esto hoy (de "key:value" plano a comparación lado a lado), pero Sofascore va un paso más allá con barras proporcionales.
4. **Tarjetas sin jerarquía visual entre estado/competición/marcador** — nuestra `PartidoCard` trata todo con el mismo peso; las referencias siempre separan claramente "metadata" (competición, hora) de "lo importante" (escudos + marcador).
5. **Sin "identidad" de equipo** — Promiedos suma el dato de títulos ganados; nosotros no tenemos ningún dato que haga sentir que cada equipo es distinto más allá del nombre.

### 3.3 Cambios concretos propuestos por página

**`PartidoCard`** (usada en Inicio y Equipo):
- Agregar escudo (24-32px) antes de cada nombre de equipo.
- Separar visualmente "competencia + hora" (ya está, mantenerlo chico/mutado) de "equipos + marcador" (subir el peso tipográfico del marcador, ya usa Archivo Black — agrandarlo).
- Adoptar el patrón de OneFootball: la card entera con un fondo levemente más oscuro que el de la página, escudos centrados verticalmente con los nombres.

**`Tabla.tsx`**:
- Escudo circular chico (20-24px) antes del nombre de equipo, como Sofascore.
- Mantener los chips de forma (ya implementados), pero considerar agrandarlos levemente y agregar tooltip con la fecha del resultado (mejora menor, no crítica).
- Evaluar mostrar grupos cuando la competición los tiene (Libertadores) — hoy el diseño asume una tabla plana única; si en el futuro mostramos standings de copas, necesita un layout de "N mini-tablas" como Sofascore, no la tabla actual.

**`Equipos.tsx`** (grid):
- Escudo real (40-56px) en vez de la card de solo texto actual.
- Si se implementa el conteo de títulos (fuera de alcance de API-Football, requeriría data manual) — **no lo recomiendo ahora**, es esfuerzo de mantenimiento manual sin fuente de datos automática. Mencionarlo como descartado, no como pendiente.

**`Equipo.tsx`** (perfil):
- Header rediseñado al estilo OneFootball/Sofascore: escudo grande (64-80px) + nombre en Archivo Black grande + competición debajo en texto chico mutado.
- Mantener los stat-cards actuales (ya tienen buen contraste visual con el verde de acento), pero agregar escudo a cada partido de "Resultados recientes" vía `PartidoCard` ya actualizada (no requiere trabajo extra si `PartidoCard` se actualiza primero).

**`Partido.tsx`** (detalle):
- Header con ambos escudos grandes a los costados del marcador (patrón idéntico a Promiedos/Sofascore/OneFootball — las 3 lo hacen igual, es el estándar de facto).
- Estadísticas: evolucionar la comparación lado-a-lado de hoy a **barras horizontales proporcionales** (estilo Sofascore) — mismo dato, mejor lectura visual. Esto es CSS + un cálculo simple de porcentaje por stat (cuando ambos valores son numéricos; los que no lo son, como posesión ya viene en %, quedan como están).
- Eventos: adoptar el patrón de columna doble por equipo (estilo Promiedos) en vez de la lista única actual — local a la izquierda, visitante a la derecha, minuto al centro.

**Tipografía y jerarquía (global, `App.css`)**:
- Subir el tamaño de `h1` específicamente para nombres de equipo/competición en headers de página (no para los `<h1>` genéricos como "Próximos partidos") — puede necesitar una clase nueva `.titulo-hero` en vez de reusar `h1` para todo.
- Mantener Inter para texto de cuerpo (ya está bien, es legible y no compite con Archivo Black).

### 3.4 Qué NO traer de estas referencias (fuera de alcance, justificación)

- Cuotas/casas de apuestas (Sofascore, Promiedos, ElNine) — no es el objetivo de BalonPie, y agregarlo requeriría otro proveedor de datos.
- Noticias/feed editorial (OneFootball) — BalonPie es un dashboard de datos, no un medio.
- Mapa de disparos, lineups en cancha, "impulso de ataque" (Sofascore) — requieren datos que el plan Free no expone con el detalle necesario (coordenadas de tiro, posición de jugadores).
- Video de highlights embebido (Promiedos, OneFootball) — requeriría otro proveedor (YouTube/Opta), fuera del alcance de API-Football.

---

## 4. Orden de implementación sugerido

Ordenado por dependencia real (no solo prioridad), con complejidad estimada (S=simple/pocas horas, M=medio/medio día, L=grande/requiere decisiones de diseño primero).

| # | Tarea | Complejidad | Por qué este orden |
|---|---|---|---|
| 1 | Decidir el enfoque de `/proximos-partidos` (sección 2.3, opción a/b/c) | — (decisión, no código) | Bloquea todo lo demás del backend de fixtures; sin esto no se puede tocar `main.py` con criterio. |
| 2 | Agregar `escudo`/`logo_url` end-to-end (2.4) | S | Independiente de todo, alto impacto visual inmediato, no requiere decisiones pendientes. Buen primer commit. |
| 3 | Expandir `teams.py` a las 4 competiciones vía `/teams` (2.2) | M | Requiere el cambio de modelo (`liga_id` → `liga_ids`), pero no depende de la decisión del punto 1. Habilita perfiles de más equipos para probar el resto. |
| 4 | Reemplazar `get_last_fixtures`/`resultados_recientes` por `round` o `from`/`to` (2.3, última-fecha) | M | Depende de tener más equipos (punto 3) para que valga la pena probarlo con variedad. |
| 5 | Implementar la decisión del punto 1 para `/proximos-partidos` | M-L | Ya con datos de fechas reales (punto 4) es más fácil reusar la misma lógica de `round`/`from-to`. |
| 6 | Rediseño visual: `PartidoCard` + escudos en `Tabla`/`Equipos`/`Equipo` (3.3) | M | Depende del punto 2 (escudos ya en la API) — sin eso es solo CSS sin datos que mostrar. |
| 7 | Rediseño de `Partido.tsx`: barras de stats + eventos en 2 columnas (3.3) | M | Independiente de los datos nuevos, solo necesita lo que ya existe hoy — se puede hacer en paralelo al punto 6 si hay dos personas, o después si es una sola. |
| 8 | Selector de season 2022/2023/2024 (2.1) | M | Última porque es la de menor valor relativo (lo marqué como "a decidir" en 2.1) — no bloquea nada y se puede descartar sin costo. |
| 9 | Standings de copas (grupos de Libertadores) si se decide mostrar (1.5, 3.3) | L | Requiere layout nuevo (N mini-tablas), y depende de si realmente se quiere ese alcance — lo dejaría para una iteración separada, no en este batch. |

**Mi recomendación de corte para un primer batch:** puntos 1 (decisión) + 2 + 3 + 4 + 6. Eso ya resuelve "los datos no están" y "se ve genérico" sin meterse todavía en el problema sin solución limpia de "próximos partidos" (punto 5) ni en el layout de grupos de copas (punto 9), que son los dos de mayor incertidumbre de diseño.
