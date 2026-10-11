import {createClient} from "@/lib/supabase/server";

export default async function SettingsPage(){
    const supabase=await createClient();
    const {data}=await supabase.auth.getUser();
    return(
        <main className="mx-auto max-w-2xl px-6 py-12">
            <h1 className="text-3xl font-bold">Settings</h1>
            <p className="mt-3 text-zinc-600">Signed in as {data.user?.email ?? "unknown user"}.</p>
            <form action="/logout" method="post" className="mt-6">
                <button className="rounded-xl bg-black px-4 py-2 text-white">Sign Out</button>
            </form>
        </main>
    );
}