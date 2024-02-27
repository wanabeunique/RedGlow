import { createSlice } from "@reduxjs/toolkit";

export type TThemes = 'red' | 'blue' | 'orange' | 'gray' | 'violet'

const initialState = {
  theme: 'red'
};

export const settingsSlice = createSlice({
  name: "settings",
  initialState,
  reducers: {
    setTheme(state, action){
      state.theme = action.payload
    }
  },
});

export const { setTheme } = settingsSlice.actions;
export default settingsSlice.reducer;
