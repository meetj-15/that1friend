import ChatWindow from "@/components/chat-window";
import {redirect} from "next/navigation";
import {createClient} from "@/lib/supabase/server";
export default async function ChatPage(){
    const supabase=await createClient();
    const {data}=await supabase.auth.getUser();
    if(!data.user){
        redirect("/login");
    }
    return <ChatWindow />;
}