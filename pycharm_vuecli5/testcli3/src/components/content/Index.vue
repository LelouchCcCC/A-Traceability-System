<template>
  <div style="text-align: center">
    <div class="pp">
      <!--              （数据为3月5日前搜集的数据）-->
      <h2 style="margin-top: 20px">全国近7天内有疫情的城市</h2>
    </div>
    <div class="split"></div>
    <div class="myc">
      <el-card class="comm">信息较少，暂为本地的疫情</el-card>
      <div style="height: 20px"></div>
      <div>
<!--        <my-card color="blue" class="myy" v-for="i in thr.non">-->
<!--          {{ i.date }}-->
<!--        </my-card>-->
        <el-table
          :data="thr.non"
          border
          stripe
          :row-class-name="tableRowClassName"
          style="text-align: center"
          class="datatable">
        <el-table-column
            prop="date"
            label="日期"
            width="180">
        </el-table-column>
        <el-table-column
            prop="city"
            label="城市名"
            width="180">
        </el-table-column>
        <el-table-column
            prop="message"
            label="可能有关的城市">
        </el-table-column>
          <el-table-column
            prop="num"
            label="近期的感染人数">
        </el-table-column>
      </el-table>
      </div>
      <div style="height: 20px"></div>
    </div>
    <div class="split"></div>
    <div class="my2">
      <el-card class="commm">与周围城市有关联的城市</el-card>
      <div style="height: 20px"></div>
      <div>
        <el-table
          :data="thr.on"
          border
          stripe
          :row-class-name="tableRowClassName"
          style="text-align: center"
          class="datatable">
        <el-table-column
            prop="date"
            label="日期"
            width="180">
        </el-table-column>
        <el-table-column
            prop="city"
            label="城市名"
            width="180">
        </el-table-column>
        <el-table-column
            prop="message"
            label="可能有关的城市">
        </el-table-column>
          <el-table-column
            prop="num"
            label="近期的感染人数">
        </el-table-column>
      </el-table>
      </div>
      <div style="height: 20px"></div>
    </div>
    <div class="split"></div>
    <div class="my3">
      <el-card class="commmm">与周围城市关联密切的城市</el-card>
      <div style="height: 20px"></div>
              <el-table
          :data="thr.ons"
          border
          stripe
          :row-class-name="tableRowClassName"
          style="text-align: center"
          class="datatable">
        <el-table-column
            prop="date"
            label="日期"
            width="180">
        </el-table-column>
        <el-table-column
            prop="city"
            label="城市名"
            width="180">
        </el-table-column>
        <el-table-column
            prop="message"
            label="可能有关的城市">
        </el-table-column>
          <el-table-column
            prop="num"
            label="近期的感染人数">
        </el-table-column>
      </el-table>
    </div>
    <div style="height: 50px"></div>

<!--    <div style="text-align: center">-->
<!--      <el-table-->
<!--          :data="pp"-->
<!--          border-->
<!--          :row-class-name="tableRowClassName"-->
<!--          style="text-align: center"-->
<!--          class="datatable">-->
<!--        <el-table-column-->
<!--            prop="date"-->
<!--            label="日期"-->
<!--            width="180">-->
<!--        </el-table-column>-->
<!--        <el-table-column-->
<!--            prop="city"-->
<!--            label="城市名"-->
<!--            width="180">-->
<!--        </el-table-column>-->
<!--        <el-table-column-->
<!--            prop="message"-->
<!--            label="可能有关的城市">-->
<!--        </el-table-column>-->
<!--      </el-table>-->
<!--    </div>-->

    <!--    <el-row :gutter="12" class="onmus">-->
    <!--      <el-col :span="6" class="myCard" v-for="(item,index) in dd">-->
    <!--        <el-card shadow="hover" class="subCard">-->
    <!--          <router-link :to="'/city/'+city_name[index]">-->
    <!--            <div :class="city_name[index]">-->
    <!--              <p>{{ item[0][0] }}</p>-->
    <!--              &lt;!&ndash; <el-divider></el-divider> &ndash;&gt;-->
    <!--              <p>{{ item[0][1] }}</p>-->
    <!--              <p>{{ item[1] }}</p>-->
    <!--            </div>-->
    <!--          </router-link>-->
    <!--          <router-view></router-view>-->
    <!--        </el-card>-->
    <!--      </el-col>-->
    <!--    </el-row>-->
  </div>
