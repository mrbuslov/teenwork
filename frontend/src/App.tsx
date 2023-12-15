import { Route, Routes } from 'react-router-dom';
import Home from './pages/Home/Home'
import { ROUTES } from './utils/routes';
import Layout from './components/Layout/Layout';
import "./styles/index.scss";
import AddJobPost from './pages/AddJobPost/AddJobPost';

const App = () => {
  return (
    <Routes>
      <Route path={ROUTES.ROOT} element={<Layout />}>
        <Route index element={<Home />} />
        <Route path={ROUTES.ADD_JOB_POST} element={<AddJobPost />} />
        <Route path='*' element={<><h1>Not found</h1></>} />
      </Route>
    </Routes>
  )
}

export default App
