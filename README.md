# HuggingFace-Space-Qwen2-1.5B-REST-API-FastAPI-


Upload file `app.py` dan `requirements.txt` ke repository Space baru pada HuggingFace.


## Cara deploy
1. Buat Space baru: pilih `Compute: CPU` (atau GPU jika tersedia)
2. Upload `app.py` dan `requirements.txt`.
3. (Opsional) Set `MODEL_ID` di Environment Variables jika mau ganti model.


Contoh panggilan dari website (frontend):


```js
async function askAI(msg){
const res = await fetch('https://<your-space-name>.hf.space/chat', {
method: 'POST',
headers: {'Content-Type':'application/json'},
body: JSON.stringify({message: msg})
});
const data = await res.json();
return data.reply;
}
