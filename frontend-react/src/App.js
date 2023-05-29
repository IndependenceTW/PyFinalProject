import { Route, Routes } from "react-router-dom";
import LoginPage from "./pages/login-page";
import HomePage from "./pages/home-page";
import RegisterPage from "./pages/register-page";
import DashboardLayout from "./components/Layout"
import RestaurantsPage from "./pages/restaurant-page";
import NewRestaurant from "./pages/new-restaurant-page";
import RestaurantDetailPage from "./pages/restaurant-detail-page";
import NewMenuPage from "./pages/new-menu-page";
import RecommendPage from "./pages/recommend-page";

function App() {
  return (
      <Routes>
        <Route element={<DashboardLayout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/restaurant" element={<RestaurantsPage />} />
          <Route path="/restaurant/create" element={<NewRestaurant />} />
          <Route path="/restaurant/:id" element={<RestaurantDetailPage />} />
          <Route path="/restaurant/:id/addmenu/" element={<NewMenuPage />} />
          <Route path="/recommend" element={<RecommendPage/>} />
        </Route>
      </Routes>
  );
}

export default App;
