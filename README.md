# KLL FindIt AI

lost-and-found matching for KLL (CSE 103 Intelligent System).

## Run it

```
cd C:\dev\findit-ai
venv\Scripts\activate
python app.py
```

Open http://127.0.0.1:5000 in your browser. Optional sample data: `python seed_data.py`.

## Files and who works on them

| File                             | What it does                                       | Suggested owner        |
| -------------------------------- | -------------------------------------------------- | ---------------------- |
| `db.py`                          | SQLite tables and queries                          | Backend coder          |
| `app.py`                         | Routes (pages and forms)                           | Backend coder          |
| `matching.py`                    | Attribute score + TF-IDF text similarity + ranking | Matching coder         |
| `templates/`, `static/style.css` | Pages and look                                     | Interface coder        |
| `evaluate.py`, `data/*.csv`      | Accuracy tests (top-1 / top-3, three methods)      | Testing coder          |
| `config.py`                      | Categories, colors, rooms, weights                 | Everyone (small edits) |

## Still to build (ideas)

- Login for staff (hide the claim form and private details from the public)
- Dashboard (counts, frequent loss locations, Chart.js)
- CSV export
- Holding-period reminders for unclaimed items
- Feedback buttons (Correct / Incorrect) that adjust the weights
