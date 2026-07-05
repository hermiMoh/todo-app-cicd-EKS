import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

test('renders todo app', () => {
  render(<App />);
  const titleElement = screen.getByText(/Todo List/i);
  expect(titleElement).toBeInTheDocument();
});

test('adds a new todo', async () => {
  render(<App />);
  const input = screen.getByPlaceholderText(/Enter a new todo/i);
  const button = screen.getByText(/Add/i);
  
  fireEvent.change(input, { target: { value: 'Test Todo' } });
  fireEvent.click(button);
  
  const todoElement = await screen.findByText('Test Todo');
  expect(todoElement).toBeInTheDocument();
});