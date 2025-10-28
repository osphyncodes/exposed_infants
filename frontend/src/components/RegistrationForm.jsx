import react from "react";
import React from "react";
import Form from "./form/form";

export default function RegistrationForm() {
  const [formData, setFormData] = React.useState({});
  const [errors, setErrors] = React.useState({});

  const registrationFields = [
    {
      type: "text",
      name: "firstName",
      label: "First Name",
      placeholder: "Enter your first name",
      required: true,
      autoComplete: "given-name",
    },
    {
      type: "text",
      name: "lastName",
      label: "Last Name",
      placeholder: "Enter your last name",
      required: true,
      autoComplete: "family-name",
    },
    {
      type: "email",
      name: "email",
      label: "Email Address",
      placeholder: "Enter your email",
      required: true,
      autoComplete: "email",
    },
    {
      type: "select",
      name: "country",
      label: "Country",
      options: [
        { value: "us", label: "United States" },
        { value: "ca", label: "Canada" },
        { value: "uk", label: "United Kingdom" },
      ],
      placeholder: "Select your country",
      required: true,
    },
    {
      type: "radio",
      name: "gender",
      label: "Gender",
      options: [
        { value: "male", label: "Male" },
        { value: "female", label: "Female" },
        { value: "other", label: "Other" },
      ],
      required: true,
    },
    {
      type: "textarea",
      name: "bio",
      label: "Biography",
      placeholder: "Tell us about yourself...",
      rows: 4,
    },
    {
      type: "checkbox",
      name: "terms",
      label: "I agree to the terms and conditions",
      required: true,
    },
  ];

  const handleChange = (name, value, event) => {
    const { names, type, checked } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: "" }));
    }
  };

  const handleSubmit = (values) => {
    // Handle form submission
  };

  return (
    <Form
      fields={registrationFields}
      values={formData}
      errors={errors}
      onChange={handleChange}
      onSubmit={handleSubmit}
      submitText="Register"
      className="registration-form"
    />
  );
}
