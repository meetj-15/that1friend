"use client"
import {createClient} from "@/lib/supabase/client";
export default function LoginPage(){
    async function loginWithGoogle(){
        const supabase=createClient();
        await supabase.auth.signInWithOAuth({
            provider: "google",
            options:{
                redirectTo: `${window.location.origin}/auth/callback`,
            },
        });
    }
    return(
        <main className="flkex min=h-screen items-center justify-center">
            <div className="w-full max-w-sm rounded-2xl border p-8">
                <h1 className="text-2xl font-bold">Sign in</h1>
                <button
                    onClick={loginWithGoogle}
                    className="mt-6 w-full rounded-xl bg-black px-4 py-3 text-white">Continue with Google</button>
            </div>
        </main>
    );
}