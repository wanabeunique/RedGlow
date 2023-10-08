import { combineReducers } from "@reduxjs/toolkit";
import authReducer from "./reducers/isAuthSlice";
import userReducer from "./reducers/userSlice";
import socketsReducer from "./reducers/isSocketsActive";
import menusReduce from "./reducers/isMenusActiveSlice";

const rootReducer = combineReducers({
  authReducer,
  userReducer,
  socketsReducer,
  menusReduce,
});

export default rootReducer;
