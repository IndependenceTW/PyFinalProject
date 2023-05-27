import { Route, Routes } from "react-router-dom";
import LoginPage from "./pages/login-page";
import HomePage from "./pages/home-page";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </div>
  );
}

export default App;
