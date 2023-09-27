import axios from "./axios";

export const getMenu = (param) => {
    return axios.request({
        url: '/login',
        method: 'post',
        data: param,
    })
}

export const getFeed = () => {
    return axios.request({
        url: '/managerfeed',
        method: 'get',
    })
}

export const sendEmail = (param) => {
    return axios.request({
        url: '/sendemail',
        method: 'post',
        data: param,
    })
}

export const getLeft = () => {
    return axios.request({
        url: '/getleft',
        method: 'get',
    })
}

export const postUrl = (param) => {
    return axios.request({
        url: '/manager_url',
        method: 'post',
        data: param,
    })
}

export const getIndex = () => {
    return axios.request({
        url: '/tst',
        method: 'get',
    })
}

export const onBack = (param) => {
    return axios.request({
        url: '/bullt',
        method: 'post',
        data: param,
    })
}

export const submit = (param) => {
    return axios.request({
        url: '/add-manager',
        method: 'post',
        data: param,
    })
}

export const submit2 = () => {
    return axios.request({
        url: '/watch-manager',
        method: 'get',
    })
}