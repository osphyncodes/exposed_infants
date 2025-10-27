// AppSelector.jsx
import React from "react";
import { Button } from "react-bootstrap";
import {
  Baby,
  Handshake,
  Settings,
  Pill,
  LogOut,
  Users,
  MapPin,
  FlaskConical,
} from "lucide-react"; // import icons from lucide-react

import { useAuth } from "../hooks/UseAuth";
import { useNavigate } from "react-router-dom";
// Reusable AppCard Component
import BarChart from "../components/BarChart";
import RegistrationForm from "../components/RegistrationForm";

const categories = ["Jan", "Feb", "Mar", "Apr", "May"];
const series = [
  {
    name: "Patients",
    data: [30, 45, 28, 52, 40],
  },
  {
    name: "Dogs",
    data: [30, 45, 50, 23, 40],
  },
];

const AppCard = ({ title, description, icon: Icon, btnColor, link }) => {
  const navigate = useNavigate();

  const handleAppClick = () => {
    navigate(link);
  };

  return (
    <div className="col-md-6 col-lg-3">
      <div
        className="card text-center p-4 h-100"
        style={{ opacity: 0, top: 20 }}
      >
        <div className="mb-3">
          <Icon size={48} />
        </div>

        <h4 className="mb-3">{title}</h4>
        <p className="text-muted mb-4">{description}</p>

        <Button
          onClick={handleAppClick}
          style={{ backgroundColor: btnColor, borderColor: btnColor }}
        >
          Open App
        </Button>
      </div>
    </div>
  );
};

// AppSelector Component
const AppSelector = () => {
  const apps = [
    {
      title: "Exposed Infants",
      description:
        "Track and manage exposed infant cases with comprehensive tools.",
      icon: Baby,
      btnColor: "#0d6efd", // Bootstrap primary
      link: "/exposed-infants",
    },
    {
      title: "Tingathe Tools",
      description:
        "Community health worker tools for improved patient engagement.",
      icon: Settings,
      btnColor: "#198754", // Bootstrap success
      link: "/tingathe-tools",
    },
    {
      title: "Pact App",
      description: "Patient-centered care coordination and treatment tracking.",
      icon: Handshake,
      btnColor: "#0dcaf0", // Bootstrap info
      link: "/pact-dashboard",
    },
    {
      title: "ART App",
      description: "Antiretroviral therapy management and monitoring system.",
      icon: Pill,
      btnColor: "#6610f2", // Custom purple
      link: "/art",
    },
    {
      title: "Teen Club App",
      description: "Teen club management made easy.",
      icon: Users,
      btnColor: "#5719baff",
      link: "/sessions/dashboard",
    },
    {
      title: "Tracing App",
      description: "Manage Tracing data.",
      icon: MapPin,
      btnColor: "#6610f2",
      link: "/tracing/dashboard",
    },
    {
      title: "HVL Management App",
      description: "Manage HVL data.",
      icon: FlaskConical,
      btnColor: "#6610f2",
      link: "/hvl-management/dashboard",
    },
  ];

  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleLogout = (e) => {
    e.preventDefault();
    logout();
    navigate("/");
  };

  React.useEffect(() => {
    // Animate cards like in your jQuery example
    const cards = document.querySelectorAll(".card");
    cards.forEach((card, i) => {
      setTimeout(() => {
        card.style.opacity = 1;
        card.style.top = "0px";
        card.style.transition = "all 0.4s ease";
      }, i * 200);
    });
  }, []);

  return (
    <div className="container py-5">
      <div className="text-center mb-5">
        <h2>
          <i className="me-2"></i> Application Portal
        </h2>
        <p className="text-muted mt-3">Select an application to continue</p>
      </div>
      <div className="row g-4">
        {apps.map((app, index) => (
          <AppCard key={index} {...app} />
        ))}
      </div>

      {/* Floating Logout Button */}
      <form
        onSubmit={handleLogout}
        method="post"
        className="position-fixed bottom-0 end-0 m-3"
      >
        <button
          type="submit"
          className="btn btn-danger rounded-circle d-flex justify-content-center align-items-center"
          style={{ width: 50, height: 50 }}
          title="Logout"
        >
          <LogOut size={22} />
        </button>
      </form>
    </div>
  );
};

export default AppSelector;
