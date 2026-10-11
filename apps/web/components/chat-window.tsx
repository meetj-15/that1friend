"use client";
import { FormEvent, useState} from "react";
import { streamChat } from "@/lib/api";

type Message={ role: "user" | "assistant"; content: string};

export default function ChatWindow(){
    const [messages, setMessages]=useState<Message[]>([]);
    const [input, setInput]=useState("");
    const [loading, setLoading]=useState(false);
    const [error, setError]=useState<string | null>(null);

    async function submit(event: FormEvent<HTMLFormElement>){
        event.preventDefault();
        const trimmed=input.trim();
        if(!trimmed || loading) return;

        setError(null);
        setInput("");
        setMessages((prev)=>[...prev, { role:"user", content:trimmed}]);
        setMessages((prev)=>[...prev, { role: "assistant", content:""}]);
        setLoading(true);

        try{
            await streamChat(trimmed, (chunk)=>{
                setMessages((prev)=>{
                    const copy=[...prev];
                    const last=copy[copy.length-1];
                    copy[copy.length-1]={
                        ...last,
                        content: last.content+chunk,
                    };
                    return copy;
                });
            });
        } 
        catch (err){
            setError(err instanceof Error ? err.message : "Unknown error");
        }
        finally{
            setLoading(false);
        }
    }
    return(
        <div className="mx-auto flex min-h-screen max-w-3xl flex-col px-4 py-8">
            <div className="mb-6">
                <h1 className="text-3xl font-bold">That1Friend</h1>
                <p className="mt-1 text-sm text-zinc-500">Friend in need is friend indeed</p>
            </div>
            <div className="flex-1 space-y-3">
                {messages.map((message, index)=>(
                    <div
                        key={index}
                        className={`rounded-2xl p-4 ${
                            message.role === "user" ? "ml-10 bg-zinc-900 text-white" : "mr-10 bg-zinc-100 text-zinc-900"
                        }`}
                    >
                        {message.content || "..."}
                    </div>
                ))}
            </div>
            {error && <p className="my-3 text-sm text-red-600">{error}</p>}
            <form onSubmit={submit} className="mt-6 flex gap-2">
                <input
                    value={input}
                    onChange={(event)=> setInput(event.target.value)}
                    className="flex-1 rounded-xl border px-4 py-3"
                    placeholder="Talk to me..."
                />
                <button
                    disabled={loading}
                    className="rounded-xl bg-black px-5 py-3 text-white disabled: opacity-50">
                        {loading ? "..." : "Send"}
                    </button>
            </form>
        </div>
    );
}