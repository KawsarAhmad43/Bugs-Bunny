import React, { useState } from 'react';
import {
  Box,
  Checkbox,
  TextField,
  Typography,
  IconButton,
  ListItemText,
  ListItemSecondaryAction,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Save as SaveIcon,
  Cancel as CancelIcon,
} from '@mui/icons-material';
import { Todo } from '../services/api';

interface TodoItemProps {
  todo: Todo;
  onUpdate: (id: number, updates: Partial<Todo>) => void;
  onDelete: (id: number) => void;
}

function TodoItem({ todo, onUpdate, onDelete }: TodoItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description);

  const handleSave = () => {
    onUpdate(todo.id, {
      title: editTitle,
      description: editDescription,
    });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditTitle(todo.title);
    setEditDescription(todo.description);
    setIsEditing(false);
  };

  const handleToggleComplete = () => {
    // BUG 5: Using wrong field name
    onUpdate(todo.id, {
      is_completed: !todo.is_completed,
    });
  };

  if (isEditing) {
    return (
      <Box sx={{ width: '100%', p: 1 }}>
        <TextField
          fullWidth
          value={editTitle}
          onChange={(e) => setEditTitle(e.target.value)}
          margin="dense"
          size="small"
        />
        <TextField
          fullWidth
          multiline
          rows={2}
          value={editDescription}
          onChange={(e) => setEditDescription(e.target.value)}
          margin="dense"
          size="small"
        />
        <Box sx={{ mt: 1 }}>
          <IconButton onClick={handleSave} color="primary">
            <SaveIcon />
          </IconButton>
          <IconButton onClick={handleCancel}>
            <CancelIcon />
          </IconButton>
        </Box>
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', width: '100%', p: 1 }}>
      <Checkbox
        checked={todo.is_completed}
        onChange={handleToggleComplete}
      />
      <ListItemText
        primary={
          <Typography
            variant="body1"
            sx={{
              textDecoration: todo.is_completed ? 'line-through' : 'none',
            }}
          >
            {todo.title}
          </Typography>
        }
        secondary={todo.description}
      />
      <ListItemSecondaryAction>
        <IconButton onClick={() => setIsEditing(true)}>
          <EditIcon />
        </IconButton>
        <IconButton onClick={() => onDelete(todo.id)} color="error">
          <DeleteIcon />
        </IconButton>
      </ListItemSecondaryAction>
    </Box>
  );
}

export default TodoItem;