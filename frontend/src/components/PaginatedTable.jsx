import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Eye, Edit, Trash2 } from "lucide-react"; // Lucide icons

const PaginatedTable = ({
  data = [],
  columns = [],
  rowsPerPage = 5,
  onEdit,
  onDelete,
  onView,
}) => {
  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = Math.ceil(data.length / rowsPerPage);

  const startIndex = (currentPage - 1) * rowsPerPage;
  const currentRows = data.slice(startIndex, startIndex + rowsPerPage);

  const handlePageChange = (page) => {
    if (page > 0 && page <= totalPages) setCurrentPage(page);
  };

  return (
    <div className="table-responsive">
      <table className="table table-hover table-bordered align-middle mt-3">
        <thead className="table-light">
          <tr>
            {columns.map((col) => (
              <th key={col.accessor}>{col.header}</th>
            ))}
            {(onEdit || onDelete || onView) && (
              <th className="text-center">Actions</th>
            )}
          </tr>
        </thead>
        <tbody>
          {currentRows.length > 0 ? (
            currentRows.map((row, index) => (
              <tr key={index}>
                {columns.map((col) => (
                  <td key={col.accessor}>{row[col.accessor]}</td>
                ))}
                {(onEdit || onDelete || onView) && (
                  <td className="text-center">
                    <div className="d-flex justify-content-center gap-2">
                      {onView && (
                        <button
                          className="btn btn-sm btn-outline-info"
                          onClick={() => onView(row)}
                          title="View"
                        >
                          <Eye size={16} />
                        </button>
                      )}
                      {onEdit && (
                        <button
                          className="btn btn-sm btn-outline-warning"
                          onClick={() => onEdit(row)}
                          title="Edit"
                        >
                          <Edit size={16} />
                        </button>
                      )}
                      {onDelete && (
                        <button
                          className="btn btn-sm btn-outline-danger"
                          onClick={() => onDelete(row)}
                          title="Delete"
                        >
                          <Trash2 size={16} />
                        </button>
                      )}
                    </div>
                  </td>
                )}
              </tr>
            ))
          ) : (
            <tr>
              <td
                colSpan={columns.length + 1}
                className="text-center text-muted py-3"
              >
                No records found
              </td>
            </tr>
          )}
        </tbody>
      </table>

      {/* Pagination Controls */}
      <nav>
        <ul className="pagination justify-content-center">
          {/* Previous */}
          <li className={`page-item ${currentPage === 1 ? "disabled" : ""}`}>
            <button
              className="page-link"
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
            >
              Previous
            </button>
          </li>

          {/* Always show first page */}
          <li className={`page-item ${currentPage === 1 ? "active" : ""}`}>
            <button
              className="page-link"
              onClick={() => {
                if (1 !== currentPage) handlePageChange(1);
              }}
            >
              1
            </button>
          </li>

          {/* Show ellipsis if there are pages between first and current-1 */}
          {currentPage > 3 && (
            <li className="page-item disabled">
              <span className="page-link">...</span>
            </li>
          )}

          {/* Show current page and surrounding pages */}
          {currentPage > 2 && (
            <li className="page-item">
              <button
                className="page-link"
                onClick={() => handlePageChange(currentPage - 1)}
              >
                {currentPage - 1}
              </button>
            </li>
          )}

          {/* Current page (if not first or last) */}
          {currentPage > 1 && currentPage < totalPages && (
            <li className="page-item active">
              <span className="page-link">{currentPage}</span>
            </li>
          )}

          {/* Show next page if not last */}
          {currentPage < totalPages - 1 && (
            <li className="page-item">
              <button
                className="page-link"
                onClick={() => handlePageChange(currentPage + 1)}
              >
                {currentPage + 1}
              </button>
            </li>
          )}

          {/* Show ellipsis if there are pages between current+1 and last */}
          {currentPage < totalPages - 2 && (
            <li className="page-item disabled">
              <span className="page-link">...</span>
            </li>
          )}

          {/* Always show last page if there is more than 1 page */}
          {totalPages > 1 && (
            <li
              className={`page-item ${
                currentPage === totalPages ? "active" : ""
              }`}
            >
              <button
                className="page-link"
                onClick={() => {
                  if (totalPages !== currentPage) handlePageChange(totalPages);
                }}
              >
                {totalPages}
              </button>
            </li>
          )}

          {/* Next */}
          <li
            className={`page-item ${
              currentPage === totalPages ? "disabled" : ""
            }`}
          >
            <button
              className="page-link"
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
            >
              Next
            </button>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default PaginatedTable;
