import { Outlet } from "react-router-dom";
import Header from "@/components/Header/Header";
import Footer from "@/components/Footer/Footer";
import Friends from "@/pages/Friends/Friends";
import { useAppSelector } from "@/hooks/useAppSelector";

export default function Layout() {
  const isAuth = useAppSelector((state) => state.authReducer.data);

  return (
    <div className="wrapper">
      <Header />
      <Outlet />
      {isAuth && <Friends />}
      <Footer />
    </div>
  );
}
