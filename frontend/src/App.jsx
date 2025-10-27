import React from "react";
import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./hooks/UseAuth";
import ProtectedRoute from "./components/ProtecedRoute";
import Login from "./pages/Login";
import AppSelector from "./pages/AppSelector";
import Try from "./pages/Try";
import ExposedDashboard from "./pages/exposed/ExposedDashboard";

import { AlertProvider } from "./context/AlertContext"; // <- make sure path is correct

function App() {
  return (
    <AuthProvider>
      <AlertProvider>
        <div className="App">
          <main>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/try" element={<Try />} />
              {/* Protected Routes */}
              <Route
                path="/"
                element={
                  <ProtectedRoute>
                    <AppSelector />
                  </ProtectedRoute>
                }
              />

              <Route
                path="/exposed-infants"
                element={
                  <ProtectedRoute>
                    <ExposedDashboard />
                  </ProtectedRoute>
                }
              />
            </Routes>
          </main>
        </div>
      </AlertProvider>
    </AuthProvider>
  );
}

export default App;
