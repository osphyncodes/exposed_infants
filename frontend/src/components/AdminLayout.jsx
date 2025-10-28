import React, { useState, useEffect } from "react";
import { Outlet } from "react-router-dom";
import AdminSidebar from "./AdminSidebar";
import "../styles/AdminLayout.css";
import { LayoutDashboard, Menu, Bell, User } from "lucide-react";
import { useAuth } from "../hooks/UseAuth";

const AdminLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [menuItems, setMenuItems] = useState([]);
  const { user, logout } = useAuth();

  const menuData = [
    {
      name: "Dashboard",
      path: "/exposed-infants",
      icon: <LayoutDashboard size={20} />,
      exact: true,
    },
    {
      name: "Children",
      path: "/exposed-infants/children",
      icon: <LayoutDashboard size={20} />,
      exact: true,
    },
  ];

  useEffect(() => {
    const checkMobile = () => {
      const mobile = window.innerWidth < 768;
      setIsMobile(mobile);
      // Auto-close sidebar on resize to desktop if it was open
      if (!mobile && sidebarOpen) {
        setSidebarOpen(false);
      }
    };

    checkMobile();
    window.addEventListener("resize", checkMobile);

    return () => {
      window.removeEventListener("resize", checkMobile);
    };
  }, [sidebarOpen]);

  const handleSidebarToggle = (collapsed) => {
    setSidebarCollapsed(collapsed);
  };

  const getMainContentStyle = () => {
    if (isMobile) {
      return {
        marginLeft: "0",
        width: "100%",
      };
    }

    return {
      marginLeft: sidebarCollapsed ? "0px" : "0px",
      width: sidebarCollapsed ? "calc(100% - 80px)" : "calc(100% - 0px)",
      transition: "all 0.3s ease",
    };
  };

  return (
    <div className="d-flex">
      <AdminSidebar
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen(!sidebarOpen)}
        onCollapse={handleSidebarToggle}
        menuItems={menuData}
      />

      {/* Main Content */}
      <div className="flex-grow-1 bg-light" style={getMainContentStyle()}>
        {/* Top Bar */}
        <div className="bg-white border-bottom py-3 px-4 d-flex align-items-center shadow-sm">
          <button
            className="btn btn-outline-secondary btn-sm me-3 d-md-none"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu size={16} />
          </button>

          <div className="d-flex align-items-center flex-grow-1">
            <h5 className="mb-0 fw-semibold text-dark">Admin Dashboard</h5>
            {sidebarCollapsed && !isMobile && (
              <small className="text-muted ms-2">(Collapsed)</small>
            )}
          </div>

          {/* Topbar Actions */}
          <div className="d-flex align-items-center gap-3">
            <button className="btn btn-light btn-sm position-relative">
              <Bell size={18} />
              <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                3
              </span>
            </button>

            <div className="dropdown">
              <button
                className="btn btn-light btn-sm dropdown-toggle d-flex align-items-center"
                type="button"
                data-bs-toggle="dropdown"
              >
                <div
                  className="bg-primary rounded-circle d-flex align-items-center justify-content-center text-white me-2"
                  style={{ width: "32px", height: "32px", fontSize: "14px" }}
                >
                  <User size={16} />
                </div>
                <span className="d-none d-md-inline">Admin</span>
              </button>
              <ul className="dropdown-menu dropdown-menu-end">
                <li>
                  <a className="dropdown-item" href="/profile">
                    Profile
                  </a>
                </li>
                <li>
                  <a className="dropdown-item" href="/settings">
                    Settings
                  </a>
                </li>
                <li>
                  <hr className="dropdown-divider" />
                </li>
                <li>
                  <button
                    className="dropdown-item"
                    onClick={() => {
                      logout();
                    }}
                  >
                    Logout
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* Page Content */}
        <div className="p-4" style={{ minHeight: "calc(100vh - 60px)" }}>
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default AdminLayout;
