import { createSlice } from '@reduxjs/toolkit';

export interface IGameParams {
  selectedGame: string;
  countPlayers: number;
  eloFilter: boolean;
  activeSearch: boolean;
}

const initialState: Partial<IGameParams> = {
  eloFilter: true,
  activeSearch: false,
};

const slice = createSlice({
  name: 'game',
  initialState,
  reducers: {
    setSelectedGame: (state, action) => {
      state.selectedGame = action.payload;
    },
    setCountPlayers: (state, action) => {
      state.countPlayers = action.payload;
    },
    setEloFilter: (state, action) => {
      state.eloFilter = action.payload;
    },
    toggleEloFilter: (state) => {
      state.eloFilter = !state.eloFilter;
      console.log(state.eloFilter, !state.eloFilter);
    },
    startSearch: (state) => {
      state.activeSearch = true;
    },
    stopSearch: (state) => {
      state.activeSearch = false;
    },
  },
});

export const {
  setSelectedGame,
  setCountPlayers,
  setEloFilter,
  toggleEloFilter,
  startSearch,
  stopSearch
} = slice.actions;

export default slice.reducer;
