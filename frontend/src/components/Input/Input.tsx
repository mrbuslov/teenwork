import React, {FC, PropsWithChildren, HTMLAttributes, ReactNode} from 'react'
import classNames from "classnames";
import classes from "./Input.module.scss";


interface InputProps {
  value: string;
  fontSize: "small" | "medium" | "large";
  isDisabled?: boolean;
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

const Input: FC<InputProps> = ({
  value,
  fontSize,
  isDisabled = false,
  ...props
}) => {
  return (
    <input
      {...props}
      className={classNames(
        classes.input,
      )}
      style={{
        fontSize: calculateFontSize(fontSize)
      }}
      value={value}
      disabled={isDisabled}
    />
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
