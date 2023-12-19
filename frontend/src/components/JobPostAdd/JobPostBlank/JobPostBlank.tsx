import { Link } from 'react-router-dom'
import classes from './JobPostBlank.module.scss'
import FullHeart from '../../../assets/img/full_heart.svg';
import { ChangeEvent, useEffect, useState } from 'react';
import classNames from 'classnames';
import Input from '../../Input/Input';
import Select from '../../Select/Select';
import { AGES, CURRENCIES, EMPLOYMENT_TYPES, SERVER_ENDPOINT } from '../../../consts/consts';
import axios from 'axios';

export interface JobPostProps {
    titleDefaultValue: string;
    rubricDefaultValue: string;
    ageDefaultValue: number;
    cityDefaultValue: string;
    priceDefaultValue: number;
    currencyDefaultValue: string;

    onChange: (e: ChangeEvent<any>) => void;
    setFieldValue: (f_name: string, f_value: any) => void;
}  


const sortCitiesByValue = (value: string, citiesList: string[]) => {
    return citiesList.filter((city) => city.toLowerCase().includes(value.toLowerCase()))
}


const JobPostBlank = (jobPost: JobPostProps) => {
    const [uaCities, setUaCities] = useState<string[]>([]);
    const [uaCitiesDropdownOptions, setUaCitieDropdownOptions] = useState<string[]>([]);
    useEffect(() => {
        const getCities = async () => {
            // TODO: move to services
            const { data } = await axios.get(SERVER_ENDPOINT + '/api/ua_cities/')
            const citiesNames = data.cities.map((c: any) => c.city).sort()
            setUaCities(citiesNames)
        }
        getCities();
    }, [])

    const handleCitiesChange = (e: ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        jobPost.setFieldValue('city', value)
        if (!value) {
            setUaCitieDropdownOptions([])
            return
        }
        setUaCitieDropdownOptions(sortCitiesByValue(value, uaCities))
    }

    const handleOptionClick = (e: ChangeEvent<HTMLInputElement>) => {
        const value = e.target.textContent;
        console.log('option val', value)
        jobPost.setFieldValue('city', value)
        setUaCitieDropdownOptions([])
    }

    const handleCitiesClick = (e: ChangeEvent<HTMLInputElement>, action: 'open' | 'close') => {
        const value = e.target.value;
        console.log(value, action)
        if (action == 'open'){
            setUaCitieDropdownOptions(sortCitiesByValue(value, uaCities))
        }
        else {
            setUaCitieDropdownOptions([])
        }
    }

    return (
        <>
            <div className={classes.jobPost}>
                <div className={classes.container}>
                    <div className={classes.imageBlock}>
                        There <br /> will be <br /> a photo
                    </div>
                    <div className={classes.info}>
                        <span className={classes.nameBlock}>
                            <Input 
                                fontSize='large' 
                                className={classes.name} 
                                value={jobPost.titleDefaultValue}
                                onChange={jobPost.onChange}
                                name='title'
                                placeholder="Enter what we're going to do"
                            />
                            <span className={classes.salary}>
                                <Input 
                                    fontSize='large' 
                                    className={classes.price} 
                                    value={jobPost.priceDefaultValue}
                                    onChange={jobPost.onChange}
                                    name='price'
                                    placeholder='Pay'
                                />
                                <Select
                                    options={CURRENCIES}
                                    value={jobPost.currencyDefaultValue}
                                    className={classes.currency} 
                                    onChange={jobPost.onChange}
                                    name='currency'
                                />
                            </span>
                        </span> 
                        <div className={classes.additionalBlock}>
                            <span>
                                Age (from): &nbsp;
                                <Select
                                    options={AGES}
                                    value={jobPost.ageDefaultValue}
                                    className={classes.age} 
                                    onChange={jobPost.onChange}
                                    name='age'
                                />
                                &nbsp;
                                years.
                            </span>
                            <span className={classes.rubric}>
                                Type of employment:    
                                <Select
                                    value={jobPost.rubricDefaultValue}
                                    options={EMPLOYMENT_TYPES}
                                    className={classes.emplType} 
                                    onChange={jobPost.onChange}
                                    name='age'
                                />
                            </span>
                            <span>
                                <Input 
                                    fontSize='medium' 
                                    className={classes.city} 
                                    value={jobPost.cityDefaultValue}
                                    onChange={handleCitiesChange}
                                    // onBlur={(e: any) => handleCitiesClick(e, 'close')}
                                    onClick={(e: any) => handleCitiesClick(e, 'open')}
                                    name='city'
                                    placeholder='Enter city'
                                    dropdownOptions={uaCitiesDropdownOptions}
                                    handleOptionClick={handleOptionClick}
                                />
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default JobPostBlank
