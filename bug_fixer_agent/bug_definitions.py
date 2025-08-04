# bug_fixer_agent/bug_definitions.py
class BugDefinitions:
    def __init__(self):
        self.planted_bugs = [
            {
                "name": "State Management Bug",
                "description": "Todo items don't update in the UI after editing. The `handleUpdate` function in `TodoList.tsx` makes an API call but never updates the local `todos` state with the returned data.",
                "files": ["frontend/src/components/TodoList.tsx"],
                "root_cause": "Missing state update after successful API call to reflect changes locally.",
                "fix_summary": "Update the local `todos` state array with the response from the `updateTodo` API call to ensure UI consistency."
            },
            {
                "name": "CSRF Token Bug", 
                "description": "POST, PUT, and DELETE requests are failing due to a missing `X-CSRFToken` header. The `apiCall` helper in `api.ts` needs to include the CSRF token for mutating requests.",
                "files": ["frontend/src/services/api.ts"],
                "root_cause": "Django's CSRF protection blocks mutating requests without the `X-CSRFToken` header, which was missing in `api.ts`.",
                "fix_summary": "In `apiCall` in `api.ts`, add the `X-CSRFToken` header for 'POST', 'PUT', and 'DELETE' methods by retrieving the token from the cookie."
            },
            {
                "name": "Permission Bug",
                "description": "Users can see todos from other users. The `get_queryset` method in the `TodoViewSet` should filter todos by the currently authenticated user.",
                "files": ["backend/todos/views.py"],
                "root_cause": "The `get_queryset` method in `TodoViewSet` was not filtering todos by the authenticated user, leading to data exposure.",
                "fix_summary": "Modify `get_queryset` in `TodoViewSet` to filter `Todo` objects by `self.request.user` to ensure users only see their own todos."
            },
            {
                "name": "React useEffect Bug",
                "description": "An infinite loop occurs in `TodoList.tsx` because the `useEffect` hook that calls `fetchTodos` is missing a dependency array, causing it to run on every component render.",
                "files": ["frontend/src/components/TodoList.tsx"],
                "root_cause": "The `useEffect` hook in `TodoList.tsx` lacked a dependency array, causing `fetchTodos` to be called on every render, leading to an infinite loop.",
                "fix_summary": "Add an empty dependency array (`[]`) to the `useEffect` hook in `TodoList.tsx` to ensure `fetchTodos` runs only once on component mount."
            },
            {
                "name": "API Integration Bug",
                "description": "Field name mismatch between frontend and backend. The Django serializer sends `completed` and `created_at`, but the React interface expects `is_completed` and `created`.",
                "files": ["backend/todos/serializers.py"],
                "root_cause": "The Django `TodoSerializer` uses field names (`completed`, `created_at`) that do not align with the field names expected by the React frontend (`is_completed`, `created`), causing integration issues.",
                "fix_summary": "In `backend/todos/serializers.py`, map the backend fields `completed` and `created_at` to `is_completed` and `created` respectively, using `serializers.BooleanField(source='completed')` and `serializers.DateTimeField(source='created_at')` in `TodoSerializer`."
            }
        ]

    def get_bug_by_name(self, bug_name):
        for bug in self.planted_bugs:
            if bug["name"] == bug_name:
                return bug
        return None

    def get_all_bugs(self):
        return self.planted_bugs