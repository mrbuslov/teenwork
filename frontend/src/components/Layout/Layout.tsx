import { Link, Outlet } from "react-router-dom";
import Navbar from "../NavBar/Navbar";

const Layout = () => {
  return (
    <>
      <Navbar />
      <Outlet />
    </>
  )
}

export default Layout
