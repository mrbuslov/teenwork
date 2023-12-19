import React, {FC, PropsWithChildren, HTMLAttributes, ReactNode, ChangeEvent} from 'react'
import classNames from "classnames";
import classes from "./Input.module.scss";


interface InputProps {
  value: string | number;
  onChange: (e?: any) => void;
  handleOptionClick?: (e?: any) => void;
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
  ...props
}: InputProps) => (
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
)

const Input: FC<InputProps> = ({
  value,
  fontSize,
  onChange,
  dropdownOptions,
  handleOptionClick,
  isDisabled = false,
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


// import React from 'react';

// interface MyComponentProps {
//   name?: string;
//   [key: string]: any; // Allow any other prop
// }

// const Input: React.FC<MyComponentProps> = ({ name, ...otherProps }) => {
//   // You can use 'name' here as it's defined in the interface
//   // 'otherProps' will contain any other additional props passed to the component

//   return (
//     <div>
//       <p>Name: {name}</p>
//       {/* You can use otherProps here */}
//     </div>
//   );
// };

// export default Input;
