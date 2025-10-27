// components/Form/Form.js
import React from "react";
import TextField from "./fields/TextField";
import SelectField from "./fields/SelectField";
import TextArea from "./fields/TextArea";
import Checkbox from "./fields/CheckBox";
import RadioGroup from "./fields/RadioGroup";
import DatePicker from "./fields/DatePicker";
import FileUpload from "./fields/FileUpload";

const fieldComponents = {
  text: TextField,
  email: TextField,
  password: TextField,
  number: TextField,
  select: SelectField,
  textarea: TextArea,
  checkbox: Checkbox,
  radio: RadioGroup,
  date: DatePicker,
  file: FileUpload,
};

export default function Form({
  fields = [],
  onSubmit,
  onChange,
  onBlur,
  onFocus,
  values = {},
  errors = {},
  loading = false,
  submitText = "Submit",
  resetText = "Reset",
  showReset = true,
  className = "",
  formClassName = "",
  buttonClassName = "",
  fieldClassName = "",
  ...formProps
}) {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSubmit) {
      onSubmit(values, e);
    }
  };

  const handleChange = (name, value, event) => {
    if (onChange) {
      onChange(name, value, event);
    }
  };

  const handleBlur = (name, event) => {
    if (onBlur) {
      onBlur(name, event);
    }
  };

  const handleFocus = (name, event) => {
    if (onFocus) {
      onFocus(name, event);
    }
  };

  const renderField = (fieldConfig, index) => {
    const FieldComponent = fieldComponents[fieldConfig.type] || TextField;

    return (
      <FieldComponent
        key={fieldConfig.name || index}
        value={values[fieldConfig.name] || ""}
        error={errors[fieldConfig.name]}
        onChange={(value, event) =>
          handleChange(fieldConfig.name, value, event)
        }
        onBlur={(event) => handleBlur(fieldConfig.name, event)}
        onFocus={(event) => handleFocus(fieldConfig.name, event)}
        className={fieldClassName}
        {...fieldConfig}
      />
    );
  };

  return (
    <div className={`form-container ${className}`}>
      <form
        onSubmit={handleSubmit}
        className={`form ${formClassName}`}
        {...formProps}
      >
        {fields.map(renderField)}

        <div className="form-actions">
          <button
            type="submit"
            disabled={loading}
            className={`btn btn-primary ${buttonClassName}`}
          >
            {loading ? "Loading..." : submitText}
          </button>

          {showReset && (
            <button type="reset" className={`reset-button ${buttonClassName}`}>
              {resetText}
            </button>
          )}
        </div>
      </form>
    </div>
  );
}
