import React, { useEffect, useState } from "react";
import axios from "axios";
import Chart from "react-apexcharts";
import { exposedAPI } from "../../utils/api";
import { Loader } from "lucide-react";

/**
 * Reusable ExposedDashboard component
 * Fetches dashboard metrics and displays them using ApexCharts.
 */
const ExposedDashboard = () => {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch data on mount
  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res = await exposedAPI.getExposedDashboard();

        setDashboard(res.data);
      } catch (err) {
        console.error("Error fetching dashboard:", err);
        setError("Failed to load dashboard data");
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="text-center my-5">
        <Loader />
      </div>
    );
  }

  if (error) {
    return <p className="text-danger text-center">{error}</p>;
  }

  if (!dashboard) return null;

  // Chart Configurations
  const childrenPerMonthOptions = {
    chart: { type: "bar", toolbar: { show: false } },
    xaxis: { categories: dashboard.children_per_month_labels },
    colors: ["#007bff"],
    title: { text: "Children Registered per Month", align: "center" },
  };

  const genderDistributionOptions = {
    chart: { type: "pie" },
    labels: dashboard.gender_labels,
    colors: ["#007bff", "#ff6384"],
    title: { text: "Gender Distribution", align: "center" },
  };

  const visitTrendsOptions = {
    chart: { type: "line", toolbar: { show: false } },
    xaxis: { categories: dashboard.visit_trends_labels },
    stroke: { curve: "smooth" },
    colors: ["#28a745", "#ffc107"],
    title: { text: "Visit Trends (Last 7 Days)", align: "center" },
  };

  const outcomesOptions = {
    chart: { type: "bar", toolbar: { show: false } },
    xaxis: { categories: dashboard.outcome_labels },
    colors: ["#17a2b8"],
    title: { text: "Follow-up Outcomes", align: "center" },
  };

  const appTrendsOptions = {
    chart: { type: "line", toolbar: { show: false } },
    xaxis: { categories: dashboard.app_trends_labels },
    stroke: { curve: "smooth" },
    colors: ["#6610f2"],
    title: { text: "Upcoming Appointments (Next 7 Days)", align: "center" },
  };

  return (
    <div className="container py-4">
      <h2 className="mb-4 text-center">Children Dashboard</h2>

      {/* ===== Summary Cards ===== */}
      <div className="row g-3 mb-4">
        <div className="col-md-3">
          <div className="card shadow-sm text-center p-3">
            <h5>Total Children</h5>
            <h3 className="text-primary">{dashboard.total_children}</h3>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card shadow-sm text-center p-3">
            <h5>Total Visits</h5>
            <h3 className="text-success">{dashboard.total_visits}</h3>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card shadow-sm text-center p-3">
            <h5>Upcoming Appointments</h5>
            <h3 className="text-warning">{dashboard.upcoming_appointments}</h3>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card shadow-sm text-center p-3">
            <h5>HTS Samples</h5>
            <h3 className="text-info">{dashboard.total_hts_samples}</h3>
          </div>
        </div>
      </div>

      {/* ===== Charts ===== */}
      <div className="row g-4">
        {/* Children per Month */}
        <div className="col-lg-6">
          <div className="card shadow-sm p-3">
            <Chart
              options={childrenPerMonthOptions}
              series={[
                { name: "Children", data: dashboard.children_per_month_data },
              ]}
              type="bar"
              height={300}
            />
          </div>
        </div>

        {/* Gender Distribution */}
        <div className="col-lg-6">
          <div className="card shadow-sm p-3">
            <Chart
              options={genderDistributionOptions}
              series={dashboard.gender_data}
              type="pie"
              height={300}
            />
          </div>
        </div>

        {/* Visit Trends */}
        <div className="col-lg-6">
          <div className="card shadow-sm p-3">
            <Chart
              options={visitTrendsOptions}
              series={[
                {
                  name: "Total Visits",
                  data: dashboard.visit_trends_data,
                },
                {
                  name: "Unique Children",
                  data: dashboard.unique_children_trends_data,
                },
              ]}
              type="line"
              height={300}
            />
          </div>
        </div>

        {/* Outcomes */}
        <div className="col-lg-6">
          <div className="card shadow-sm p-3">
            <Chart
              options={outcomesOptions}
              series={[{ name: "Count", data: dashboard.outcome_data }]}
              type="bar"
              height={300}
            />
          </div>
        </div>

        {/* Appointment Trends */}
        <div className="col-lg-12">
          <div className="card shadow-sm p-3">
            <Chart
              options={appTrendsOptions}
              series={[
                { name: "Appointments", data: dashboard.app_trends_data },
              ]}
              type="line"
              height={300}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExposedDashboard;
