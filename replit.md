# چیتا نت (Chita Net)

فروشگاه VPN ایرانی با رابط کاربری فارسی — کاربران پلن‌های اینترنت مشاهده، از طریق تلگرام OTP وارد می‌شوند، و با کارت بانکی پرداخت می‌کنند.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the API server (port 5000)
- `pnpm --filter @workspace/chita-net run dev` — run the frontend (port from env)
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)

## Required env vars / secrets

- `DATABASE_URL` — Postgres connection string
- `SESSION_SECRET` — secret for express-session (set as Replit secret)
- `TELEGRAM_TOKEN` — Telegram bot token (set as Replit secret)
- `BANK_CARD` — bank card number shown on payment page
- `BANK_OWNER` — card owner name
- `ADMIN_CHAT_ID` — Telegram chat ID for admin notifications
- `ADMIN_PASSWORD` — admin password
- `BOT_TELEGRAM_LINK` — link to Telegram bot (e.g. https://t.me/ChitaSeee_bot?start=login)

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- Frontend: React + Vite (Vazirmatn font, RTL, dark navy + gold theme)
- API: Express 5
- DB: PostgreSQL + Drizzle ORM
- Auth: Telegram OTP via bot polling
- Session: express-session + connect-pg-simple
- Validation: Zod (`zod/v4`), `drizzle-zod`
- API codegen: Orval (from OpenAPI spec)

## Where things live

- `artifacts/chita-net/` — React+Vite frontend, previewPath `/`
- `artifacts/api-server/` — Express API server, paths `/api`
- `lib/db/` — Drizzle ORM schema + migrations
- `lib/api-spec/openapi.yaml` — OpenAPI spec (source of truth for API contract)
- `lib/api-client-react/` — generated React Query hooks + Zod schemas
- `lib/telegram.ts` — Telegram bot polling for OTP delivery

## Architecture decisions

- Contract-first API: OpenAPI spec → Orval codegen → React Query hooks. Never call API directly in components; always use generated hooks.
- Session stored in PostgreSQL via `connect-pg-simple` for production durability.
- Telegram OTP: user sends Telegram ID → bot sends 6-digit code → user enters code to login. No passwords stored.
- Plans are hardcoded in `artifacts/api-server/src/lib/plans.ts` (no DB table for plans).
- All UI text is Persian; layout is RTL (`dir="rtl"` on `<html>`).

## Pages

- `/` — Home: plan grid with purchase buttons
- `/login` — Two-step Telegram OTP login
- `/profile` — Protected: user info + order history + stats
- `/orders` — Protected: order list with status badges
- `/buy/:planKey` — Protected: payment page with bank card info

## User preferences

- All UI text must be in Persian (Farsi)
- Dark navy (#0a0e27) background, gold (#ffc107) accent
- Vazirmatn font, RTL layout

## Gotchas

- Run codegen after any OpenAPI spec changes: `pnpm --filter @workspace/api-spec run codegen`
- The `/api/auth/me` 401 in logs is expected for unauthenticated users — not an error.
- Telegram bot polling runs inside the API server process (lib/telegram.ts).
- Do not use `pnpm dev` at workspace root — run individual artifact workflows.
