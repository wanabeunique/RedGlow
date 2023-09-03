import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  data: false,
}

export const isAuthSlice = createSlice({
  name: 'isAuth',
  initialState,
  reducers: {
    setIsAuth(state, action) {
      state.data = action.payload;
    },
  }
});


export const { setIsAuth } = isAuthSlice.actions
export default isAuthSlice.reducer;