</template>

<script>

import {getIndex} from "@/components/api/data";
import {pinyin} from "pinyin-pro";
export default {
  name: "Index",
  methods: {
    tableRowClassName({row, rowIndex}) {
      if(row['message'].includes('本土')){
        return 'success-row'
      }
      if(row['message'].includes(',')){
        return 'warning-row';
      }
      else {
        return 'yiban-row';
      }
      return '';
    }
  },
  data() {
    return {
      dd: [],
      city_name: [],
      pp: [],
      thr: [],
    }
  },
  mounted: function () {
    //这里放获取json数据
    getIndex().then(res => {
      this.dd = res.data.key
      this.pp = res.data.key2
      this.thr = res.data.key3
      for (let i of this.dd) {
        this.city_name.push(pinyin(i[0][0], {toneType: 'none'}).replace(/\s*/g, ""))
      }

    }).catch(function (error) {
      console.log(error)
    })
    // let that = this
    // this.axios({
    //   method: 'get',
    //   ContentType: 'application/json;charset-utf-8',
    //   url: '/tst',
    //   data: {}
    // }).then(function (response) {
    //   console.log('获取数据response:' + response)
    //   const dd = response.data.key
    //   that.dd = dd
    //   console.log('这是数据：', dd)
    //   for (let i of that.dd) {
    //     that.city_name.push(pinyin(i[0][0], {toneType: 'none'}).replace(/\s*/g, ""))
    //   }
    //   // console.log(that.city_name)
    //   // console.log('books:' + JSON.stringify(that.bodys, null, 4))
    // }).catch(function (error) {
    //   console.log(error)
    // })
  }


}
</script>

<style scoped>


table, th, td {
  border: 1px solid black;
  cellpadding: 1px;
  cellspacing: 1px;
  text-align: center;
}

table {
  width: 100%;
}

p {
  text-align: center;
  line-height: 200%;
}

#body {
  width: 950px;
  margin: auto;
}

.pp {
  text-align: center;
  margin-top: 10px;
  margin-bottom: 20px;
}

.disp {
  margin: 10px 25px;
}

.disp ul {
  /*float: left;*/
  overflow: hidden;
  display: inline-block;
}

.disp ul li {
  height: fit-content;
  width: 300px;
  margin-right: 30px;
  margin-bottom: 30px;
  background-color: #666666;
  /*float: left;*/
  float: left;
  transition: all 0.9ms;
  color: black;
  border-radius: 10px;
}

/*.onmus:hover {*/
/*  box-shadow: 0px 15px 30px rgba(0, 0, 0, 0.4);*/
/*  cursor: pointer;*/
/*  !*margin-top: 90px;*!*/
/*}*/

.router-link-active {
  text-decoration: none;
  color: #fff;
}

a {
  text-decoration: none;
  color: black;
}

.myCard {
  margin-top: 20px;
}

.subCard {
  background-color: #F8F9FA;
}

.el-aside {
  height: 100vh;
}

.el-header {
  padding: 0;
}

.el-card /deep/ .el-card__header {
  padding: 0;
}

.el-card__body, /deep/ .el-main {
  padding: 0;
}

.datatable {
  width: 80%;
  margin-left: 10%;
}

.el-table /deep/.warning-row {
  background: #ff8198;
}

.el-table /deep/.success-row {
  background: #f0f9eb;
}

.el-table /deep/.yiban-row {
  background: oldlace;
}

.myc {
  overflow: hidden;
}

.my2 {
  overflow: hidden;
}

.my3 {
  overflow: hidden;
}

.myy {
  margin: 0px;
  width: 200px;
  text-align: left;
}

.split {
  height: 2px;
  border-top: 1px gray solid;
  margin-left: 20px;
  margin-right: 20px;
}

.comm {
  width: 250px;
  height: 50px;
  background-color: gray;
  size: 14px;
  margin-left: 20px;
  margin-top: 5px;
}

.commm {
  width: 250px;
  height: 50px;
  background-color: orange;
  size: 14px;
  margin-left: 20px;
  margin-top: 5px;
}

.commmm {
  width: 250px;
  height: 50px;
  background-color: #ff8198;
  size: 14px;
  margin-left: 20px;
  margin-top: 5px;
}
</style>