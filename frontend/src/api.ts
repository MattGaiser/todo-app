import axios, { AxiosError } from 'axios';
import { Todo, TodoCreate, TodoUpdate } from './types';

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8001';

export class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public data?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

const handleApiError = (error: unknown): never => {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError;
    throw new ApiError(
      axiosError.response?.data?.detail || 'An error occurred',
      axiosError.response?.status,
      axiosError.response?.data
    );
  }
  throw new ApiError('An unexpected error occurred');
};

const apiCall = async <T>(
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH',
  endpoint: string,
  data?: any
): Promise<T> => {
  try {
    const response = await axios({
      method,
      url: `${API_URL}${endpoint}`,
      data,
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    return handleApiError(error);
  }
};

export const api = {
  getTodos: () => apiCall<Todo[]>('GET', '/todos'),

  createTodo: (todo: TodoCreate) => apiCall<Todo>('POST', '/todos', todo),

  updateTodo: (id: number, todo: TodoUpdate) => 
    apiCall<Todo>('PUT', `/todos/${id}`, todo),

  deleteTodo: (id: number) => 
    apiCall<void>('DELETE', `/todos/${id}`),

  completeTodo: (id: number) => 
    apiCall<Todo>('PATCH', `/todos/${id}/complete`),

  incompleteTodo: (id: number) => 
    apiCall<Todo>('PATCH', `/todos/${id}/incomplete`),
}; 
