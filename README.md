# 🧠 AI-Powered Adaptive Math Learning Prototype (Streamlit)

An **AI-powered adaptive learning system** that helps children (ages 5–10) practice **basic math skills** (addition, subtraction, multiplication, and division).  
The app dynamically adjusts the **difficulty** of math puzzles based on learner performance using a **machine learning model (Decision Tree Classifier)**.

---

## 🚀 Features

- 🎯 **Adaptive Difficulty:** Automatically adjusts question difficulty (Easy / Medium / Hard) based on accuracy and response time.  
- 🧩 **Dynamic Puzzle Generator:** Generates new math problems for each difficulty level.  
- ⏱️ **Performance Tracking:** Records correctness, time taken, and progression.  
- 📊 **Visual Dashboard:** Real-time charts for accuracy, response time, and difficulty transitions.  
- 🤖 **ML-Based Adaptive Engine:** Uses a trained Decision Tree model with self-retraining using user performance.  
- 💾 **Data Logging:** Saves learner sessions as CSV files for analysis.

---

## 🗂️ Project Structure

```
math-adaptive-streamlit/
├── app.py                     # Streamlit main app
├── requirements.txt            # Required libraries
├── README.md                   # Project documentation
└── src/
    ├── adaptive_engine_ml.py   # ML-based adaptive logic
    ├── puzzle_generator.py     # Math puzzle generator
    ├── tracker.py              # Performance tracker
    └── progress_summary.py     # Summary + analytics
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/math-adaptive-streamlit.git
cd math-adaptive-streamlit
```

### 2️⃣ Install Requirements
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the App Locally
```bash
streamlit run app.py
```

Then open your browser and go to 👉 `http://localhost:8501`

---

## 🧮 How It Works

1. User enters their **name** and chooses an initial difficulty level.  
2. The system presents math puzzles one by one.  
3. After each response:
   - Correctness ✅ or ❌ is recorded.
   - Response time ⏱️ is measured.
   - The ML model predicts the next optimal difficulty.
4. At the end of the session:
   - A **summary dashboard** shows:
     - Accuracy trend  
     - Response time trend  
     - Difficulty transition  
   - Results are saved in a `.csv` file.

---

## 🧠 Adaptive Engine (ML Model)

The adaptive logic uses:
- **Features:**
  - Current level (Easy/Medium/Hard)
  - Number of correct answers in recent attempts
  - Average response time
  - Last attempt correctness
- **Model:** Decision Tree Classifier  
- **Training:** Bootstrapped with simulated data + self-retraining after every few attempts.

---

## 📈 Example Dashboard

- Accuracy (%) vs Attempt  
- Response Time (s) per Attempt  
- Difficulty Level Transitions  

These charts visualize learning progress and engagement in real-time.

---

## ☁️ Deployment (Streamlit Cloud)

1. Push this project to a GitHub repository.  
2. Go to [https://share.streamlit.io](https://share.streamlit.io).  
3. Click **“New app”** → Select your GitHub repo.  
4. Set the file path to `app.py`.  
5. Click **Deploy** 🎉  

You’ll get a live URL like:  
👉 `https://yourname-math-adaptive.streamlit.app`

---

## 📄 License
This project is open-source under the **MIT License**.  
You can modify and use it for educational or research purposes.




