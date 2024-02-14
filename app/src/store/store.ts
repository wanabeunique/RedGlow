import { AnyAction, configureStore, Store} from "@reduxjs/toolkit";
import thunkMiddleware from 'redux-thunk'
import rootReducer from "./reducers";
import storage from 'reduxjs-toolkit-persist/lib/storage'
import { persistReducer } from 'redux-persist' 

const persistConfig = {
  key: 'root',
  storage: storage,
}

const persistedReducer = persistReducer(persistConfig, rootReducer);

const store = configureStore({
  reducer: persistedReducer,
  middleware: [thunkMiddleware] 
})

export default store

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

