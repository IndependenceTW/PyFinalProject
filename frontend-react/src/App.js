import { Route, Routes } from "react-router-dom";
import LoginPage from "./pages/login-page";
import HomePage from "./pages/home-page";
import RegisterPage from "./pages/register-page";
import DashboardLayout from "./components/Layout"
import RestaurantsPage from "./pages/restaurant-page";
import NewRestaurant from "./pages/new-restaurant-page";
import RestaurantDetailPage from "./pages/restaurant-detail-page";

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
        </Route>
      </Routes>
  );
}

export default App;
