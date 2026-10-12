create table if not exists public.memories (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id) on delete cascade,
    type text not null,
    content text not null,
    importance numeric not null default 0.5,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists public.running_jokes (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id) on delete cascade,
    description text not null,
    strength numeric not null default 0.5,
    last_used_at timestamptz
);

alter table public.memories enable row level security;
alter table public.running_jokes enable row level security;

create policy "memory owner" on public.memories
for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy "running joke owner" on public.running_jokes
for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
