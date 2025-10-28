import React from "react";
import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./hooks/UseAuth";
import ProtectedRoute from "./components/ProtecedRoute";
import Login from "./pages/Login";
import AppSelector from "./pages/AppSelector";
import Try from "./pages/Try";
import ExposedDashboard from "./pages/exposed/ExposedDashboard";
import AdminLayout from "./components/AdminLayout";
import ExposedLayout from "./components/ExposedLayout";
import { AlertProvider } from "./context/AlertContext"; // <- make sure path is correct
import ChildrenList from "./pages/exposed/ChildrenList";
import ChildForm from "./components/children/ChildForm";
import ChildDetail from "./components/children/ChildDetail";

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
              // Add admin routes
              <Route
                path="/exposed-infants/*"
                element={
                  <ProtectedRoute>
                    <ExposedLayout />
                  </ProtectedRoute>
                }
              >
                e
                <Route index element={<ExposedDashboard />} />
                <Route path="children" element={<ChildrenList />} />
                <Route path="children/create" element={<ChildForm />} />
                <Route
                  path="children/edit/:hcc_number"
                  element={<ChildForm />}
                />
                <Route path="children/:hcc_number" element={<ChildDetail />} />
                {/* <Route path="papers" element={<AdminPapers />} />
                <Route path="quizzes" element={<AdminQuizzes />} />
                <Route path="subscriptions" element={<AdminSubscriptions />} />
                <Route path="logs" element={<AdminLogs />} />
                <Route path="settings" element={<AdminSettings />} /> */}
              </Route>
            </Routes>
          </main>
        </div>
      </AlertProvider>
    </AuthProvider>
  );
}

export default App;
