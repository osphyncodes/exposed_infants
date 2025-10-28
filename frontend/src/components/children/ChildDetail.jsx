import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import {
  FaChild,
  FaCalendarCheck,
  FaVial,
  FaUserShield,
  FaArrowLeft,
} from "react-icons/fa";

const ChildDetail = () => {
  const { hcc_number } = useParams();
  const [child, setChild] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchChild = async () => {
      try {
        const res = await axios.get(`/api/children/${hcc_number}/`);
        setChild(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchChild();
  }, [hcc_number]);

  if (loading) return <div>Loading...</div>;
  if (!child) return <div>Child not found</div>;

  return (
    <div
      className="container-fluid px-4"
      style={{ maxWidth: "1600px", paddingTop: "70px" }}
    >
      {/* Navbar */}
      <nav
        className="navbar navbar-expand-lg navbar-light bg-white fixed-top shadow-sm"
        style={{ zIndex: 1030 }}
      >
        <div className="container-fluid">
          <span className="navbar-brand fw-bold">
            <FaChild className="me-2" /> {child.child_name} ({child.hcc_number})
          </span>

          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNavDropdown"
          >
            <span className="navbar-toggler-icon"></span>
          </button>

          <div className="collapse navbar-collapse" id="navbarNavDropdown">
            <ul className="navbar-nav me-auto">
              <li className="nav-item">
                <Link className="nav-link" to={`/visits/${child.hcc_number}`}>
                  <FaCalendarCheck className="me-1" /> Visits
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to={`/hts/${child.hcc_number}`}>
                  <FaVial className="me-1" /> HTS Results
                </Link>
              </li>
              {/* Admin dropdown only if needed */}
              {/* Add more links as necessary */}
            </ul>

            <Link className="btn btn-outline-secondary" to="/children">
              <FaArrowLeft className="me-2" /> Back to List
            </Link>
          </div>
        </div>
      </nav>

      {/* Child Info */}
      <div className="card shadow mb-4 mt-4">
        <div className="card-header bg-primary text-white">
          <h3 className="card-title mb-0">
            <FaChild className="me-2" />
            Child Information
          </h3>
        </div>
        <div className="card-body row g-3">
          {/* Basic Info */}
          <div className="col-md-4 p-3 bg-light rounded">
            <h5 className="border-bottom pb-2 mb-3">Basic Info</h5>
            <div>
              <strong>HCC Number:</strong> {child.hcc_number}
            </div>
            <div>
              <strong>Name:</strong> {child.child_name}
            </div>
            <div>
              <strong>DOB:</strong> {child.child_dob}
            </div>
            <div>
              <strong>Gender:</strong> {child.child_gender}
            </div>
            <div>
              <strong>Birth Weight:</strong> {child.child_birth_weight} kg
            </div>
          </div>

          {/* Guardian Info */}
          <div className="col-md-4 p-3 bg-light rounded">
            <h5 className="border-bottom pb-2 mb-3">Guardian Info</h5>
            <div>
              <strong>Guardian:</strong> {child.guardian_name}
            </div>
            <div>
              <strong>Relationship:</strong> {child.relationship}
            </div>
            <div>
              <strong>Phone:</strong> {child.guardian_phone}
            </div>
            <div>
              <strong>Address:</strong> {child.physical_address}
            </div>
            <div>
              <strong>Agrees to FUP:</strong>{" "}
              {child.agrees_to_fup ? "Yes" : "No"}
            </div>
          </div>

          {/* Medical Status */}
          <div className="col-md-4 p-3 bg-light rounded">
            <h5 className="border-bottom pb-2 mb-3">Medical Status</h5>
            <div>
              <strong>Mother Status:</strong> {child.mother_status}
            </div>
            <div>
              <strong>ART Number:</strong> {child.mother_art_number}
            </div>
            <div>
              <strong>ART Start Date:</strong> {child.mother_art_start_date}
            </div>
          </div>
        </div>
      </div>

      {/* Visits Table */}
      <div className="card shadow mb-4">
        <div className="card-header bg-secondary text-white">
          <h3 className="card-title mb-0">
            <FaCalendarCheck className="me-2" />
            Visit History
          </h3>
        </div>
        <div className="card-body">
          {child.visits.length > 0 ? (
            <div className="table-responsive">
              <table className="table table-bordered table-hover table-striped">
                <thead className="table-light">
                  <tr>
                    <th>Age</th>
                    <th>Visit Date</th>
                    <th>Height</th>
                    <th>Weight</th>
                    <th>MUAC</th>
                    <th>Breastfeeding</th>
                    <th>Outcome</th>
                  </tr>
                </thead>
                <tbody>
                  {child.visits.map((v) => (
                    <tr key={v.id}>
                      <td>{v.age_in_months}m</td>
                      <td>{v.visit_date}</td>
                      <td>{v.height || "-"}</td>
                      <td>{v.weight || "-"}</td>
                      <td>{v.muac || "-"}</td>
                      <td>{v.breastfeeding || "-"}</td>
                      <td>{v.follow_up_outcome || "-"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="alert alert-info">No visits recorded yet.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChildDetail;
