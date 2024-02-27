import { useEffect } from "react"
import { useAppSelector } from "./useAppSelector"
import { TThemes } from "@/store/reducers/settingsSlice"
import { useAppDispatch } from "./useAppDispatch"
import { setTheme } from "@/store/reducers/settingsSlice"
import removeBodyThemes from "@/functions/removeBodyClasses"

export const useColorSheme = () => {
  const dispatch = useAppDispatch()
  const theme = useAppSelector((state) => state.settingsReducer.theme) || 'red'

  useEffect(() => {
    const root = window.document.documentElement 
    removeBodyThemes()
    root.classList.add(`theme-${theme}`) 
  }, [theme])  

  const setColorTheme = (theme: TThemes) => { 
    dispatch(setTheme(theme)) 
  }

  return {theme, setColorTheme}
}
