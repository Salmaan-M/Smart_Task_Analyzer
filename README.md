# Smart Task Analyzer
📌 Smart Task Analyzer — Django Project

A priority-scoring task analysis tool built for the Singularium Internship Assignment.
Backend powered by Django + Django REST Framework, frontend built using HTML/CSS/JS.

🚀 Features
🔹 Backend (Django + DRF)

Task model with:

Title

Due date

Estimated hours

Importance (1–10)

Dependencies (list of task IDs, JSONField)

Smart scoring algorithm that considers:

Urgency

Importance

Effort (1 / estimated_hours)

Dependency penalties

Fully working APIs:

POST /api/tasks/analyze/ → Returns scored tasks

GET /api/tasks/suggest/ → Returns top 3 recommended tasks with explanations

Circular dependency detection

Edge-case handling

5+ automated unit tests

🔹 Frontend (HTML/CSS/JS)

Form for creating tasks

Bulk JSON input

“Analyze” button

Sorting modes:

Smart Balance

Fastest Wins

High Impact

Deadline Driven

Priority color coding:

🟩 High

🟨 Medium

🟥 Low

Table rendering with task details

Suggestions section displaying explanations

📦 Project Structure
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

🛠 Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/yourusername/smart-task-analyzer.git
cd smart-task-analyzer

2️⃣ Create a virtual environment
python -m venv venv

3️⃣ Activate the virtual environment

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate

4️⃣ Install dependencies
pip install -r requirements.txt

5️⃣ Run migrations
python manage.py migrate

6️⃣ Start development server
python manage.py runserver


Then visit:

👉 http://127.0.0.1:8000/

🧪 Running Tests
python manage.py test


You should see something like:

Found 5 tests.
.....
OK

📡 API Documentation
🔵 POST /api/tasks/analyze/

Analyzes tasks and returns a sorted list with smart priority scores.

Example Request:
[
  {
    "title": "Finish report",
    "due_date": "2030-01-01T10:00",
    "estimated_hours": 3,
    "importance": 9,
    "dependencies": []
  }
]

Returns:

Score

Explanation

All task fields

Sorted descending by score

🟢 GET /api/tasks/suggest/

Returns top 3 tasks + explanations.

Requires that /api/tasks/analyze/ has been called first.

🧠 Algorithm Explanation (Approx. 350–400 words)

The Smart Task Analyzer uses a balanced, weighted scoring system designed to simulate human-like prioritization of tasks. The goal of the algorithm is to consider multiple dimensions of a task—urgency, importance, effort, and dependencies—and convert them into a single priority score. This creates a consistent, explainable prioritization that works across different task types.

The first major factor is urgency, determined by the number of days until the due date. Tasks that are overdue or due today receive the highest urgency score (10/10). Tasks due within one day still get high urgency (9/10), and tasks due within a week gradually decrease from 9 down to a minimum of 5. Anything due further than a week is treated as low urgency (around 3/10). This ensures that deadlines matter, but long-term tasks are not completely ignored.

The next factor is importance, which is provided directly by the user on a scale of 1–10. This allows the user to express how meaningful or impactful a task is, separate from its due date. The algorithm gives importance a strong weight so that high-impact tasks do not get overshadowed by minor but urgent tasks.

Effort is computed as an inverse function of estimated_hours. A shorter task increases the overall priority, because "quick wins" help maintain productivity momentum. To keep values manageable, the effort bonus is capped at 10 and scaled appropriately.

Finally, the algorithm implements a dependency penalty. Tasks that depend on other incomplete items naturally have lower immediate priority, since they cannot be started right away. Each dependency subtracts from the score, and a circular dependency (a task depending on itself) results in an even larger penalty.

The final score is a weighted combination of these factors:

score = (urgency * 0.4) +
        (importance * 0.4) +
        (effort * 0.2) -
        (dependency_penalty)


This weighting ensures balance: urgency and importance dominate, effort provides a boost, and dependencies reduce priority. The output includes both the score and a human-readable explanation describing how the score was formed.

⚙️ Design Decisions

DRF used for APIs → clean input validation + serializer consistency

Timezone-aware calculations → avoids naive-vs-aware errors

Frontend kept minimal → internship-friendly, readable HTML/JS

Color-coded priorities → visually intuitive scoring

Delete-and-recreate on analyze → simplifies suggest endpoint

Unit tests → ensure scoring stays correct as code evolves
