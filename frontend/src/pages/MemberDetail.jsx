import React, { useEffect, useState } from "react";
export default function MemberDetail({api,id,apiBase,onBack}){
  const [m,setM] = useState(null);
  const [err,setErr] = useState("");
  const [topup,setTopup] = useState("");

  async function load(){
    const res = await api("/members/"+id);
    if(!res.ok){ setErr("Error"); return; }
    setM(await res.json());
  }
  useEffect(()=>{ load(); }, [id]);

  async function doTopup(){
    setErr("");
    const amt = parseFloat(topup);
    if(!amt || amt<=0){ setErr("Importe inválido"); return; }
    const res = await api("/members/"+id+"/topup", {method:"POST", body: JSON.stringify({amount: amt})});
    if(!res.ok){ setErr("No se pudo recargar"); return; }
    setTopup(""); await load();
  }
  async function promo(){
    setErr("");
    const res = await api("/members/"+id+"/topup_promo_100_10", {method:"POST"});
    if(!res.ok){ setErr("Error promo"); return; }
    await load();
  }

  if(!m) return <div style={{padding:12}}>Cargando...</div>;
  const memberQr = apiBase + "/qr/member/" + m.public_id + ".png";
  const refQr = apiBase + "/qr/ref/" + m.ref_code + ".png";

  return (
    <div style={{padding:12}}>
      <button onClick={onBack}>← Volver</button>
      <h2>Socio #{m.id} · {m.name||""}</h2>
      <div style={{color:"#666"}}>{m.phone||""} {m.email||""} · Ref: <b>{m.ref_code}</b></div>

      <div style={{display:"flex",gap:20,flexWrap:"wrap",marginTop:10}}>
        <div style={{border:"1px solid #eee",borderRadius:14,padding:12,minWidth:280}}>
          <h3 style={{marginTop:0}}>Saldos</h3>
          <div>Recarga: <b>€{Number(m.wallet_recharge_balance).toFixed(2)}</b></div>
          <div>Recomendación: <b>€{Number(m.wallet_referral_balance).toFixed(2)}</b></div>
          <div style={{marginTop:10,display:"flex",gap:8,flexWrap:"wrap"}}>
            <input value={topup} onChange={e=>setTopup(e.target.value)} placeholder="Recarga €" style={{padding:10,border:"1px solid #ddd",borderRadius:10,width:140}} />
            <button onClick={doTopup}>Recargar</button>
            <button onClick={promo}>Promo 100+10</button>
          </div>
          {err && <div style={{color:"#b91c1c",marginTop:8}}>{err}</div>}
        </div>

        <div style={{border:"1px solid #eee",borderRadius:14,padding:12}}>
          <h3 style={{marginTop:0}}>QR socio</h3>
          <img src={memberQr} alt="qr" style={{width:260,height:"auto"}} />
        </div>

        <div style={{border:"1px solid #eee",borderRadius:14,padding:12}}>
          <h3 style={{marginTop:0}}>QR recomendación</h3>
          <img src={refQr} alt="qr" style={{width:260,height:"auto"}} />
        </div>
      </div>
    </div>
  );
}
