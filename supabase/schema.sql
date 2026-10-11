create extension if not exists pgcrypto;

create table if not exists public.profiles(
    id uuid primary key refrences auth.users(id) on delete cascade,
    display_name text, 
    avatar_url text, 
    created_at timestampz not null default now() 
);

create table if not exists public.preferences(
    user_id uuid primary key references auth.users(id) on delete cascade,
    region text not null default 'neutral',
    dialect_intensity numeric not null default 0.4,
    language_mode text not null default 'auto',
    humor_level numeric not null default 0.7,
    sarcasm_level numeric not null default 0.5
    memory_enabled boolean not null default true
);

create table if not exists public.conversations(
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id) on delete cascade,
    title text not null default 'New Convo',
    active_task jsonb,
    created_at timestampz not null default now()
    updated_at timesatampz not null default now()
);

create table if not exists public.messages(
    id uuid primary key default gen_random_uuid(),
    conversation_id uuid not null references public.conversations(id) on delete cascade,
    role text not null check(role in ('user', 'assistant', 'system')),
    content text not null,
    created_at timestampz not null default now()
);

create index if not exists conversations_user_id_idx on public.conversations(user_id);
create index if not exists messages_conversation_id_idx on public.messages(conversation_id, created_at);

alter table public.profiles enable row level security;
alter table public.preferences enable row level security;
alter table public.conversations enable row level security;
alter table public.messages enable row level security;

create policy "profiles owner read" on public.profiles for select using (auth.uid()=id);
create policy "profiles owner update" on public.profiles for update using (auth.uid()=id);
create policy "preferences owner read" on public.preferences for select using (auth.uid()=user_id);
create policy "preferences owner write" on public.preferences for all using (auth.uid()=user_id) with check(auth.uid()=user_id);
create policy "conversation owner read" on public.conversations for select using (auth.uid()=user_id);
create policy "conversation owner write" on public.conversations for all using (auth.uid()=user_id) with check (auth.uid()=user_id);
create policy "message owner read" on public.messages for select using (exists(select 1 from public.conversations c where c.id=conversation_id and c.user-id=auth.id()));
create policy "messages owner write" on public.messages for all using(exists(select 1 from public.conversations c where c.id=conversation_id and c.user_id=auth.uid()))with check (exiats(select 1 from public.conversations c where c.id=conversation_id and c.user_id=auth.uid())); 