import React, { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { exposedAPI } from "../../utils/api";
import Loader from "../../components/Loader";
import { ArrowLeft, Save, Upload, FileText, X } from "lucide-react";

const ChildForm = () => {
  const { hcc_number } = useParams();
  const navigate = useNavigate();
  const isEdit = Boolean(hcc_number);

  console.log(hcc_number);

  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [subjects, setSubjects] = useState([]);
  const [categories, setCategories] = useState([]);
  const [formData, setFormData] = useState({
    hcc_number: "",
    child_name: "",
    child_dob: "",
    child_gender: "",
    child_birth_weight: "",
    guardian_name: "",
    relationship: "",
    guardian_phone: "",
    physical_address: "",
    agrees_to_fup: "Yes",
    mother_status: "Alive OnART",
    mother_art_number: "",
    mother_art_start_date: "",
  });
  const [errors, setErrors] = useState({});

  useEffect(() => {
    fetchInitialData();
  }, [hcc_number]);

  const fetchInitialData = async () => {
    try {
      setLoading(true);

      if (isEdit) {
        const childRes = await exposedAPI.getChild(hcc_number);
        const child = childRes.data;
        setFormData({
          hcc_number: child.hcc_number,
          child_name: child.child_name,
          child_dob: child.child_dob,
          child_gender: child.child_gender,
          child_birth_weight: child.child_birth_weight,
          guardian_name: child.guardian_name,
          relationship: child.relationship,
          guardian_phone: child.guardian_phone,
          physical_address: child.physical_address,
          agrees_to_fup: child.agrees_to_fup,
          mother_status: child.mother_status,
          mother_art_number: child.mother_art_number,
          mother_art_start_date: child.mother_art_start_date,
        });
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      alert("Failed to load form data");
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: "",
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.hcc_number) newErrors.hcc_number = "HCC Number is required";
    if (!formData.child_name.trim())
      newErrors.child_name = "Child name is required";
    if (!formData.child_dob)
      newErrors.child_dob = "Child Date of birth is required";
    if (!formData.child_gender.trim())
      newErrors.child_gender = "Child sex is required";
    if (formData.child_birth_weight < 0) {
      newErrors.child_birth_weight = "Please enter a valid birth weight";
    }
    if (!formData.guardian_name)
      newErrors.guardian_name = "Guardian name is required";
    if (!formData.relationship)
      newErrors.relationship = "Relationship is required";
    if (!formData.physical_address)
      newErrors.physical_address = "Physical address is required";
    if (!formData.agrees_to_fup)
      newErrors.agrees_to_fup = "Agrees to follow-up is required";

    setErrors(newErrors);

    console.log(errors.hcc_number);

    console.log(Object.keys(newErrors).length === 0);

    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setSaving(true);
    try {
      if (isEdit) {
        console.log("Updating child:", JSON.stringify(formData));
        await exposedAPI.updateChild(hcc_number, formData, {
          headers: { "Content-Type": "application/json" },
        });
        alert("Child updated successfully!");
      } else {
        // For create, you can still use JSON (no need for FormData unless uploading files)
        await exposedAPI.createChild(formData, {
          headers: { "Content-Type": "application/json" },
        });
        alert("Child created successfully!");
      }

      navigate("/admin/papers");
    } catch (error) {
      console.error("Error saving child:", error);
      const errorMsg = error.response?.data || "Failed to save child";
      alert(typeof errorMsg === "object" ? JSON.stringify(errorMsg) : errorMsg);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <Loader text="Loading form..." />;
  }

  return (
    <div>
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <button
            className="btn btn-outline-secondary btn-sm me-3"
            onClick={() => navigate("/exposed-infants/children")}
          >
            <ArrowLeft size={16} />
          </button>
          <h4 className="d-inline-block mb-0">
            {isEdit ? "Edit Child" : "Create New Child"}
          </h4>
        </div>
        <button
          className="btn btn-primary"
          onClick={handleSubmit}
          disabled={saving}
        >
          {saving ? (
            <div
              className="spinner-border spinner-border-sm me-2"
              role="status"
            >
              <span className="visually-hidden">Loading...</span>
            </div>
          ) : (
            <Save size={18} className="me-2" />
          )}
          {isEdit ? "Update Paper" : "Create Paper"}
        </button>
      </div>

      <div className="row">
        <div className="col-lg-12">
          <div className="card shadow-sm">
            <div className="card-body">
              <form
                className="row g-3 shadow p-4 bg-light rounded"
                onSubmit={handleSubmit}
              >
                {/* Basic Child Info */}
                <div className="col-md-6">
                  <label className="form-label">HCC Number</label>
                  <input
                    type="number"
                    name="hcc_number"
                    className="form-control"
                    value={formData.hcc_number}
                    onChange={handleInputChange}
                  />

                  {errors.hcc_number && (
                    <div className="invalid-feedback">{errors.hcc_number}</div>
                  )}
                </div>

                <div className="col-md-6">
                  <label className="form-label">Child Name</label>
                  <input
                    type="text"
                    name="child_name"
                    className="form-control"
                    value={formData.child_name}
                    onChange={handleInputChange}
                  />
                </div>

                <div className="col-md-6">
                  <label className="form-label">Date of Birth</label>
                  <input
                    type="date"
                    name="child_dob"
                    className="form-control"
                    value={formData.child_dob}
                    onChange={handleInputChange}
                  />
                </div>

                <div className="col-md-6">
                  <label className="form-label">Gender</label>
                  <select
                    name="child_gender"
                    className="form-select"
                    value={formData.child_gender}
                    onChange={handleInputChange}
                  >
                    <option value="">Select Gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                  </select>
                </div>

                <div className="col-md-6">
                  <label className="form-label">Birth Weight (kg)</label>
                  <input
                    type="number"
                    step="0.01"
                    name="child_birth_weight"
                    className="form-control"
                    value={formData.child_birth_weight}
                    onChange={handleInputChange}
                  />
                </div>

                {/* Guardian Info */}
                <div className="col-md-6">
                  <label className="form-label">Guardian Name</label>
                  <input
                    type="text"
                    name="guardian_name"
                    className="form-control"
                    value={formData.guardian_name}
                    onChange={handleInputChange}
                  />
                </div>

                <div className="col-md-6">
                  <label className="form-label">Relationship</label>
                  <input
                    type="text"
                    name="relationship"
                    className="form-control"
                    value={formData.relationship}
                    onChange={handleInputChange}
                  />
                </div>

                <div className="col-md-6">
                  <label className="form-label">Guardian Phone</label>
                  <input
                    type="tel"
                    name="guardian_phone"
                    className="form-control"
                    value={formData.guardian_phone}
                    onChange={handleInputChange}
                    placeholder="e.g., +265..."
                  />
                </div>

                <div className="col-12">
                  <label className="form-label">Physical Address</label>
                  <textarea
                    name="physical_address"
                    className="form-control"
                    rows="2"
                    value={formData.physical_address}
                    onChange={handleInputChange}
                  />
                </div>

                {/* Mother Info */}
                <div className="col-md-6">
                  <label className="form-label">Agrees to FUP?</label>
                  <select
                    name="agrees_to_fup"
                    className="form-select"
                    value={formData.agrees_to_fup}
                    onChange={handleInputChange}
                  >
                    <option value="">Select</option>
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                  </select>
                </div>

                <div className="col-md-6">
                  <label className="form-label">Mother Status</label>
                  <select
                    name="mother_status"
                    className="form-select"
                    value={formData.mother_status}
                    onChange={handleInputChange}
                  >
                    <option value="">Select Status</option>
                    <option value="Alive No ART">Alive No ART</option>
                    <option value="Alive OnART">Alive OnART</option>
                    <option value="Died">Died</option>
                    <option value="Unknown">Unknown</option>
                  </select>
                </div>

                <div className="col-md-6">
                  <label className="form-label">Mother ART Number</label>
                  <input
                    type="text"
                    name="mother_art_number"
                    className="form-control"
                    value={formData.mother_art_number}
                    onChange={handleInputChange}
                  />
                </div>

                <div className="col-md-6">
                  <label className="form-label">ART Start Date</label>
                  <input
                    type="date"
                    name="mother_art_start_date"
                    className="form-control"
                    value={formData.mother_art_start_date}
                    onChange={handleInputChange}
                  />
                </div>

                {/* Buttons */}
                <div className="col-12 text-end">
                  <button type="submit" className="btn btn-primary">
                    Save Child
                  </button>
                  <button
                    type="button"
                    className="btn btn-secondary ms-2"
                    onClick={() => window.history.back()}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChildForm;
