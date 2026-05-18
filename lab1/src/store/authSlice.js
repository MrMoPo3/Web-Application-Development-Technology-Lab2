import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  users: [],
  currentUserEmail: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    registerUser(state, action) {
      const user = action.payload;
      const exists = state.users.some((item) => item.email === user.email);

      if (!exists) {
        state.users.push(user);
      }

      state.currentUserEmail = user.email;
    },
    loginUser(state, action) {
      state.currentUserEmail = action.payload.email;
    },
    logoutUser(state) {
      state.currentUserEmail = null;
    },
  },
});

export const { registerUser, loginUser, logoutUser } = authSlice.actions;
export default authSlice.reducer;
