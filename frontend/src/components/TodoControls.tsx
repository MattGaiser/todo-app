import React from 'react';

type FilterType = 'all' | 'completed' | 'incomplete' | 'overdue';
type SortType = 'due_date' | 'created_at' | 'title';

interface TodoControlsProps {
  filter: FilterType;
  sortBy: SortType;
  onFilterChange: (filter: FilterType) => void;
  onSortChange: (sort: SortType) => void;
}

export const TodoControls: React.FC<TodoControlsProps> = ({
  filter,
  sortBy,
  onFilterChange,
  onSortChange
}) => {
  return (
    <div className="controls">
      <div className="filter-controls">
        <label>Filter:</label>
        <select 
          value={filter} 
          onChange={(e) => onFilterChange(e.target.value as FilterType)}
          className="filter-select"
        >
          <option value="all">All</option>
          <option value="completed">Completed</option>
          <option value="incomplete">Incomplete</option>
          <option value="overdue">Overdue</option>
        </select>
      </div>

      <div className="sort-controls">
        <label>Sort by:</label>
        <select 
          value={sortBy} 
          onChange={(e) => onSortChange(e.target.value as SortType)}
          className="sort-select"
        >
          <option value="due_date">Due Date</option>
          <option value="created_at">Created Date</option>
          <option value="title">Title</option>
        </select>
      </div>
    </div>
  );
}; 