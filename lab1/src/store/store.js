import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice.js';
import pollsReducer from './pollsSlice.js';
import { loadState, saveState } from './storage.js';

const persistedState = loadState();

export const store = configureStore({
  reducer: {
    auth: authReducer,
    polls: pollsReducer,
  },
  preloadedState: persistedState,
});

store.subscribe(() => {
  saveState({
    auth: store.getState().auth,
    polls: store.getState().polls,
  });
});
