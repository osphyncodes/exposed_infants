import React from 'react'

const Loader = ({ size = 'md', text = 'Loading...' }) => {
  const sizeClass = {
    sm: 'spinner-border-sm',
    md: '',
    lg: 'spinner-border-lg'
  }

  return (
    <div className="d-flex flex-column align-items-center justify-content-center p-4">
      <div className={`spinner-border ${sizeClass[size]} text-primary`} role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      {text && <p className="mt-2 text-muted">{text}</p>}
    </div>
  )
}

export default Loader