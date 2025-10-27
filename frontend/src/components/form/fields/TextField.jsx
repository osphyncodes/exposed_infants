// components/Form/Fields/TextField.js
import React from "react";

export default function TextField({
  label,
  name,
  type = "text",
  value = "",
  placeholder = "",
  error,
  required = false,
  disabled = false,
  readOnly = false,
  autoComplete = "on",
  onChange,
  onBlur,
  onFocus,
  className = "",
  wrapperClassName = "",
  labelClassName = "",
  inputClassName = "",
  errorClassName = "",
  ...inputProps
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
        type={type}
        id={name}
        name={name}
        value={value}
        placeholder={placeholder}
        onChange={handleChange}
        onBlur={onBlur}
        onFocus={onFocus}
        required={required}
        disabled={disabled}
        readOnly={readOnly}
        autoComplete={autoComplete}
        className={`form-control ${error ? "error" : ""} ${inputClassName}`}
        {...inputProps}
      />

      {error && <div className={`form-error ${errorClassName}`}>{error}</div>}
    </div>
  );
}
