import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { exposedAPI } from "../../utils/api";

const ChildVisit = () => {
  const { hcc_number } = useParams();
  const navigate = useNavigate();

  const [child, setChild] = useState(null);
  const [visits, setVisits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [messages, setMessages] = useState([]);
  const [user, setUser] = useState({ is_superuser: false }); // Replace with real auth state

  useEffect(() => {
    fetchVisits();
  }, [hcc_number]);

  const fetchVisits = async () => {
    try {
      const response = await exposedAPI.getChildVisits(hcc_number);
      if (!response.ok) throw new Error("Failed to fetch visits");

      const data = await response.json();
      setChild(data.child);
      setVisits(data.visits);
    } catch (error) {
      console.error("Error:", error);
      setMessages([{ text: "Error loading visits", type: "danger" }]);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (visitId) => {
    if (!window.confirm("Are you sure you want to delete this visit?")) return;

    try {
      const response = await fetch(
        `http://localhost:8000/api/exposed/visits/${visitId}/`,
        { method: "DELETE" }
      );

      if (response.ok) {
        setVisits(visits.filter((v) => v.id !== visitId));
        setMessages([{ text: "Visit deleted successfully", type: "success" }]);
      } else {
        setMessages([{ text: "Failed to delete visit", type: "warning" }]);
      }
    } catch (error) {
      console.error(error);
      setMessages([{ text: "Error deleting visit", type: "danger" }]);
    }
  };

  const calculateAgeInMonths = (dob, visitDate) => {
    if (!dob || !visitDate) return "N/A";
    const dobDate = new Date(dob);
    const visit = new Date(visitDate);
    const months =
      (visit.getFullYear() - dobDate.getFullYear()) * 12 +
      (visit.getMonth() - dobDate.getMonth());
    return months;
  };

  if (loading) return <p>Loading visits...</p>;

  return (
    <div className="container mt-4">
      {/* Alerts */}
      {messages.length > 0 && (
        <div className="container mt-3">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`alert alert-${msg.type} alert-dismissible fade show`}
              role="alert"
            >
              {msg.text}
              <button
                type="button"
                className="btn-close"
                data-bs-dismiss="alert"
                aria-label="Close"
              ></button>
            </div>
          ))}
        </div>
      )}

      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Child Dashboard - Visits ({visits.length})</h2>
        <div>
          {user.is_superuser && (
            <button
              className="btn btn-success me-2"
              onClick={() => navigate(`/children/${hcc_number}/add-visit`)}
            >
              Add Visit
            </button>
          )}
          <button
            className="btn btn-primary"
            onClick={() => navigate(`/children/${hcc_number}`)}
          >
            Back
          </button>
        </div>
      </div>

      <div className="card mb-4">
        <div className="card-header bg-secondary text-white">Visit History</div>
        <div className="card-body">
          {visits.length > 0 ? (
            <div className="table-responsive">
              <table className="table table-bordered table-striped table-hover">
                <thead className="table-secondary">
                  <tr>
                    <th>Age (months)</th>
                    <th>Visit Date</th>
                    <th>Height (cm)</th>
                    <th>Weight (kg)</th>
                    <th>MUAC (cm)</th>
                    <th>Wasting</th>
                    <th>Breastfeeding</th>
                    <th>Mother ART Status</th>
                    <th>Clinical Monitoring</th>
                    <th>HIV Testing</th>
                    <th>Infection Status</th>
                    <th>CPT Given</th>
                    <th>Follow-Up Outcome</th>
                    <th>Next Appointment</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {visits.map((visit) => (
                    <tr key={visit.id}>
                      <td>
                        {calculateAgeInMonths(
                          child?.child_dob,
                          visit.visit_date
                        )}
                      </td>
                      <td>{visit.visit_date}</td>
                      <td>{visit.height}</td>
                      <td>{visit.weight}</td>
                      <td>{visit.muac}</td>
                      <td>{visit.wasting}</td>
                      <td>{visit.breastfeeding}</td>
                      <td>{visit.mother_art_status}</td>
                      <td>{visit.clinical_monitoring}</td>
                      <td>{visit.hiv_testing}</td>
                      <td>{visit.infection_status}</td>
                      <td>{visit.cpt_given ? "Yes" : "No"}</td>
                      <td>{visit.follow_up_outcome}</td>
                      <td>{visit.next_appointment_or_outcome_date}</td>
                      <td>
                        <button
                          className="btn btn-sm btn-primary me-2"
                          onClick={() =>
                            navigate(
                              `/children/${hcc_number}/visits/${visit.id}/edit`
                            )
                          }
                        >
                          <i className="fas fa-edit"></i>
                        </button>
                        <button
                          className="btn btn-sm btn-warning"
                          onClick={() => handleDelete(visit.id)}
                        >
                          <i className="fas fa-trash"></i>
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p>No visits recorded yet.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChildVisit;
