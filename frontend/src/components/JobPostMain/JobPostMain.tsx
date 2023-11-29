import { Link } from 'react-router-dom'
import classes from './JobPostMain.module.scss'
import FullHeart from '../../assets/img/full_heart.svg';
import EmptyHeart from '../../assets/img/heart.svg';
import { useState } from 'react';
import classNames from 'classnames';

export interface JobPostAuthor {
    profile_link: string
    name: string
    phone_number: string
    email: string
    is_official: boolean
}

export interface JobPostProps {
    id: number
    slug: string
    url: string
    title: string
    rubric: string
    image_link: string
    age: number
    city: string
    published_date: Date
    content: string
    price: number
    currency: string
    owner: JobPostAuthor
    is_added_to_favourites: boolean
}

interface Props {
    jobPost: JobPostProps
}

function returnJobPostDateString(datePublished: Date) {
    datePublished = new Date(datePublished);
    const dateToday = new Date();
    const dateYesterday = new Date();
    dateYesterday.setDate(dateYesterday.getDate() - 1);

    if (dateToday.toDateString() == datePublished.toDateString()) {
        return `Today at ${datePublished.getHours()}:${datePublished.getMinutes()}`
    }
    else if (dateYesterday.toDateString() == datePublished.toDateString()) {
        return `Yesterday at ${datePublished.getHours()}:${datePublished.getMinutes()}`
    }
    else {
        return datePublished.toLocaleString('en-GB', {weekday: 'short', month: 'short', day: 'numeric' })
    }
}

function toggleMoreInfoArrow() {
    
}

const JobPostMain = ({jobPost}: Props) => {
    const [isMoreInfoPanelActive, setMoreInfoPanelActive] = useState(false)

    return (
        <>
            <div className={classes.jobPost}>
                <div className={classes.container}>
                    <Link to={jobPost.url} className={classes.imageBlock}>
                        <img src={jobPost.image_link} />	
                    </Link>
                    <div className={classes.info}>
                        <span className={classes.nameBlock}>
                            <Link to={jobPost.url} className={classes.name}>
                                {jobPost.title}
                            </Link>
                            <span className={classes.salary}>{ jobPost.price } { jobPost.currency }</span>
                        </span> 
                        <div className={classes.additionalBlock}>
                            <span className={classes.age}>
                                Age: {jobPost.age ? <>{ jobPost.age } лет.</> : <>All</>}
                            </span>
                            <span className={classes.rubric}>{jobPost.rubric}</span>
                            <span className={classes.city}>{jobPost.city}</span>
                        </div>
                        <div className={classes.dateCreatedBlock}>
                            <span className={classes.dateCreated}>{returnJobPostDateString(jobPost.published_date)}</span>
                            
                            <img 
                                src={jobPost.is_added_to_favourites ?
                                        FullHeart 
                                        :
                                        EmptyHeart
                                    }
                                className={classes.addedToFav}
                            />
                        </div>
                    </div>
                </div>

                <div className={classes.moreInfo}>
                    <div className={classes.arrowDownDiv} onClick={() => setMoreInfoPanelActive(!isMoreInfoPanelActive)}>
                        <div className={classNames(classes.arrowDown, isMoreInfoPanelActive && classes.arrowUp)}></div>
                    </div>
                    {isMoreInfoPanelActive &&
                        <div className={classes.info}>
                            <div className={classes.authorInfo}>
                                <span className={classes.name}>
                                    {jobPost.owner.profile_link ?
                                        <Link to={jobPost.owner.profile_link}>{jobPost.owner.name}</Link>
                                        :
                                        <>
                                            <span style={{fontWeight: "bold"}}>{jobPost.owner.name}</span>
                                            <span className={classes.tempUserLabel}>24h</span>
                                        </>

                                    }
                                </span>
                                <span>Phone number: <a href={`tel:${jobPost.owner.phone_number}`}>{jobPost.owner.phone_number}</a></span> 
                                <span>Email: <a href= {`mailto:${jobPost.owner.email}`}>{jobPost.owner.email}</a></span>            
                            </div>
                            <div className={classes.jobContent}>{jobPost.content}</div>
                        </div>
                    }
                </div>
            </div>
        </>
    )
}

export default JobPostMain
