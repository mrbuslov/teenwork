import { useCallback, useEffect, useState } from "react"
import { getMainPagePosts } from "../../services/server_api"
import axios from "axios";
import { SERVER_ENDPOINT } from "../../consts/consts";
import JobPostMain, {JobPostProps} from "../../components/JobPostMain/JobPostMain";
import Paginator from "../../components/Paginator/Paginator";
import classes from "./Home.module.scss";
import Loader from "../../components/Loader/Loader";

const Home = () => {
  const [data, setData] = useState<JobPostProps[]>([]);
  const [page, setPage] = useState(1);
  const [isLoading, setLoading] = useState(false);
  const [isMorePostsLoading, setMorePostsLoading] = useState(false);

  const getPosts = async () => {
    setLoading(true);

    const res = await getMainPagePosts();
    console.log('get posts res', res)

    setData(res)
    setLoading(false)
  }
  useEffect(() => {
    getPosts();
  }, [])

  const handleLoadMorePostsBtnClick = async () => {
    console.log('handleLoadMorePostsBtnClick')
    setMorePostsLoading(true);
    const res = await getMainPagePosts(page + 1);
    setData([...data, ...res.result]);
    if (res.nextPage){
      setPage(page + 1);
    }
    else {
      setPage(0)
    }
    setMorePostsLoading(false);
  }

  if (isLoading) return <Loader />;
  else {
    return (
      <div className={classes.jobPostsContainer}>
        {data.map((item) => <JobPostMain key={item.id} jobPost={item} />)}
        {/* <Paginator 
          onNextPageClick={handleNextPageClick}
          onPrevPageClick={handlePrevPageClick}
          disable={{left: true, right: true}}
        /> */}

        {isMorePostsLoading ?
          <Loader />
          :
          page ?
            <div 
              className={classes.loadMoreBtn}
              onClick={() => handleLoadMorePostsBtnClick()}
            >Load more...</div>
            :
            ''
        }
      </div>
    )
  }
}

export default Home
