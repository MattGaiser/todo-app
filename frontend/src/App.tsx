import { useState, useEffect, useMemo } from 'react';
import { Todo, TodoCreate } from './types';
import { api } from './api';
import { TodoForm } from './components/TodoForm';
import { TodoList } from './components/TodoList';
import { TodoControls } from './components/TodoControls';
import { useApiError } from './hooks/useApiError';
import { ErrorBoundary } from './components/ErrorBoundary';
import { ToastProvider } from './contexts/ToastContext';
import './App.css';

type FilterType = 'all' | 'completed' | 'incomplete' | 'overdue';
type SortType = 'due_date' | 'created_at' | 'title';

function isOverdue(todo: Todo): boolean {
  if (!todo.due_date || todo.is_completed) return false;
  const [year, month, day] = todo.due_date.split('T')[0].split('-').map(Number);
  const dueDate = new Date(year, month - 1, day);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return dueDate < today;
}

function App() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodo, setNewTodo] = useState<TodoCreate>({
    title: '',
    description: '',
    due_date: ''
  });
  const [editingTodo, setEditingTodo] = useState<Todo | null>(null);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [filter, setFilter] = useState<FilterType>('all');
  const [sortBy, setSortBy] = useState<SortType>('due_date');
  const { error, handleApiError, clearError } = useApiError();

  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    try {
      setLoading(true);
      const data = await api.getTodos();
      setTodos(data);
      clearError();
    } catch (err) {
      handleApiError(err, 'Failed to load todos');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTodo.title.trim()) return;

    try {
      const created = await api.createTodo(newTodo);
      setTodos([...todos, created]);
      setNewTodo({ title: '', description: '', due_date: '' });
      setShowForm(false);
      clearError();
    } catch (err) {
      handleApiError(err, 'Failed to create todo');
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingTodo) return;

    try {
      const updated = await api.updateTodo(editingTodo.id, {
        title: editingTodo.title,
        description: editingTodo.description,
        due_date: editingTodo.due_date
      });
      setTodos(todos.map(todo => todo.id === editingTodo.id ? updated : todo));
      setEditingTodo(null);
      clearError();
    } catch (err) {
      handleApiError(err, 'Failed to update todo');
    }
  };

  const handleComplete = async (id: number) => {
    try {
      const updated = await api.completeTodo(id);
      setTodos(todos.map(todo => todo.id === id ? updated : todo));
      clearError();
    } catch (err) {
      handleApiError(err, 'Failed to complete todo');
    }
  };

  const handleIncomplete = async (id: number) => {
    try {
      const updated = await api.incompleteTodo(id);
      setTodos(todos.map(todo => todo.id === id ? updated : todo));
      clearError();
    } catch (err) {
      handleApiError(err, 'Failed to mark todo as incomplete');
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await api.deleteTodo(id);
      setTodos(todos.filter(todo => todo.id !== id));
      clearError();
    } catch (err) {
      handleApiError(err, 'Failed to delete todo');
    }
  };

  const formatDate = (dateString: string) => {
    const [year, month, day] = dateString.split('T')[0].split('-').map(Number);
    const date = new Date(year, month - 1, day);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const filteredTodos = useMemo(() => {
    return todos.filter(todo => {
      switch (filter) {
        case 'completed':
          return todo.is_completed;
        case 'incomplete':
          return !todo.is_completed;
        case 'overdue':
          return isOverdue(todo);
        default:
          return true;
      }
    });
  }, [todos, filter]);

  const sortedTodos = useMemo(() => {
    return [...filteredTodos].sort((a, b) => {
      switch (sortBy) {
        case 'due_date':
          if (!a.due_date) return 1;
          if (!b.due_date) return -1;
          return a.due_date.localeCompare(b.due_date);
        case 'created_at':
          return a.created_at.localeCompare(b.created_at);
        case 'title':
          return a.title.localeCompare(b.title);
        default:
          return 0;
      }
    });
  }, [filteredTodos, sortBy]);

  if (loading) return <div className="loading" role="status" aria-live="polite">Loading...</div>;

  return (
    <ToastProvider>
      <ErrorBoundary>
        <div className="App" role="main">
          <h1>Todo App</h1>
          
          {error && (
            <div 
              className="error" 
              role="alert" 
              aria-live="assertive"
            >
              {error}
            </div>
          )}

          <TodoControls
            filter={filter}
            sortBy={sortBy}
            onFilterChange={setFilter}
            onSortChange={setSortBy}
          />

          <button 
            className="toggle-form-button"
            onClick={() => {
              setShowForm(!showForm);
              setEditingTodo(null);
            }}
            aria-expanded={showForm}
            aria-controls="todo-form"
          >
            {showForm ? 'Cancel' : 'Add New Todo'}
          </button>

          {showForm && !editingTodo && (
            <div id="todo-form" role="form" aria-label="New Todo Form">
              <TodoForm
                todo={newTodo}
                onSubmit={handleSubmit}
                onChange={(field, value) => setNewTodo({ ...newTodo, [field]: value })}
                isEditing={false}
              />
            </div>
          )}

          {editingTodo && (
            <div id="todo-form" role="form" aria-label="Edit Todo Form">
              <TodoForm
                todo={editingTodo}
                onSubmit={handleUpdate}
                onChange={(field, value) => setEditingTodo({ ...editingTodo, [field]: value })}
                onCancel={() => setEditingTodo(null)}
                isEditing={true}
              />
            </div>
          )}

          <TodoList
            todos={sortedTodos}
            onComplete={handleComplete}
            onIncomplete={handleIncomplete}
            onEdit={setEditingTodo}
            onDelete={handleDelete}
            isOverdue={isOverdue}
            formatDate={formatDate}
          />
        </div>
      </ErrorBoundary>
    </ToastProvider>
  );
}

export default App;
