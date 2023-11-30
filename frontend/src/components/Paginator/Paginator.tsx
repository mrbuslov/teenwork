import classes from './Paginator.module.scss'

export interface PaginatorProps {
    onNextPageClick: () => void
    onPrevPageClick: () => void
    disable: {
        left: boolean
        right: boolean
    }
    nav?: {
        current: number
        previous: number
    }
}

const Paginator = ({
    onNextPageClick,
    onPrevPageClick,
    disable,
    nav,
}: PaginatorProps) => {
    const handleNextPageClick = () => {
        onNextPageClick();
    }
    const handlePrevPageClick = () => {
        onPrevPageClick();
    }

    return (
        <div className={classes.paginatorBlock}>
            <span className={'paginationArrowLeft'} onClick={() => handlePrevPageClick()}></span>
            <span className={'paginationArrowRight'} onClick={() => handleNextPageClick()}></span>
        </div>
    )
}

export default Paginator
