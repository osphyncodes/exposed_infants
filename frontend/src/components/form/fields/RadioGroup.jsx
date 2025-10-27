// components/Form/Fields/RadioGroup.js
import React from "react";

export default function RadioGroup({
  label,
  name,
  value = "",
  options = [],
  error,
  required = false,
  disabled = false,
  onChange,
  onBlur,
  onFocus,
  className = "",
  wrapperClassName = "",
  labelClassName = "",
  radioClassName = "",
  errorClassName = "",
  ...radioProps
}) {
  const handleChange = (optionValue, event) => {
    if (onChange) {
      onChange(optionValue, event);
    }
  };

  return (
    <div className={`form-field radio-group ${wrapperClassName}`}>
      {label && (
        <label className={`radio-group-label ${labelClassName}`}>
          {label}
          {required && <span className="required">*</span>}
        </label>
      )}

      <div className="radio-options">
        {options.map((option) => (
          <label key={option.value} className="radio-option">
            <input
              type="radio"
              name={name}
              value={option.value}
              checked={value === option.value}
              onChange={(e) => handleChange(option.value, e)}
              onBlur={onBlur}
              onFocus={onFocus}
              required={required}
              disabled={disabled || option.disabled}
              className={`form-check-input ${radioClassName}`}
              {...radioProps}
            />
            <span className="radio-text">{option.label}</span>
          </label>
        ))}
      </div>

      {error && <div className={`form-error ${errorClassName}`}>{error}</div>}
    </div>
  );
}
