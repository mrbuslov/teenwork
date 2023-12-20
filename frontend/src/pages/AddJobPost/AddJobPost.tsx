import React, { ChangeEvent, useRef, useState } from 'react'
import { Formik, Field, Form, FormikHelpers, FormikProps } from 'formik';
import Input from '../../components/Input/Input';
import BorderBox from '../../components/BorderBox/BorderBox'
import ImagesDragger from '../../components/JobPostAdd/ImagesDragger/ImagesDragger';
import JobPostBlank from '../../components/JobPostAdd/JobPostBlank/JobPostBlank';
import classes from './AddJobPost.module.scss';
import * as Yup from 'yup';
import { AGES, CURRENCIES, EMPLOYMENT_TYPES, SERVER_ENDPOINT } from '../../consts/consts';


const JopPostSchema = Yup.object().shape({
  title: Yup.string().min(4, 'Title is too short').max(200, 'Title is too long').required('Required'),
  rubric: Yup.string(),
  age: Yup.number(),
  city: Yup.string(),
  price: Yup.number(),
  currency: Yup.string(),
  workersNum: Yup.number(),
  description: Yup.string(),
  userName: Yup.string(),
  userPhone: Yup.string(),
  userEmail: Yup.string(),
})


const AddJobPost = () => {
  const [descriptionWordsCount, setDescriptionWordsCount] = useState(0)
  const [images, setImages] = useState<File[]>([])
  const MAX_DESC_WORDS_NUM = 5000;
  const formInitialValues = { 
    images: images,
    title: '',
    rubric: EMPLOYMENT_TYPES[0],
    age: AGES[0],
    city: '',
    price: 0,
    currency: CURRENCIES[0], 
    workersNum: 0,
    description: '',
    userName: '',
    userPhone: '',
    userEmail: '',
  }

  return (
    <div className={classes.container}>
      <h1 className={classes.pageTitle}>Let's add a job post</h1>
      <h3 className={classes.pageNote}>This post will be active for 24 hours and then we will unfortunately delete it. <br />
      To publish permanent posts you need to sign up for free .</h3>
      <Formik
        initialValues={formInitialValues}
        validationSchema={JopPostSchema}
        onSubmit={(values, actions) => {
          console.log('images', images)
          alert(JSON.stringify(values, null, 2));
          actions.setSubmitting(false);
        }}
      >
        {props => (
          <form onSubmit={props.handleSubmit} className={classes.formMain}>
            <BorderBox label="Let's start by uploading up to 3 photos">
              <ImagesDragger images={images} setImages={(imgsList: File[]) => {
                props.setFieldValue('images', imgsList);
                setImages(imgsList);
              }} />
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
                errors={{
                  title: props.touched.title ? props.errors.title! : '',
                }}
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
            <BorderBox label="Let's describe your job offer">
              <div style={{position: 'relative'}}>
                <textarea 
                  name='description'
                  value={props.values.description}
                  className={classes.description}
                  onChange={(e: ChangeEvent<HTMLTextAreaElement>) => {
                    if (e.target.value.length <= MAX_DESC_WORDS_NUM){
                      props.handleChange(e)
                      setDescriptionWordsCount(e.target.value.length)
                    }
                  }}   
                  placeholder='I suggest you write the address, location, working conditions and much more...'
                ></textarea>
                <span className={classes.descWordsCounter}>{descriptionWordsCount}/{MAX_DESC_WORDS_NUM}</span>
              </div>
            </BorderBox>
            <BorderBox label="Tell us a little about yourself">
              <div className={classes.userInfo}>
                <div className={classes.userInfoPart}>
                  <span>How can people name you?</span>
                  <Input
                    fontSize='medium'
                    value={props.values.userName}
                    name='userName'   
                    onChange={props.handleChange}     
                  /> 
                </div>
                <div className={classes.userInfoPart}>
                  <span>Your phone number</span>
                  <Input
                    fontSize='medium'
                    value={props.values.userPhone}
                    name='userPhone'   
                    onChange={props.handleChange}     
                  /> 
                </div>
                <div className={classes.userInfoPart}>
                  <span>Your email (optional)</span>
                  <Input
                    fontSize='medium'
                    value={props.values.userEmail}
                    name='userEmail'   
                    onChange={props.handleChange}     
                  /> 
                </div>
              </div>
            </BorderBox>
            <button type="submit" className={classes.submitBtn}>Submit</button>
          </form>
        )}
      </Formik>
    </div>
  )
}

export default AddJobPost
