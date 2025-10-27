import React, { useEffect } from "react";
import "../styles/Alert.css";

const Alert = ({ variant = "info", message, onClose }) => {
  if (!message) return null;

  // Auto close after 3 seconds
  useEffect(() => {
    const timer = setTimeout(() => {
      if (onClose) onClose();
    }, 4000);

    return () => clearTimeout(timer);
  }, [message, onClose]);

  return (
    <div className="alert-container">
      <div
        className={`alert alert-${variant} alert-dismissible fade show shadow alert-slide`}
        role="alert"
      >
        {message}
        {onClose && (
          <button
            type="button"
            className="btn-close"
            onClick={onClose}
          ></button>
        )}
      </div>
    </div>
  );
};

export default Alert;
