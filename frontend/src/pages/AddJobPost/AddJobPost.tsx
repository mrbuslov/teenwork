import React from 'react'
import { Formik, Field, Form, FormikHelpers, FormikProps } from 'formik';
import classes from './AddJobPost.module.scss';
import Input from '../../components/Input/Input';
import BorderBox from '../../components/BorderBox/BorderBox'
import ImagesDragger from '../../components/JobPostAdd/ImagesDragger/ImagesDragger';
import JobPostBlank from '../../components/JobPostAdd/JobPostBlank/JobPostBlank';


const AddJobPost = () => {
  return (
    <div className={classes.container}>
      <h1 className={classes.pageTitle}>Let's add a job post</h1>
      <h3 className={classes.pageNote}>This post will be active for 24 hours and then we will unfortunately delete it. <br />
      To publish permanent posts you need to sign up for free .</h3>
      <Formik
        initialValues={{ 
          title: '',
          rubric: '',
          age: 0,
          city: '',
          price: 0,
          currency: '', 
          workersNum: 0,
        }}
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
            <BorderBox label="Fill in all fields">
              <JobPostBlank
                titleDefaultValue={props.values.title}
                rubricDefaultValue={props.values.rubric}
                ageDefaultValue={props.values.age}
                cityDefaultValue={props.values.city}
                priceDefaultValue={props.values.price}
                currencyDefaultValue={props.values.currency}
                onChange={props.handleChange}
                setFieldValue={props.setFieldValue}
              />
              <div className={classes.workersNumBlock}>
                <span>How many people do you need</span>
                &nbsp;
                <span>(optional):</span>
                &nbsp;
                <Input
                  fontSize='medium'
                  value={props.values.workersNum}
                  className={classes.workersNum}
                  name='workersNum'   
                  onChange={props.handleChange}     
                /> 
              </div>
            </BorderBox>
            <button type="submit">Submit</button>
          </form>
        )}
      </Formik>
              {/* <Input
                fontSize='medium'
                value={props.values.firstName}
                onBlur={props.handleBlur}
                name='firstName'   
                onChange={props.handleChange}     
              /> */}
    </div>
  )
}

export default AddJobPost
