import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  username: '',
  // Эло, стимайди?, аватар
}

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUsername(state, action) {
      state.username = action.payload;
    },
  }
});


export const { setUsername } = userSlice.actions
export default userSlice.reducer;