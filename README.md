
```markdown
# **Smart Task Analyzer**
📌 *Django + DRF Project for Singularium Internship Assignment*

A priority-scoring task analysis tool built with **Django**, **Django REST Framework**, and a simple **HTML/CSS/JS** frontend.  
It evaluates tasks using urgency, importance, effort, and dependency factors.

---

## 🚀 **Features**

### 🔹 **Backend (Django + DRF)**
Task model includes:
- `title`
- `due_date`
- `estimated_hours`
- `importance` (1–10)
- `dependencies` (JSON list of task IDs)

Smart scoring algorithm uses:
- **Urgency**  
- **Importance**  
- **Effort (1 / hours)**  
- **Dependency penalties**

APIs:
- **POST** `/api/tasks/analyze/` → Returns scored tasks  
- **GET** `/api/tasks/suggest/` → Returns top 3 tasks with explanations  

Additional features:
- Circular dependency detection  
- Edge-case handling  
- 5+ automated unit tests  

---

### 🔹 **Frontend (HTML/CSS/JS)**
- Form to create tasks  
- Bulk JSON input  
- Analyze button  
- Sorting modes:
  - Smart Balance  
  - Fastest Wins  
  - High Impact  
  - Deadline Driven  
- Priority color coding:
  - 🟩 High  
  - 🟨 Medium  
  - 🟥 Low  
- Results table  
- Suggestions display area  

---

## 📦 **Project Structure**
```

smartanalyzer/
tasks/
models.py
serializers.py
views.py
utils.py
tests.py
templates/tasks/index.html
manage.py
requirements.txt
README.md

````

---

## 🛠 **Installation & Setup**

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/smart-task-analyzer.git
cd smart-task-analyzer
````

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
```

### 3️⃣ Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run migrations

```bash
python manage.py migrate
```

### 6️⃣ Start development server

```bash
python manage.py runserver
```

Visit:
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🧪 **Running Tests**

```bash
python manage.py test
```

Expected output:

```
Found 5 tests.
.....
OK
```

---

## 📡 **API Documentation**

### 🔵 **POST /api/tasks/analyze/**

Analyzes tasks and returns a sorted list with scores.

#### Example Request:

```json
[
  {
    "title": "Finish report",
    "due_date": "2030-01-01T10:00",
    "estimated_hours": 3,
    "importance": 9,
    "dependencies": []
  }
]
```

Returns:

* Score
* Explanation
* All task fields
* Sorted by score descending

---

### 🟢 **GET /api/tasks/suggest/**

Returns **top 3 tasks** + explanations.

Requires:

* `/api/tasks/analyze/` must be called first.

---

## 🧠 **Algorithm Explanation (350–400 words)**

The Smart Task Analyzer uses a balanced, weighted scoring system designed to simulate human-like prioritization of tasks. The goal of the algorithm is to consider multiple dimensions of a task—urgency, importance, effort, and dependencies—and convert them into a single priority score. This creates a consistent, explainable prioritization that works across different task types.

The first major factor is **urgency**, determined by the number of days until the due date. Tasks that are overdue or due today receive the highest urgency score (10/10). Tasks due within one day still get high urgency (9/10), and tasks due within a week gradually decrease from 9 down to a minimum of 5. Anything due further than a week is treated as low urgency (around 3/10). This ensures that deadlines matter, but long-term tasks are not completely ignored.

The next factor is **importance**, which is provided directly by the user on a scale of 1–10. This allows the user to express how meaningful or impactful a task is, separate from its due date. The algorithm gives importance a strong weight so that high-impact tasks do not get overshadowed by minor but urgent tasks.

**Effort** is computed as an inverse function of estimated_hours. A shorter task increases the overall priority, because “quick wins” help maintain productivity. To keep values balanced, the effort bonus is capped at 10 and scaled appropriately.

Lastly, the algorithm applies a **dependency penalty**. Tasks that depend on other incomplete items naturally have lower immediate priority. Each dependency subtracts from the score, while circular dependencies (a task depending on itself) receive a heavier penalty.

Final score formula:

```
score = (urgency * 0.4) +
        (importance * 0.4) +
        (effort * 0.2) -
        (dependency_penalty)
```

This ensures urgency and importance dominate, effort boosts productivity, and dependencies reduce priority. The output includes both the numeric score and a human-readable explanation.

---

## ⚙️ **Design Decisions**

* DRF for clean input validation
* Timezone-aware date handling
* Simple frontend (no frameworks)
* Color-coded priority levels
* Database reset on analyze → clean suggest logic
* Unit tests protect scoring integrity
