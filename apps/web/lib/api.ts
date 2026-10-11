const API_BASE_URL=process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";
export async function sendChat(content: string): Promise<string>{
    const response=await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({content}),
    });

    if(!response.ok){
        throw new Error(`API error: ${response.status}`);
    }
    const data=(await response.json()) as { content: string };
    return data.content;
}

export async function streamChat(
    content: string, 
    onChunk: (chunk:string)=> void,
): Promise<void>{
    const response=await fetch(`${API_BASE_URL}/chat/stream`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ content }),
    });
    if(!response.ok || !response.body){
        throw new Error(`Streaming API Error: ${response.status}`);
    }
    const reader=response.body.getReader();
    const decoder=new TextDecoder();
    let buffer="";
    while(true){
        const {done, value}=await reader.read();
        if(done) break;
        buffer+=decoder.decode(value, { stream:true});
        const events=buffer.split("\n\n");
        buffer=events.pop() ?? "";
        for (const event of events){
            const line=event.split("\n").find((x)=>x.startsWith("data: "));
            if(!line)continue;
            const payload=line.slice(6);
            if(payload==="[DONE]")return;
            const parsed=JSON.parse(payload) as {content:string};
            onChunk(parsed.content);
        }
    }
}