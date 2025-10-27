import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  Users,
  FileText,
  BookOpen,
  CreditCard,
  Settings,
  Activity,
  BarChart3,
  Shield,
  LogOut,
  Menu,
  ChevronLeft,
  ChevronRight,
  Home,
} from "lucide-react";
import "../styles/AdminSidebar.css";

const AdminSidebar = ({ isOpen, onToggle }) => {
  const location = useLocation();
  const [collapsed, setCollapsed] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  // Check if device is mobile
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkMobile();
    window.addEventListener("resize", checkMobile);

    return () => {
      window.removeEventListener("resize", checkMobile);
    };
  }, []);

  const menuItems = [
    {
      name: "Dashboard",
      path: "/admin",
      icon: <LayoutDashboard size={20} />,
      exact: true,
    },
    {
      name: "Users",
      path: "/admin/users",
      icon: <Users size={20} />,
    },
    {
      name: "Papers",
      path: "/admin/papers",
      icon: <FileText size={20} />,
    },
    {
      name: "Quizzes",
      path: "/admin/quizzes",
      icon: <BookOpen size={20} />,
    },
    {
      name: "Subscriptions",
      path: "/admin/subscriptions",
      icon: <CreditCard size={20} />,
    },
    {
      name: "Subjects",
      path: "/admin/subjects",
      icon: <BarChart3 size={20} />,
    },
    {
      name: "Activity Logs",
      path: "/admin/logs",
      icon: <Activity size={20} />,
    },
    {
      name: "Settings",
      path: "/admin/settings",
      icon: <Settings size={20} />,
    },
  ];

  const isActive = (path, exact = false) => {
    if (exact) {
      return location.pathname === path;
    }
    return location.pathname.startsWith(path);
  };

  const handleToggle = () => {
    if (isMobile) {
      onToggle();
    } else {
      setCollapsed(!collapsed);
    }
  };

  const handleLinkClick = () => {
    if (isMobile) {
      onToggle();
    }
  };

  const sidebarWidth = collapsed ? "80px" : "280px";
  const sidebarClass = `bg-dark text-white vh-100 position-fixed start-0 top-0 z-3 ${
    isOpen || !isMobile ? "d-block" : "d-none"
  }`;

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && isMobile && (
        <div
          className="d-md-none position-fixed top-0 start-0 w-100 h-100 bg-dark bg-opacity-50 z-2"
          onClick={onToggle}
        />
      )}

      {/* Sidebar */}
      <div
        className={sidebarClass}
        style={{
          width: isMobile ? "280px" : sidebarWidth,
          transition: "all 0.3s ease",
          boxShadow: "2px 0 10px rgba(0,0,0,0.1)",
        }}
      >
        {/* Header */}
        <div className="p-3 border-bottom border-secondary position-relative">
          <div
            className={`d-flex justify-content-between align-items-center ${
              collapsed ? "flex-column gap-2" : ""
            }`}
          >
            {!collapsed && (
              <div className="flex-grow-1">
                <div className="d-flex align-items-center">
                  <Shield className="me-2" size={24} />
                  <div>
                    <h6 className="mb-0 text-white">Admin Panel</h6>
                    <small className="text-muted">PastPapers Pro</small>
                  </div>
                </div>
              </div>
            )}

            {collapsed && (
              <div className="text-center">
                <Shield size={28} />
                <small className="text-muted d-block mt-1">Admin</small>
              </div>
            )}

            {/* Toggle Button */}
            <div className={`${collapsed ? "" : "ms-2"}`}>
              <button
                className="btn btn-outline-light btn-sm"
                onClick={handleToggle}
                title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
              >
                {isMobile ? (
                  <Menu size={16} />
                ) : collapsed ? (
                  <ChevronRight size={16} />
                ) : (
                  <ChevronLeft size={16} />
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="p-3">
          <ul className="nav nav-pills flex-column">
            {menuItems.map((item) => (
              <li key={item.path} className="nav-item mb-2">
                <Link
                  to={item.path}
                  className={`nav-link d-flex align-items-center ${
                    isActive(item.path, item.exact)
                      ? "bg-primary text-white"
                      : "text-light hover-bg-light hover-bg-opacity-10"
                  }`}
                  style={{
                    borderRadius: "8px",
                    transition: "all 0.2s",
                    padding: collapsed ? "0.75rem" : "0.75rem 1rem",
                    justifyContent: collapsed ? "center" : "flex-start",
                  }}
                  onClick={handleLinkClick}
                  title={collapsed ? item.name : ""}
                >
                  <span className={collapsed ? "" : "me-3"}>{item.icon}</span>
                  {!collapsed && (
                    <span
                      style={{
                        opacity: collapsed ? 0 : 1,
                        transition: "opacity 0.2s ease",
                      }}
                    >
                      {item.name}
                    </span>
                  )}
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        {/* Footer */}
        <div className="position-absolute bottom-0 start-0 w-100 p-3 border-top border-secondary">
          <div
            className={`d-flex justify-content-between align-items-center ${
              collapsed ? "flex-column gap-2" : ""
            }`}
          >
            {!collapsed && (
              <div>
                <small className="text-muted">Admin User</small>
              </div>
            )}

            <div className="d-flex gap-2">
              <Link
                to="/"
                className="btn btn-outline-light btn-sm"
                title="Back to Home"
                onClick={handleLinkClick}
              >
                <Home size={14} />
                {!collapsed && <span className="ms-1">Home</span>}
              </Link>

              <Link
                to="/logout"
                className="btn btn-outline-light btn-sm"
                title="Logout"
                onClick={handleLinkClick}
              >
                <LogOut size={14} />
                {!collapsed && <span className="ms-1">Logout</span>}
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Spacer for desktop when not collapsed */}
      {!isMobile && !collapsed && (
        <div style={{ width: "280px", flexShrink: 0 }}></div>
      )}

      {!isMobile && collapsed && (
        <div style={{ width: "80px", flexShrink: 0 }}></div>
      )}
    </>
  );
};

export default AdminSidebar;
