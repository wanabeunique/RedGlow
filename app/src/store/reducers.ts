import { combineReducers } from "@reduxjs/toolkit";
import friendsSlice from "./reducers/friendsSlice";
import authReducer from "./reducers/isAuthSlice";
import userReducer from "./reducers/userSlice";
import socketsReducer from "./reducers/isSocketsActive";
import menusReduce from "./reducers/isMenusActiveSlice";

const rootReducer = combineReducers({
  friendsSlice,
  authReducer,
  userReducer,
  socketsReducer,
  menusReduce,
});

export default rootReducer;
