import { createSlice, PayloadAction } from '@reduxjs/toolkit'

type IMenusActive = {
  friends: boolean,
  profile: boolean,
}

const initialState: IMenusActive = {
  friends: false,
  profile: false,
}

export const isfriendsMenuActiveSlice = createSlice({
  name: 'isMenuActive',
  initialState,
  reducers: {
    setFriendsMenuActive(state, action: PayloadAction<boolean>) {
      state.friends = action.payload;
    },
    setProfileMenuActive(state, action: PayloadAction<boolean>) {
      state.profile = action.payload;
    },
  },
});


export const { setFriendsMenuActive, setProfileMenuActive } = isfriendsMenuActiveSlice.actions
export default isfriendsMenuActiveSlice.reducer;