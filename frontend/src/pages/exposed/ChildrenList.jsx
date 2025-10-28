import React, { useState, useEffect, useRef, useLayoutEffect } from "react";
import PaginatedTable from "../../components/PaginatedTable";
import { exposedAPI } from "../../utils/api";
import Loader from "../../components/Loader";
import { useNavigate } from "react-router-dom";
import ChildForm from "../../components/children/ChildForm";

const ChildrenList = () => {
  const [filters, setFilters] = useState({
    search_value: "",
    search_by: "",
  });

  const [tableData, setTableData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState([]);
  const [errors, setErrors] = useState([]);
  const [creating, setCreating] = useState(false);
  const [formData, setFormData] = useState({
    search_by: "hcc",
    search: "",
  });

  const navigate = useNavigate();

  const columns = [
    { header: "HCC Number", accessor: "hcc_number" },
    { header: "Child Name", accessor: "name" },
    { header: "Gender", accessor: "gender" },
    { header: "Mother ARV#", accessor: "mother_art" },
    { header: "DOB", accessor: "dob" },
    { header: "Guardian", accessor: "guardian" },
    { header: "Relationship", accessor: "relationship" },
  ];
  const searchRef = useRef(null);

  useEffect(() => {
    const fetchChildren = async () => {
      try {
        setLoading(true);
        const res = await exposedAPI.getChildren(filters);
        let data = [];
        data = res.data;

        data = data.map((child) => ({
          id: child.hcc_number,
          hcc_number: child.hcc_number,
          name: child.child_name,
          gender: child.child_gender,
          mother_art: child.mother_art_number,
          dob: child.child_dob,
          guardian: child.guardian_name,
          relationship: child.relationship,
        }));

        setTableData(data);
      } catch (err) {
        console.error("Error fetching dashboard:", err);
        setError("Failed to load dashboard data");
      } finally {
        setLoading(false);
      }
    };

    fetchChildren();
  }, [filters]);

  useLayoutEffect(() => {
    if (!loading && searchRef.current) {
      searchRef.current.focus();
    }
  }, [loading, tableData]);

  const handleView = (row) => alert(`Viewing ${row.name}`);
  const handleEdit = (row) => alert(`Editing ${row.name}`);
  const handleDelete = (row) => alert(`Deleting ${row.name}`);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);
      const res = await exposedAPI.getChildren(formData);
      const data = res.data.map((child) => ({
        id: child.hcc_number,
        hcc_number: child.hcc_number,
        name: child.child_name,
        gender: child.child_gender,
        mother_art: child.mother_art_number,
        dob: child.child_dob,
        guardian: child.guardian_name,
        relationship: child.relationship,
      }));
      setTableData(data);
    } catch (err) {
      console.error("Error fetching dashboard:", err);
      setError("Failed to load dashboard data");
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    console.log(value);

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

  if (loading) {
    return (
      <div>
        <Loader text="Loading children...." />
      </div>
    );
  }

  if (creating) {
    return <ChildForm />;
  }
  return (
    <>
      <div className="container mt-4">
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h2>Children Management</h2>
          <button
            onClick={() => {
              navigate("/exposed-infants/children/create");
            }}
            className="btn btn-primary"
          >
            Add New Child
          </button>
        </div>

        <form onSubmit={handleSubmit} method="post" className="row g-3 mb-4">
          <div className="col-md-4">
            <select
              id="id_search_by"
              name="search_by"
              className="form-select"
              required
              value={formData.search_by}
              onChange={handleInputChange}
            >
              <option value="hcc">HCC Number</option>
              <option value="mother_art">Mother ART Number</option>
            </select>
          </div>
          <div className="col-md-5">
            <input
              className="form-control"
              type="number"
              name="search"
              value={formData.search}
              onChange={handleInputChange}
              ref={searchRef}
            />
          </div>
          <div className="col-md-3">
            <button type="submit" className="btn btn-success w-100">
              Search
            </button>
          </div>
        </form>

        <div className="card-header bg-white">
          <h5 id="table_title" className="card-title mb-0">
            Attendance List
          </h5>
        </div>
        <hr />
        <div className="card-body">
          <div className="table-responsive">
            <PaginatedTable
              data={tableData}
              columns={columns}
              rowsPerPage={5}
              onView={handleView}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />
          </div>
        </div>
      </div>
    </>
  );
};

export default ChildrenList;
