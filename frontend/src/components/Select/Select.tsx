import React from 'react'

interface Props {
  value?: string | number;
  options: (string | number)[];
  [key: string]: any;
}

const Select = ({
  value,
  options,
  ...props
}: Props) => {
  return (
    <select
      {...props}
    >
      {options.map((option, i) => 
        <option 
          key={i} 
          value={option}
          selected={value == option}
        >{option}</option>
      )}
    </select>
  )
}

export default Select
