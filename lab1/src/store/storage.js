const APP_KEY = 'pollcraft_lab1_state';

export function loadState() {
  try {
    const serialized = localStorage.getItem(APP_KEY);
    return serialized ? JSON.parse(serialized) : undefined;
  } catch {
    return undefined;
  }
}

export function saveState(state) {
  try {
    localStorage.setItem(APP_KEY, JSON.stringify(state));
  } catch {
    // localStorage can be unavailable in private browser modes.
  }
}
