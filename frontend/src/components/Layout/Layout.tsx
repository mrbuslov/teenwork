import { Link, Outlet } from "react-router-dom";
import styles from './Layout.module.scss';
import Navbar from "../NavBar/Navbar";

const Layout = () => {
  return (
    <>
      <Navbar />
      <Outlet />
      <div>Footer</div>
    </>
  )
}

export default Layout