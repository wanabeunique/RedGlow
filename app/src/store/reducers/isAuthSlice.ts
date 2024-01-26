import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { setLogout } from '../../service/setLogout';

type isAuthState = {
  data: boolean;
};

const initialState: isAuthState = {
  data: false,
};

export const isAuthSlice = createSlice({
  name: 'isAuth',
  initialState,
  reducers: {
    setIsAuth(state, action: PayloadAction<boolean>) {
      state.data = action.payload;
    },
  },
});

export const { setIsAuth } = isAuthSlice.actions;
export default isAuthSlice.reducer;
