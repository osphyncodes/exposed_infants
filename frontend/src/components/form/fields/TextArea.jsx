// components/Form/Fields/TextArea.js
import React from "react";

export default function TextArea({
  label,
  name,
  value = "",
  placeholder = "",
  rows = 4,
  error,
  required = false,
  disabled = false,
  readOnly = false,
  onChange,
  onBlur,
  onFocus,
  className = "",
  wrapperClassName = "",
  labelClassName = "",
  textareaClassName = "",
  errorClassName = "",
  ...textareaProps
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

      <textarea
        id={name}
        name={name}
        value={value}
        placeholder={placeholder}
        rows={rows}
        onChange={handleChange}
        onBlur={onBlur}
        onFocus={onFocus}
        required={required}
        disabled={disabled}
        readOnly={readOnly}
        className={`form-control ${error ? "error" : ""} ${textareaClassName}`}
        {...textareaProps}
      />

      {error && <div className={`form-error ${errorClassName}`}>{error}</div>}
    </div>
  );
}
