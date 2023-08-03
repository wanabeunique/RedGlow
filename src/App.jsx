import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.sass'
import Header from './components/Header/Header'
import Footer from './components/Footer/Footer'
import { Button } from 'antd';

function App() {
  return (
    <>
      <Header />
      <Footer />
      <Button type="primary">Button</Button>
    </>
  )
}

export default App
