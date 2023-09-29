import { AnyAction, configureStore, Store } from "@reduxjs/toolkit";
import rootReducer from "./reducers";

const store: Store<RootState, AnyAction> = configureStore({
  reducer: rootReducer 
})

export default store

export type RootState = ReturnType<typeof rootReducer>
export type AppDispatch = typeof store.dispatch