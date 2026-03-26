import React, { useMemo, useState } from "react";
import Login from "./pages/Login.jsx";
import Members from "./pages/Members.jsx";
import MemberDetail from "./pages/MemberDetail.jsx";
import Orders from "./pages/Orders.jsx";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000/api";

function Nav({setPage,role,onLogout}){
  return (
    <div style={{display:"flex",gap:10,alignItems:"center",padding:"10px 12px",borderBottom:"1px solid #eee"}}>
      <strong style={{letterSpacing:2}}>WOW ADMIN</strong>
      <button onClick={()=>setPage("members")}>Miembros</button>
      <button onClick={()=>setPage("orders")}>Pedidos</button>
      <div style={{marginLeft:"auto",display:"flex",gap:10,alignItems:"center"}}>
        <span style={{color:"#666"}}>{role}</span>
        <button onClick={onLogout}>Salir</button>
      </div>
    </div>
  );
}

export default function App(){
  const [token,setToken] = useState(localStorage.getItem("token")||"");
  const [role,setRole] = useState(localStorage.getItem("role")||"");
  const [page,setPage] = useState("members");
  const [selectedId,setSelectedId] = useState(null);

  const api = useMemo(()=> (path, opts={}) => fetch(API_BASE+path, {
      ...opts,
      headers: { "Content-Type":"application/json", ...(opts.headers||{}), ...(token?{"Authorization":"Bearer "+token}:{}) }
    }), [token]);

  const logout = ()=>{ localStorage.clear(); setToken(""); setRole(""); };

  if(!token) return <Login apiBase={API_BASE} onLogin={(t,r)=>{setToken(t);setRole(r);localStorage.setItem("token",t);localStorage.setItem("role",r);}} />;

  return (
    <div>
      <Nav setPage={(p)=>{setPage(p); if(p!=="member") setSelectedId(null);}} role={role} onLogout={logout} />
      {page==="members" && <Members api={api} onOpen={(id)=>{setSelectedId(id); setPage("member");}} />}
      {page==="member" && selectedId && <MemberDetail api={api} id={selectedId} apiBase={API_BASE} onBack={()=>setPage("members")} />}
      {page==="orders" && <Orders api={api} />}
      <div style={{padding:12,color:"#888",fontSize:12}}>MVP · 返现按 <b>实付金额</b> · Promo: 100€ + 10€</div>
    </div>
  );
}
