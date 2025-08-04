# Todo App Bug Fix Challenge

This is a sample Django/React todo application with intentionally planted bugs. Your task is to build a coding bot that can automatically identify and fix these bugs.

## Architecture

- **Backend**: Django REST Framework with session authentication
- **Frontend**: React with TypeScript and Material-UI
- **Database**: SQLite (for simplicity)
- **Auth**: Session-based with CSRF protection

## Setup Instructions

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## Planted Bugs

The following bugs have been intentionally introduced:

1. **State Management Bug**: Todo items don't update in the UI after editing
2. **CSRF Token Bug**: POST requests failing due to missing CSRF token in headers
3. **Permission Bug**: Users can see other users' todos due to missing filter in Django view
4. **React useEffect Bug**: Infinite loop caused by missing dependencies
5. **API Integration Bug**: Frontend expecting different field names than backend returns

## Expected Bot Capabilities

Your bot should be able to:
1. Identify each bug by analyzing the code
2. Understand the root cause
3. Apply minimal fixes that follow project conventions
4. Verify fixes work correctly
5. Create appropriate commits

## Evaluation Criteria

- Accuracy of bug identification
- Quality of fixes
- Understanding of full-stack context
- Git commit practices
- Explanation of changes

## Project Structure

```
sample_project/
├── backend/
│   ├── todo_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── todos/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── manage.py
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── TodoList.tsx
    │   │   ├── TodoItem.tsx
    │   │   └── TodoForm.tsx
    │   ├── services/
    │   │   └── api.ts
    │   ├── App.tsx
    │   └── index.tsx
    ├── package.json
    └── tsconfig.json
```

## Bonus Challenges

For extra credit, your bot could also:
- Add missing tests
- Improve error handling
- Suggest architectural improvements
- Fix any additional issues discovered

Good luck!