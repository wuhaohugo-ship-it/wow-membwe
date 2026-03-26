import React, { useState } from "react";
export default function Orders({api}){
  const [form,setForm] = useState({channel:"dinein",order_no:"",amount_gross:"",amount_paid:"",member_id:"",use_wallet_referral:"0",use_wallet_recharge:"0"});
  const [out,setOut] = useState(null);
  const [err,setErr] = useState("");

  async function submit(e){
    e.preventDefault();
    setErr(""); setOut(null);
    const payload = {
      channel: form.channel,
      order_no: form.order_no || null,
      amount_gross: parseFloat(form.amount_gross||"0"),
      amount_paid: parseFloat(form.amount_paid||"0"),
      member_id: form.member_id? parseInt(form.member_id,10): null,
      use_wallet_referral: parseFloat(form.use_wallet_referral||"0"),
      use_wallet_recharge: parseFloat(form.use_wallet_recharge||"0"),
    };
    const res = await api("/orders", {method:"POST", body: JSON.stringify(payload)});
    if(!res.ok){ const t=await res.text(); setErr(t); return; }
    setOut(await res.json());
  }

  async function refund(){
    if(!out?.id) return;
    const res = await api("/orders/"+out.id+"/refund", {method:"POST", body: JSON.stringify({reason:"manual"})});
    if(!res.ok){ const t=await res.text(); setErr(t); return; }
    setOut(await res.json());
  }

  return (
    <div style={{padding:12}}>
      <h2>Registrar pedido</h2>
      <form onSubmit={submit} style={{display:"grid",gridTemplateColumns:"repeat(2, minmax(0,1fr))",gap:10,maxWidth:760}}>
        <label>Canal<br/>
          <select value={form.channel} onChange={e=>setForm({...form,channel:e.target.value})} style={{width:"100%",padding:10,border:"1px solid #ddd",borderRadius:10}}>
            <option value="dinein">dinein</option><option value="glovo">glovo</option><option value="ubereats">ubereats</option><option value="justeat">justeat</option>
          </select>
        </label>
        <label>Order No (opcional)<br/><input value={form.order_no} onChange={e=>setForm({...form,order_no:e.target.value})} style={{width:"100%",padding:10,border:"1px solid #ddd",borderRadius:10}} /></label>
        <label>Importe total<br/><input value={form.amount_gross} onChange={e=>setForm({...form,amount_gross:e.target.value})} style={{width:"100%",padding:10,border:"1px solid #ddd",borderRadius:10}} /></label>
        <label>Importe pagado (cash/card)<br/><input value={form.amount_paid} onChange={e=>setForm({...form,amount_paid:e.target.value})} style={{width:"100%",padding:10,border:"1px solid #ddd",borderRadius:10}} /></label>
        <label>Member ID (opcional)<br/><input value={form.member_id} onChange={e=>setForm({...form,member_id:e.target.value})} style={{width:"100%",padding:10,border:"1px solid #ddd",borderRadius:10}} /></label>
        <label>Usar recomendación (€)<br/><input value={form.use_wallet_referral} onChange={e=>setForm({...form,use_wallet_referral:e.target.value})} style={{width:"100%",padding:10,border:"1px solid #ddd",borderRadius:10}} /></label>
        <label>Usar recarga (€)<br/><input value={form.use_wallet_recharge} onChange={e=>setForm({...form,use_wallet_recharge:e.target.value})} style={{width:"100%",padding:10,border:"1px solid #ddd",borderRadius:10}} /></label>
        <div style={{display:"flex",gap:10,alignItems:"flex-end"}}>
          <button style={{padding:"10px 12px"}}>Guardar</button>
          {out?.id && <button type="button" onClick={refund} style={{padding:"10px 12px"}}>Refund</button>}
        </div>
      </form>
      {err && <div style={{marginTop:10,color:"#b91c1c",whiteSpace:"pre-wrap"}}>{err}</div>}
      {out && <pre style={{marginTop:12,background:"#0b1020",color:"#e5e7eb",padding:12,borderRadius:12,overflow:"auto"}}>{JSON.stringify(out,null,2)}</pre>}
    </div>
  );
}
