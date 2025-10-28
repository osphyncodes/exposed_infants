import React from "react";
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
  Bell,
  User,
} from "lucide-react";
import AdminLayout from "./AdminLayout";

const menuData = [
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

const ExposedLayout = () => {
  return <AdminLayout menuData={menuData} />;
};

export default ExposedLayout;
