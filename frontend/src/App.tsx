import { Route, Routes } from 'react-router-dom';
import Home from './pages/home/Home'
import { ROUTES } from './utils/routes';
import Layout from './components/Layout/Layout';

const App = () => {
  return (
    <Routes>
      <Route path={ROUTES.ROOT} element={<Layout />}>
        <Route index element={<Home />} />
      </Route>
    </Routes>
  )
}

export default App
