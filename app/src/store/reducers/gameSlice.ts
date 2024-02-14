import {createSlice} from '@reduxjs/toolkit';

export interface IGameParams {
  selectedGame: string,
  countPlayers: number
};

const initialState : Partial<IGameParams> = {
};

const slice = createSlice({
  name: 'game',
  initialState,
  reducers: {
    setSelectedGame: (state, action) => {
      state.selectedGame = action.payload
    },
    setCountPlayers: (state, action) => {
      state.countPlayers = action.payload
    },
  }
});

export const { setSelectedGame, setCountPlayers } = slice.actions;

export default slice.reducer;
