import { createSlice } from '@reduxjs/toolkit';

export interface IGameAcceptingParams {
  isActive: boolean,
  countPlayers: number,
  hash: string,
  timeToAccept: number
}

const initialState: Partial<IGameAcceptingParams> = {
  isActive: false,
  countPlayers: 0,
  hash: '',
  timeToAccept: 0
};

const slice = createSlice({
  name: 'gameAccepting',
  initialState,
  reducers: {
    setData: (state, action) => {
      state.isActive = action.payload.isActive
      state.countPlayers = action.payload.countPlayers
      state.hash = action.payload.hash
      state.timeToAccept = action.payload.timeToAccept
    }
  },
});

export const {
 setData
} = slice.actions;

export default slice.reducer;
