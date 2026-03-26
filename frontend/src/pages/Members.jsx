import React, { useEffect, useState } from "react";
export default function Members({api,onOpen}){
  const [q,setQ] = useState("");
  const [items,setItems] = useState([]);
  const [err,setErr] = useState("");
  const [form,setForm] = useState({phone:"",email:"",name:"",ref_code:""});

  async function load(){
    setErr("");
    const res = await api("/members?q="+encodeURIComponent(q||""));
    if(!res.ok){ setErr("Error cargando miembros"); return; }
    const data = await res.json();
    setItems(data.items||[]);
  }
  useEffect(()=>{ load(); }, []);

  async function createMember(e){
    e.preventDefault();
    setErr("");
    const payload = {...form};
    if(!payload.phone) delete payload.phone;
    if(!payload.email) delete payload.email;
    if(!payload.name) delete payload.name;
    if(!payload.ref_code) delete payload.ref_code;

    const res = await api("/members", {method:"POST", body: JSON.stringify(payload)});
    if(!res.ok){ setErr("No se pudo crear"); return; }
    setForm({phone:"",email:"",name:"",ref_code:""});
    await load();
  }

  return (
    <div style={{padding:12}}>
      <div style={{display:"flex",gap:10,flexWrap:"wrap",alignItems:"center"}}>
        <input value={q} onChange={e=>setQ(e.target.value)} placeholder="Buscar (tel/email/nombre/ref)" style={{padding:10,border:"1px solid #ddd",borderRadius:10,minWidth:260}} />
        <button onClick={load}>Buscar</button>
      </div>

      <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:14,marginTop:14}}>
        <div style={{border:"1px solid #eee",borderRadius:14,padding:12}}>
          <h3 style={{marginTop:0}}>Nuevo socio</h3>
          <form onSubmit={createMember}>
            <input value={form.phone} onChange={e=>setForm({...form,phone:e.target.value})} placeholder="Teléfono (opcional)" style={{width:"100%",padding:10,border:"1px solid #ddd",borderRadius:10,margin:"6px 0"}} />
            <input value={form.email} onChange={e=>setForm({...form,email:e.target.value})} placeholder="Email (opcional)" style={{width:"100%",padding:10,border:"1px solid #ddd",borderRadius:10,margin:"6px 0"}} />
            <input value={form.name} onChange={e=>setForm({...form,name:e.target.value})} placeholder="Nombre (opcional)" style={{width:"100%",padding:10,border:"1px solid #ddd",borderRadius:10,margin:"6px 0"}} />
            <input value={form.ref_code} onChange={e=>setForm({...form,ref_code:e.target.value})} placeholder="Código recomendación (opcional)" style={{width:"100%",padding:10,border:"1px solid #ddd",borderRadius:10,margin:"6px 0"}} />
            <button style={{padding:"10px 12px"}}>Crear</button>
          </form>
          {err && <div style={{color:"#b91c1c",marginTop:8}}>{err}</div>}
        </div>

        <div style={{border:"1px solid #eee",borderRadius:14,padding:12}}>
          <h3 style={{marginTop:0}}>Lista (máx 50)</h3>
          <div style={{maxHeight:420,overflow:"auto"}}>
            {items.map(m=>(
              <div key={m.id} style={{display:"flex",gap:10,alignItems:"center",padding:"8px 0",borderBottom:"1px dashed #eee"}}>
                <div style={{flex:1}}>
                  <div><b>#{m.id}</b> {m.name||""}</div>
                  <div style={{color:"#666",fontSize:12}}>{m.phone||""} {m.email||""} · Ref:{m.ref_code}</div>
                </div>
                <div style={{fontSize:12}}>€{Number(m.wallet_recharge_balance).toFixed(2)} / €{Number(m.wallet_referral_balance).toFixed(2)}</div>
                <button onClick={()=>onOpen(m.id)}>Abrir</button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
