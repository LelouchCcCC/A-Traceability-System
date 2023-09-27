const axios = require('axios')
const baseUrl = 'http://localhost:5000'
function getRegions(){
  axios({
    method:'get',
    url:baseUrl+'/userhome'
  }).then((res)=>{
    console.log('data:',res)
    return res.data
  })

}
module.exports = {
  getRegions
}
