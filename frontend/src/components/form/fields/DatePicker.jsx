// components/Form/Fields/DatePicker.js
import React from "react";

export default function DatePicker({
  label,
  name,
  value = "",
  error,
  required = false,
  disabled = false,
  onChange,
  onBlur,
  onFocus,
  className = "",
  wrapperClassName = "",
  labelClassName = "",
  inputClassName = "",
  errorClassName = "",
  ...dateProps
}) {
  const handleChange = (event) => {
    if (onChange) {
      onChange(event.target.value, event);
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
        type="date"
        id={name}
        name={name}
        value={value}
        onChange={handleChange}
        onBlur={onBlur}
        onFocus={onFocus}
        required={required}
        disabled={disabled}
        className={`form-input ${error ? "error" : ""} ${inputClassName}`}
        {...dateProps}
      />

      {error && <div className={`form-error ${errorClassName}`}>{error}</div>}
    </div>
  );
}
