import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import IUser from '@/interfaces/IUser';

type friendsState = {
  in: Array<IUser>;
  out: Array<IUser>;
  current: Array<IUser>;
};

const initialState: friendsState = {
  in: [],
  out: [],
  current: [],
};

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

    createInvite(state, action: PayloadAction<string>) {
      state.out.push({ username: action.payload });
    },
    cancelInvite(state, action: PayloadAction<string>) {
      state.in = state.in.filter((item) => item.username !== action.payload);
    },
    declineRequest(state, action: PayloadAction<string>) {
      state.out = state.out.filter((item) => item.username !== action.payload);
    },
    deleteFriend(state, action: PayloadAction<string>) {
      state.current = state.current.filter(
        (item) => item.username !== action.payload,
      );
      state.in.push({ username: action.payload });
    },
    incomingInvite(state, action: PayloadAction<string>) {
      state.in.push({ username: action.payload });
    },
    acceptInvite(state, action: PayloadAction<string>) {
      state.in = state.in.filter((item) => item.username !== action.payload);
      state.current.push({ username: action.payload });
    },
    acceptedInvite(state, action: PayloadAction<string>) {
      state.out = state.out.filter((item) => item.username !== action.payload);
      state.current.push({ username: action.payload });
    },
  },
});

export const {
  setFriendsIn,
  setFriendsCurrent,
  setFriendsOut,
  createInvite,
  acceptInvite,
  cancelInvite,
  declineRequest,
  deleteFriend,
  acceptedInvite,
  incomingInvite,
} = friendsSlice.actions;
export default friendsSlice.reducer;
