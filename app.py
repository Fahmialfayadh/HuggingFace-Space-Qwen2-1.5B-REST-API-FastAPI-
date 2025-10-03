# app.py
global generator
logging.info(f'Loading model: {MODEL_ID} ...')
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, trust_remote_code=True)
generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
logging.info('Model loaded. Ready to accept requests.')




class ChatRequest(BaseModel):
message: str
# optional: list of prior messages (history) if mau implement conversational context
history: list = None




@app.post('/chat')
async def chat(req: ChatRequest):
prompt = build_prompt(req.message)
# generation settings — kecil dan konservatif supaya lebih cepat
out = generator(prompt, max_new_tokens=256, do_sample=True, temperature=0.8, top_p=0.95)
text = out[0]['generated_text']
# model sering mengembalikan prompt+reply — kita crop supaya hanya bagian jawaban
reply = postprocess_generated(prompt, text)
return {'reply': reply}




# --- Helpers ---


def build_prompt(user_message: str) -> str:
# system prompt = personality default (ramah, cerdas, sedikit sarkas, sopan)
system = (
"Kamu adalah asisten AI yang ramah, cerdas, dan sedikit sarkastik namun sopan. "
"Jawab singkat, jelas, dan bantu pengguna dengan langkah praktis. "
"Jika ditanya soal kode, sertakan contoh singkat jika perlu."
)
prompt = f"System: {system}\nUser: {user_message}\nAssistant:"
return prompt




def postprocess_generated(prompt: str, generated: str) -> str:
# Jika generated_text mengandung prompt, buang bagian prompt
if generated.startswith(prompt):
return generated[len(prompt):].strip()
# fallback: kembalikan generated secara keseluruhan
return generated.strip()




# Simple health endpoint
@app.get('/')
async def root():
return {'status': 'ok', 'model': MODEL_ID}
