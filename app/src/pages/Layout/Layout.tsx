import { Outlet } from "react-router-dom";
import Header from "../Header/Header";
import Footer from "../Footer/Footer";
import Friends from "../Friends/Friends";

export default function Layout() {
  return (
    <div className="wrapper">
      <Header />
      <Outlet />
      <Friends />
      <Footer />
    </div>
  );
}
