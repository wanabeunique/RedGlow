import { createSlice } from "@reduxjs/toolkit";

type IUserSlice = {
  username?: string,
  photo?: string
}

const initialState: IUserSlice  = {
  username: "",
  photo: undefined 
  // Эло, стимайди?, аватар
};

export const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    setUsername(state, action) {
      state.username = action.payload;
    },
    setPhoto(state, action) {
      state.photo = action.payload;
    },
  },
});

export const { setUsername, setPhoto } = userSlice.actions;
export default userSlice.reducer;
