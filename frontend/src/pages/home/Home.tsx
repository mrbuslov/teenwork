import { useEffect, useState } from "react"
import { getMainPageAds } from "../../services/server_api"
import axios from "axios";
import { SERVER_ENDPOINT } from "../../consts/consts";
import JobPostMain, {JobPostProps} from "../../components/JobPostMain/JobPostMain";

const Home = () => {
  const [data, setData] = useState<JobPostProps[]>([]);

  useEffect(() => {
    console.log('useEffect')
    // let res = getMainPageAds();
    
    const headers = {
      'Content-Type': 'application/json',      
    }
    const options = {headers: headers}
    axios.get(`${SERVER_ENDPOINT}/api/main_page_ads/`, options)
    .then((res) => {
      // return res.data;
      console.log('res', res)
      setData(res.data.result)
    })
  }, [])

  return (
    <>
      {data.map((item) => <JobPostMain key={item.id} jobPost={item} />)}
    </>
  )
}

export default Home
