import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import { exposedAPI } from "../../utils/api";
import {
  Baby,
  CalendarCheck,
  FlaskConical,
  Shield,
  ArrowLeft,
  Plus,
  Eye,
} from "lucide-react";

const ChildDetail = () => {
  const { hcc_number } = useParams();
  const [child, setChild] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchChild = async () => {
      try {
        const res = await exposedAPI.getChild(hcc_number);
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
    <div className="container-fluid" style={{ maxWidth: "1600px" }}>
      {/* Navbar */}
      <nav
        className="navbar navbar-expand-lg navbar-light bg-white shadow-sm"
        style={{ zIndex: 1030 }}
      >
        <div className="container-fluid">
          <span className="navbar-brand fw-bold">
            <Baby className="me-2" /> {child.child_name} ({child.hcc_number})
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
              {/* Visits Dropdown */}
              <li className="nav-item dropdown">
                <a
                  className="nav-link dropdown-toggle"
                  href="#"
                  id="visitsDropdown"
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  <CalendarCheck className="me-1" /> Visits
                </a>
                <ul className="dropdown-menu" aria-labelledby="visitsDropdown">
                  <li>
                    <Link
                      className="dropdown-item"
                      to={`/visits/add/${child.hcc_number}`}
                    >
                      <Plus className="me-2" size={16} />
                      Add Visit
                    </Link>
                  </li>
                  <li>
                    <Link
                      className="dropdown-item"
                      to={`/visits/${child.hcc_number}`}
                    >
                      <Eye className="me-2" size={16} />
                      View Visits
                    </Link>
                  </li>
                </ul>
              </li>

              {/* HTS Samples Dropdown */}
              <li className="nav-item dropdown">
                <a
                  className="nav-link dropdown-toggle"
                  href="#"
                  id="htsDropdown"
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  <FlaskConical className="me-1" /> HTS Samples
                </a>
                <ul className="dropdown-menu" aria-labelledby="htsDropdown">
                  <li>
                    <Link
                      className="dropdown-item"
                      to={`/hts/add/${child.hcc_number}`}
                    >
                      <Plus className="me-2" size={16} />
                      Add HTS Sample
                    </Link>
                  </li>
                  <li>
                    <Link
                      className="dropdown-item"
                      to={`/hts/${child.hcc_number}`}
                    >
                      <Eye className="me-2" size={16} />
                      View HTS Samples
                    </Link>
                  </li>
                </ul>
              </li>

              {/* Admin dropdown if needed */}
              {/* <li className="nav-item dropdown">
                <a
                  className="nav-link dropdown-toggle"
                  href="#"
                  id="adminDropdown"
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  <Shield className="me-1" /> Admin
                </a>
                <ul className="dropdown-menu" aria-labelledby="adminDropdown">
                  <li><Link className="dropdown-item" to="#">Action</Link></li>
                  <li><Link className="dropdown-item" to="#">Another action</Link></li>
                </ul>
              </li> */}
            </ul>

            <Link
              className="btn btn-outline-secondary"
              to="/exposed-infants/children"
            >
              <ArrowLeft className="me-2" /> Back to List
            </Link>
          </div>
        </div>
      </nav>

      {/* Child Info */}
      <div className="card shadow mb-4 mt-4">
        <div className="card-header bg-primary text-white">
          <h3 className="card-title mb-0">
            <Baby className="me-2" />
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
          <div className="d-flex justify-content-between align-items-center">
            <h3 className="card-title mb-0">
              <CalendarCheck className="me-2" />
              Visit History
            </h3>
            <Link
              to={`/visits/add/${child.hcc_number}`}
              className="btn btn-light btn-sm"
            >
              <Plus className="me-1" size={16} />
              Add Visit
            </Link>
          </div>
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
            <div className="alert alert-info text-center">
              <CalendarCheck className="me-2" />
              No visits recorded yet.{" "}
              <Link
                to={`/visits/add/${child.hcc_number}`}
                className="alert-link"
              >
                Add the first visit
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChildDetail;
