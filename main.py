from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# NOTE: absolute imports (no leading dot) because we run "python -m uvicorn main:app"
from models.pose_trainer import analyze_squat
from models.dietician import generate_diet_plan
from models.habit_tracker import log_workout_entry, get_summary, predict_skip_risk
from models.chat_buddy import reply_to_user

app = FastAPI(title="AI Gym & Fitness Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class DietRequest(BaseModel):
    weight_kg: float
    height_cm: float
    age: int
    goal: str
    preference: str

class HabitLog(BaseModel):
    did_workout: bool
    mood: str

class Chat(BaseModel):
    message: str

@app.post("/workout/analyze")
async def workout_analyze(file: UploadFile = File(...)):
    img_bytes = await file.read()
    return analyze_squat(img_bytes)

@app.post("/diet/plan")
def diet(req: DietRequest):
    return generate_diet_plan(
        req.weight_kg,
        req.height_cm,
        req.age,
        req.goal,
        req.preference,
    )

@app.post("/habit/log")
def habit(req: HabitLog):
    return log_workout_entry(req.did_workout, req.mood)

@app.get("/habit/summary")
def habit_sum():
    return get_summary()

@app.get("/habit/predict")
def habit_predict():
    return predict_skip_risk()

@app.post("/chat")
def chat(req: Chat):
    return reply_to_user(req.message)

@app.get("/")
def root():
    return {"status": "Backend running!"}
