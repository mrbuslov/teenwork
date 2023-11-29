import axios from 'axios';
import { SERVER_ENDPOINT } from '../consts/consts';

export function getMainPageAds() {
    axios.get(`${SERVER_ENDPOINT}/api/main_page_ads/`)
    .then((res) => {
        return res.data;
    })
}
