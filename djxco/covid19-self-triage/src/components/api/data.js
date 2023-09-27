import axios from "./axios";

export const getStatistic = () => {
    return axios.request({
        url: '/statistics.json',
        method: 'get',
    })
}

export const getNotice = () => {
    return axios.request({
        url: '/notice.json',
        method: 'get',
    })
}

export const getContacts = (param) => {
    return axios.request({
        url: '/contacts_check_safe.json',
        method: 'post',
        data: param
    })
}

export const getRegionsSearch = (param) => {
    return axios.request({
        url: '/regions_search.json',
        method: 'post',
        data: param
    })
}

export const getInputTips = (param) => {
    return axios.request({
        url: '/inputtips',
        baseURL: 'https://restapi.amap.com/v3/assistant/',
        method: 'get',
        params: {
            keywords: param,
            datatype: 'poi',
            key: '148441487f6e8da5138f6372157edd77'
          },
    })
}


export const getFeedback = (param) => {
    return axios.request({
        url: '/feedback_success',
        method: 'post',
        data: param
    })
}

