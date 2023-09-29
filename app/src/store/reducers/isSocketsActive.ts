import { createSlice, PayLoadAction } from '@reduxjs/toolkit'

interface ISocket{
  data: boolean
}

const initialState: ISocket = {
  data: false,
}

export const isSocketsActive = createSlice({
  name: 'isSocketsActive',
  initialState,
  reducers: {
    setSocketsActive(state, action: PayLoadAction<boolean>) {
      state.data = action.payload;
    },
  }
});


export const { setSocketsActive } = isSocketsActive.actions
export default isSocketsActive.reducer;