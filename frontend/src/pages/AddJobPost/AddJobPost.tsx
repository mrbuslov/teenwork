import React from 'react'
import { Formik, Field, Form, FormikHelpers, FormikProps } from 'formik';
import classes from './AddJobPost.module.scss';
import Input from '../../components/Input/Input';
import BorderBox from '../../components/BorderBox/BorderBox'
import ImagesDragger from '../../components/JobPostAdd/ImagesDragger/ImagesDragger';

interface Values {
  firstName: string;
  lastName: string;
  email: string;
}

const AddJobPost = () => {
  return (
    <div className={classes.container}>
      <h1 className={classes.pageTitle}>Let's add a job post</h1>
      <h3 className={classes.pageNote}>This post will be active for 24 hours and then we will unfortunately delete it. <br />
      To publish permanent posts you need to sign up for free .</h3>
      <Formik
        initialValues={{ firstName: 'jared' }}
        onSubmit={(values, actions) => {
          setTimeout(() => {
            alert(JSON.stringify(values, null, 2));
            actions.setSubmitting(false);
          }, 1000);
        }}
      >
        {props => (
          <form onSubmit={props.handleSubmit} className={classes.formMain}>
            <BorderBox label="Let's start by uploading up to 3 photos">
              <ImagesDragger />
            </BorderBox>
            <BorderBox label='Label'>
              <Input
                fontSize='medium'
                value={props.values.firstName}
                onBlur={props.handleBlur}
                name='firstName'   
                onChange={props.handleChange}     
              />
            </BorderBox>
            <button type="submit">Submit</button>
          </form>
        )}
      </Formik>
        {/* <Formik 
        initialValues={{ email: '', color: 'red', firstName: '', lastName: '' }}
        onSubmit={(values, actions) => {
          alert(JSON.stringify(values, null, 2));
          actions.setSubmitting(false);
        }}
      >
        {(props: FormikProps<any>) => (
          <Form>
            <h1 className={classes.title}>Let's add a JOB POST!</h1>
            <h3 className={classes.title}>This ad will be active for 24 hours, and then, unfortunately, we will delete it.<br/>
            To publish permanent posts, you should sign up for free.</h3>
              <Field name="firstName">
              {({
                field, // { name, value, onChange, onBlur }
                form: { touched, errors }, // also values, setXXXX, handleXXXX, dirty, isValid, status, etc.
                meta,
              }: any) => (
                <div>
                  <Input
                    fontSize='medium'
                    value={props.values.name}
                    onBlur={props.handleBlur}
                    name='firstName'   
                    onChange={props.handleChange}     
                  />
                  {meta.touched && meta.error && (
                    <div className="error">{meta.error}</div>
                  )}
                </div>
              )}
            </Field>


            <label htmlFor="lastName">Last Name</label>
            <Field id="lastName" name="lastName" placeholder="Doe" />

            <label htmlFor="email">Email</label>
            <Field
              id="email"
              name="email"
              placeholder="john@acme.com"
              type="email"
            />

            <button type="submit">Submit</button>
          </Form>
        )}
      </Formik> */}

    </div>
  )
}

export default AddJobPost
