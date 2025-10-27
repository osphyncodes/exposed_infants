// components/Form/Fields/FileUpload.js
import React from "react";

export default function FileUpload({
  label,
  name,
  error,
  required = false,
  disabled = false,
  accept,
  multiple = false,
  onChange,
  onBlur,
  onFocus,
  className = "",
  wrapperClassName = "",
  labelClassName = "",
  inputClassName = "",
  errorClassName = "",
  ...fileProps
}) {
  const handleChange = (event) => {
    if (onChange) {
      const files = multiple ? event.target.files : event.target.files[0];
      onChange(files, event);
    }
  };

  return (
    <div className={`form-field ${wrapperClassName}`}>
      {label && (
        <label htmlFor={name} className={`form-label ${labelClassName}`}>
          {label}
          {required && <span className="required">*</span>}
        </label>
      )}

      <input
        type="file"
        id={name}
        name={name}
        onChange={handleChange}
        onBlur={onBlur}
        onFocus={onFocus}
        required={required}
        disabled={disabled}
        accept={accept}
        multiple={multiple}
        className={`form-input file-input ${
          error ? "error" : ""
        } ${inputClassName}`}
        {...fileProps}
      />

      {error && <div className={`form-error ${errorClassName}`}>{error}</div>}
    </div>
  );
}
