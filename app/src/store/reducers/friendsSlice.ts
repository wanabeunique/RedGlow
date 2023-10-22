import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import IUser from '@/interfaces/IUser';

type friendsState = {
  in: Array<IUser>,
  out: Array<IUser>,
  current: Array<IUser>,
}

const initialState: friendsState = {
  in: [],
  out: [],
  current: [],
}

export const friendsSlice = createSlice({
  name: 'friend',
  initialState,
  reducers: {
    setFriendsIn(state, action: PayloadAction<Array<IUser>>) {
      state.in = action.payload;
    },
    setFriendsOut(state, action: PayloadAction<Array<IUser>>) {
      state.out = action.payload;
    },
    setFriendsCurrent(state, action: PayloadAction<Array<IUser>>) {
      state.current = action.payload;
    },
    removeFriendIn(state, action: PayloadAction<string>) {
      const itemToRemove = action.payload;
      state.in = state.in.filter(item => item.username !== itemToRemove )
    },
    removeFriendOut(state, action: PayloadAction<string>) {
      const itemToRemove = action.payload;
      state.out = state.in.filter(item => item.username !== itemToRemove )
    },
    removeFriendCurrent(state, action: PayloadAction<string>) {
      const itemToRemove = action.payload;
      state.current = state.in.filter(item => item.username !== itemToRemove )
    },
    addFriendOut(state, action: PayloadAction<string>) {
     state.out.push({username: action.payload})
    },
    addFriendCurrent(state, action: PayloadAction<string>) {
      state.current.push({username: action.payload})
    },
  },
});

export const { setFriendsIn, setFriendsCurrent, setFriendsOut, removeFriendIn, removeFriendOut, removeFriendCurrent, addFriendOut, addFriendCurrent } = friendsSlice.actions
export default friendsSlice.reducer;
