// components/Form/Fields/SelectField.js
import React from "react";

export default function SelectField({
  label,
  name,
  value = "",
  options = [],
  placeholder = "Select an option",
  error,
  required = false,
  disabled = false,
  onChange,
  onBlur,
  onFocus,
  className = "",
  wrapperClassName = "",
  labelClassName = "",
  selectClassName = "",
  errorClassName = "",
  ...selectProps
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

      <select
        id={name}
        name={name}
        value={value}
        onChange={handleChange}
        onBlur={onBlur}
        onFocus={onFocus}
        required={required}
        disabled={disabled}
        className={`form-select ${error ? "error" : ""} ${selectClassName}`}
        {...selectProps}
      >
        <option value="">{placeholder}</option>
        {options.map((option) => (
          <option
            key={option.value}
            value={option.value}
            disabled={option.disabled}
          >
            {option.label}
          </option>
        ))}
      </select>

      {error && <div className={`form-error ${errorClassName}`}>{error}</div>}
    </div>
  );
}
