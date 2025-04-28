import React from 'react';
import { Todo } from '../types';

interface TodoItemProps {
  todo: Todo;
  onComplete: (id: number) => Promise<void>;
  onIncomplete: (id: number) => Promise<void>;
  onEdit: (todo: Todo) => void;
  onDelete: (id: number) => Promise<void>;
  isOverdue: (todo: Todo) => boolean;
  formatDate: (dateString: string) => string;
}

export const TodoItem: React.FC<TodoItemProps> = ({
  todo,
  onComplete,
  onIncomplete,
  onEdit,
  onDelete,
  isOverdue,
  formatDate
}) => {
  const status = todo.is_completed ? 'completed' : isOverdue(todo) ? 'overdue' : 'pending';
  
  return (
    <li 
      className={`todo-item ${todo.is_completed ? 'completed' : ''} ${isOverdue(todo) ? 'overdue' : ''}`}
      role="listitem"
      aria-label={`Todo: ${todo.title}`}
      aria-describedby={`todo-description-${todo.id}`}
      aria-live="polite"
    >
      <div className="todo-content">
        <h3>{todo.title}</h3>
        {todo.description && (
          <p 
            className="description" 
            id={`todo-description-${todo.id}`}
          >
            {todo.description}
          </p>
        )}
        <div className="todo-dates">
          {todo.due_date && (
            <p className="due-date">
              <strong>Due:</strong> {formatDate(todo.due_date)}
            </p>
          )}
          <p className="created-date">
            <strong>Created:</strong> {formatDate(todo.created_at)}
          </p>
        </div>
      </div>
      <div className="todo-actions">
        {todo.is_completed ? (
          <button 
            onClick={() => onIncomplete(todo.id)} 
            className="incomplete-button"
            aria-label={`Mark "${todo.title}" as incomplete`}
          >
            Mark Incomplete
          </button>
        ) : (
          <button 
            onClick={() => onComplete(todo.id)} 
            className="complete-button"
            aria-label={`Mark "${todo.title}" as complete`}
          >
            Mark Complete
          </button>
        )}
        <button 
          onClick={() => onEdit(todo)} 
          className="edit-button"
          aria-label={`Edit "${todo.title}"`}
        >
          Edit
        </button>
        <button 
          onClick={() => onDelete(todo.id)} 
          className="delete-button"
          aria-label={`Delete "${todo.title}"`}
        >
          Delete
        </button>
      </div>
    </li>
  );
}; 