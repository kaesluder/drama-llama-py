import { SnackbarProvider } from 'notistack';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders refresh button', () => {
  render(
    <SnackbarProvider>
      <App />
    </SnackbarProvider>
  );
  const linkElement = screen.getByText(/Refresh/i);
  expect(linkElement).toBeInTheDocument();
});
