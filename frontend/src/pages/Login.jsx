import React, { useState } from "react";
export default function Login({apiBase,onLogin}){
  const [username,setUsername] = useState("");
  const [password,setPassword] = useState("");
  const [err,setErr] = useState("");

  async function submit(e){
    e.preventDefault();
    setErr("");
    const res = await fetch(apiBase+"/auth/login", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({username,password})});
    if(!res.ok){ setErr("Usuario o contraseña incorrectos"); return; }
    const data = await res.json();
    onLogin(data.access_token, data.role);
  }

  return (
    <div style={{maxWidth:420,margin:"60px auto",padding:18,border:"1px solid #eee",borderRadius:14}}>
      <h2 style={{marginTop:0}}>WOW Admin</h2>
      <form onSubmit={submit}>
        <input value={username} onChange={e=>setUsername(e.target.value)} placeholder="Usuario" style={{width:"100%",padding:12,border:"1px solid #ddd",borderRadius:10,margin:"8px 0"}} />
        <input value={password} onChange={e=>setPassword(e.target.value)} placeholder="Contraseña" type="password" style={{width:"100%",padding:12,border:"1px solid #ddd",borderRadius:10,margin:"8px 0"}} />
        <button style={{width:"100%",padding:12,borderRadius:10,border:"1px solid #111",background:"#111",color:"#fff",fontWeight:700}}>Entrar</button>
      </form>
      {err && <div style={{marginTop:10,color:"#b91c1c"}}>{err}</div>}
      <div style={{marginTop:14,fontSize:12,color:"#666"}}>owner/owner1234 · staff/staff1234</div>
    </div>
  );
}
