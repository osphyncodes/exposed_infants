// components/Form/Fields/Checkbox.js
import React from "react";

export default function Checkbox({
  label,
  name,
  checked = false,
  error,
  required = false,
  disabled = false,
  onChange,
  onBlur,
  onFocus,
  className = "",
  wrapperClassName = "",
  labelClassName = "",
  checkboxClassName = "",
  errorClassName = "",
  ...checkboxProps
}) {
  const handleChange = (event) => {
    if (onChange) {
      onChange(event.target.checked, event);
    }
  };

  return (
    <div className={`form-field checkbox-field ${wrapperClassName}`}>
      <label className={`checkbox-label ${labelClassName}`}>
        <input
          type="checkbox"
          name={name}
          checked={checked}
          onChange={handleChange}
          onBlur={onBlur}
          onFocus={onFocus}
          required={required}
          disabled={disabled}
          className={`form-check-input ${checkboxClassName}`}
          {...checkboxProps}
        />
        <span className="checkbox-text">
          {label}
          {required && <span className="required">*</span>}
        </span>
      </label>

      {error && <div className={`form-error ${errorClassName}`}>{error}</div>}
    </div>
  );
}
