import React, { useState, useEffect } from 'react';
import { 
  List, 
  ListItem, 
  Paper, 
  Typography,
  Box,
  CircularProgress,
  Alert
} from '@mui/material';
import TodoItem from './TodoItem';
import { getTodos, updateTodo, deleteTodo, Todo } from '../services/api';

function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // BUG 4: React useEffect Bug - Missing dependencies causes infinite loop
  useEffect(() => {
    fetchTodos();
  }, []); // Add empty dependency array

  const fetchTodos = async () => {
    try {
      const data = await getTodos();
      setTodos(data);
      setError('');
    } catch (err: any) {
      setError(err.message || 'Failed to fetch todos');
    } finally {
      setLoading(false);
    }
  };

  // BUG 1: State Management Bug - Todo items don't update in UI after editing
  const handleUpdate = async (id: number, updates: Partial<Todo>) => {
    try {
      // This updates the backend but doesn't update the local state
      const updated = await updateTodo(id, updates);
      setTodos(todos.map(todo => todo.id === id ? updated : todo));
    } catch (err: any) {
      setError(err.message || 'Failed to update todo');
    }
  } catch (err: any) {
      setError(err.message || 'Failed to update todo');
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteTodo(id);
      // This correctly updates the state after deletion
      setTodos(todos.filter(todo => todo.id !== id));
    } catch (err: any) {
      setError(err.message || 'Failed to delete todo');
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Paper sx={{ mt: 2, p: 2 }}>
      <Typography variant="h5" gutterBottom>
        Your Todos
      </Typography>
      
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      
      {todos.length === 0 ? (
        <Typography color="text.secondary" align="center" py={4}>
          No todos yet. Create one above!
        </Typography>
      ) : (
        <List>
          {todos.map((todo) => (
            <ListItem key={todo.id} disablePadding>
              <TodoItem 
                todo={todo}
                onUpdate={handleUpdate}
                onDelete={handleDelete}
              />
            </ListItem>
          ))}
        </List>
      )}
    </Paper>
  );
}

export default TodoList;