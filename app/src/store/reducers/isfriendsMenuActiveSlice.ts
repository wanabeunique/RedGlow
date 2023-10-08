import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { setLogout } from '../../api/setLogout';

type IFriendsMenuActive = {
  data: boolean
}

const initialState: IFriendsMenuActive = {
  data: false,
}

export const isfriendsMenuActiveSlice = createSlice({
  name: 'isMenuActive',
  initialState,
  reducers: {
    setFriendsMenuActive(state, action: PayloadAction<boolean>) {
      state.data = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder.addCase(setLogout.fulfilled, (state, action) => {
      state.data = false
    })
  },
});


export const { setFriendsMenuActive } = isfriendsMenuActiveSlice.actions
export default isfriendsMenuActiveSlice.reducer;