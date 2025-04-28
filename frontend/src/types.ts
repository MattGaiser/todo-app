export interface Todo {
  id: number;
  title: string;
  description?: string;
  due_date?: string;
  is_completed: boolean;
  created_at: string;
}

export interface TodoCreate {
  title: string;
  description?: string;
  due_date?: string;
}

export interface TodoUpdate {
  title?: string;
  description?: string;
  due_date?: string;
  is_completed?: boolean;
} 