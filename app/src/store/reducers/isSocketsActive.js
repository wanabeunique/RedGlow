import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  data: false,
}

export const isSocketsActive = createSlice({
  name: 'isSocketsActive',
  initialState,
  reducers: {
    setSocketsActive(state, action) {
      state.data = action.payload;
    },
  }
});


export const { setSocketsActive } = isSocketsActive.actions
export default isSocketsActive.reducer;