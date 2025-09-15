import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App';

// Render the app
const root = createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
