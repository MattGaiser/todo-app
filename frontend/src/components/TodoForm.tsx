import React from 'react';
import { Todo, TodoCreate } from '../types';

interface TodoFormProps {
  todo: TodoCreate | Todo;
  onSubmit: (e: React.FormEvent) => Promise<void>;
  onChange: (field: keyof TodoCreate, value: string) => void;
  onCancel?: () => void;
  isEditing?: boolean;
}

export const TodoForm: React.FC<TodoFormProps> = ({
  todo,
  onSubmit,
  onChange,
  onCancel,
  isEditing = false
}) => {
  const formatDateForInput = (dateString: string) => {
    return dateString.split('T')[0];
  };

  return (
    <form 
      onSubmit={onSubmit} 
      className="todo-form"
      aria-label={isEditing ? "Edit Todo Form" : "New Todo Form"}
    >
      <div className="form-group">
        <label htmlFor="title">Title *</label>
        <input
          id="title"
          type="text"
          value={todo.title}
          onChange={(e) => onChange('title', e.target.value)}
          placeholder="Enter todo title"
          required
          className="todo-input"
          aria-required="true"
          aria-label="Todo title"
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          value={todo.description || ''}
          onChange={(e) => onChange('description', e.target.value)}
          placeholder="Enter todo description"
          className="todo-textarea"
          aria-label="Todo description"
        />
      </div>

      <div className="form-group">
        <label htmlFor="due_date">Due Date</label>
        <input
          id="due_date"
          type="date"
          value={todo.due_date ? formatDateForInput(todo.due_date) : ''}
          onChange={(e) => onChange('due_date', e.target.value)}
          className="todo-input"
          aria-label="Todo due date"
        />
      </div>

      <div className="form-actions">
        <button 
          type="submit" 
          className={isEditing ? 'update-button' : 'add-button'}
          aria-label={isEditing ? "Update todo" : "Add todo"}
        >
          {isEditing ? 'Update Todo' : 'Add Todo'}
        </button>
        {onCancel && (
          <button 
            type="button" 
            className="cancel-button"
            onClick={onCancel}
            aria-label="Cancel form"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}; 