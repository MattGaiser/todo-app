import React from 'react';
import { Todo } from '../types';
import { TodoItem } from './TodoItem';

interface TodoListProps {
  todos: Todo[];
  onComplete: (id: number) => Promise<void>;
  onIncomplete: (id: number) => Promise<void>;
  onEdit: (todo: Todo) => void;
  onDelete: (id: number) => Promise<void>;
  isOverdue: (todo: Todo) => boolean;
  formatDate: (dateString: string) => string;
}

export const TodoList: React.FC<TodoListProps> = ({
  todos,
  onComplete,
  onIncomplete,
  onEdit,
  onDelete,
  isOverdue,
  formatDate
}) => {
  return (
    <ul 
      className="todo-list"
      role="list"
      aria-label="List of todos"
    >
      {todos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onComplete={onComplete}
          onIncomplete={onIncomplete}
          onEdit={onEdit}
          onDelete={onDelete}
          isOverdue={isOverdue}
          formatDate={formatDate}
        />
      ))}
    </ul>
  );
}; 