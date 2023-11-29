import { Route, Routes } from 'react-router-dom';
import Home from './pages/home/Home'
import { ROUTES } from './utils/routes';
import Layout from './components/Layout/Layout';
import "./styles/index.scss";

const App = () => {
  return (
    <Routes>
      <Route path={ROUTES.ROOT} element={<Layout />}>
        <Route index element={<Home />} />
        <Route path='*' element={<><h1>Not found</h1></>} />
      </Route>
    </Routes>
  )
}

export default App
