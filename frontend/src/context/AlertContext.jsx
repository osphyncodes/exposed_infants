import React, { createContext, useContext, useState, useCallback } from "react";
import AlertMessage from "../components/AlertMessage";

const AlertContext = createContext();

export const AlertProvider = ({ children }) => {
  const [alert, setAlertState] = useState({ message: "", type: "info" });

  // Function that components can call
  const setAlert = useCallback((message, type = "info") => {
    setAlertState({ message, type });
  }, []);

  const handleClose = () => setAlertState({ message: "", type: "info" });

  return (
    <AlertContext.Provider value={{ setAlert }}>
      {children}
      <AlertMessage
        message={alert.message}
        variant={alert.type}
        onClose={handleClose}
      />
    </AlertContext.Provider>
  );
};

// Custom hook for easy usage
export const useAlert = () => useContext(AlertContext);
