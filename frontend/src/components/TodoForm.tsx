import React, { useState } from 'react';
import {
  Paper,
  TextField,
  Button,
  Box,
  Typography,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { createTodo } from '../services/api';

function TodoForm() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setLoading(true);
    setError('');

    try {
      await createTodo({
        title: title.trim(),
        description: description.trim(),
      });
      
      // Clear form on success
      setTitle('');
      setDescription('');
      
      // Note: In a real app, we'd update the todo list here
      // But since this is a bug challenge, we'll let them figure out
      // that the list doesn't refresh automatically
      window.location.reload(); // Temporary workaround
    } catch (err: any) {
      setError(err.message || 'Failed to create todo');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Add New Todo
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          fullWidth
          label="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          margin="normal"
          required
          error={!!error}
          helperText={error}
        />
        <TextField
          fullWidth
          label="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          margin="normal"
          multiline
          rows={3}
        />
        <Box sx={{ mt: 2 }}>
          <Button
            type="submit"
            variant="contained"
            startIcon={<AddIcon />}
            disabled={loading || !title.trim()}
          >
            {loading ? 'Adding...' : 'Add Todo'}
          </Button>
        </Box>
      </form>
    </Paper>
  );
}

export default TodoForm;