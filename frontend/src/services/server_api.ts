import axios from 'axios';
import { SERVER_ENDPOINT } from '../consts/consts';

export async function getMainPagePosts(page: number = 1) {
    const params = {
        page: page.toString(),
    };
    const paramsString = new URLSearchParams(params).toString();
    console.log('paramsString', paramsString)

    const headers = {
        'Content-Type': 'application/json',
    }
    const options = { headers: headers }
    console.log(`${SERVER_ENDPOINT}/api/v1/posts/`) // ?${paramsString}
    // const response = await axios.get(`${SERVER_ENDPOINT}/api/main_page_ads/`, options) // ?${paramsString}
    const response = await axios.get(`${SERVER_ENDPOINT}/api/v1/posts/`, options) // ?${paramsString}
    console.log('response', response)
    
    return response.data.results
}
