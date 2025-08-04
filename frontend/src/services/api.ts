// BUG 2: CSRF Token Bug - Missing X-CSRFToken header in POST/PUT/DELETE requests

const API_BASE = '/api';

// Get CSRF token from cookie
function getCsrfTokenFromCookie(): string {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const trimmed = cookie.trim();
    if (trimmed.startsWith(name + '=')) {
      return trimmed.substring(name.length + 1);
    }
  }
  return '';
}

// API call helper - BUG: Missing CSRF token in headers for mutating requests
async function apiCall(
  endpoint: string, 
  options: RequestInit = {}
): Promise<any> {
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  if (['POST', 'PUT', 'DELETE'].includes(options.method?.toUpperCase() || '')) {
    headers['X-CSRFToken'] = getCsrfTokenFromCookie();
  }
  
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
    credentials: 'include',
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || 'Request failed');
  }

  return response.json();
}));
    throw new Error(error.detail || 'Request failed');
  }

  return response.json();
}

// Auth functions
export async function getCsrfToken() {
  return apiCall('/csrf/');
}

export async function login(username: string, password: string) {
  return apiCall('/login/', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  });
}

export async function logout() {
  return apiCall('/logout/', {
    method: 'POST',
  });
}

export async function checkAuth() {
  return apiCall('/check/');
}

// Todo CRUD operations
export interface Todo {
  id: number;
  title: string;
  description: string;
  // BUG 5: API sends 'completed' but frontend expects 'is_completed'
  is_completed: boolean;
  // BUG 5: API sends 'created_at' but frontend expects 'created'
  created: string;
}

export async function getTodos(): Promise<Todo[]> {
  return apiCall('/todos/');
}

export async function createTodo(data: Partial<Todo>): Promise<Todo> {
  return apiCall('/todos/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updateTodo(id: number, data: Partial<Todo>): Promise<Todo> {
  return apiCall(`/todos/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function deleteTodo(id: number): Promise<void> {
  return apiCall(`/todos/${id}/`, {
    method: 'DELETE',
  });
}