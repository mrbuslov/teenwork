import React, {PropsWithChildren, FC, ReactNode, Children} from 'react'
import classes from "./BorderBox.module.scss";

interface Props {
  label?: string;
  children: ReactNode;
}

const BorderBox: FC<PropsWithChildren<Props>> = ({
  label,
  children
}) => {
  return (
    <div className={classes.box}>
      {label &&
        <span className={classes.label}>{label}</span>
      }
      {children}
    </div>
  )
}

export default BorderBox
