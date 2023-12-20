import React, {FC, PropsWithChildren, HTMLAttributes, ReactNode, ChangeEvent} from 'react'
import classNames from "classnames";
import classes from "./Input.module.scss";


interface InputProps {
  value: string | number;
  onChange: (e?: any) => void;
  handleOptionClick?: (e?: any) => void;
  error?: any;
  fontSize: "small" | "medium" | "large";
  isDisabled?: boolean;
  dropdownOptions?: (string | number)[]; // if user should select from options
  [key: string]: any; // ...props
}

const calculateFontSize = (fontSize: string) => {
  switch (fontSize) {
    case 'small':
      return'0.5rem'
      case 'medium':
        return'1rem'
    case 'large':
      return'1.5rem'
    default:
      return '1rem'
  }
}

const InputNode = ({
  value,
  fontSize,
  onChange,
  dropdownOptions,
  isDisabled,
  error,
  ...props
}: InputProps) => (
  <>
    <input
      {...props}
      className={classNames(
        classes.input,
        props.className
      )}
      style={{
        fontSize: calculateFontSize(fontSize)
      }}
      value={Boolean(value) ? value : ''}
      disabled={isDisabled}
      onChange={onChange}
    />
    {/* <span style={{position: 'absolute', top: '1rem', fontSize: '0.75rem'}}>{error}</span> */}
  </>
)

const Input: FC<InputProps> = ({
  value,
  fontSize,
  onChange,
  dropdownOptions,
  handleOptionClick,
  isDisabled = false,
  error,
  ...props
}) => {
  return (
    <>
      {!dropdownOptions? 
        <InputNode 
          value={value}
          fontSize={fontSize}
          onChange={onChange}
          isDisabled={isDisabled}
          error={error}
          {...props}
        />
        :
        <span style={{position: 'relative'}}>
          <InputNode 
            value={value}
            fontSize={fontSize}
            onChange={onChange}
            dropdownOptions={dropdownOptions}
            isDisabled={isDisabled}
            error={error}
            {...props}
          />
          <ul className={classes.dropdownOptions}>
            {dropdownOptions.map((option, i) => 
              <li key={i} onClick={handleOptionClick} >{option}</li>
            )}
          </ul>
        </span>
      }
    </>
  )
}

export default Input
