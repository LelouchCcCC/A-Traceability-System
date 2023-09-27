<template>
  <div>
    <div class="titl">
      <h2>流调信息网址解析</h2>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form ref="form" :model="form2" label-width="100px">
            <el-form-item label="爬虫网址：" class="elpu">
              <el-input v-model="form2.url" placeholder="请输入网址"></el-input>
            </el-form-item>
            <el-form-item label="XPath：" class="elpu">
              <el-input v-model="form2.XPath" placeholder="请输入XPath信息"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit" style="margin-left: -80px">提交</el-button>
            </el-form-item>
          </el-form>
        </el-col>
        <el-col :span="12">
          <el-form ref="form" :model="form" label-width="100px">
            <el-form-item label="解析网址：" class="elpu">
              <el-input v-model="form.url" placeholder="请输入网址"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit" style="margin-left: -80px">提交</el-button>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>


    </div>

    <div>
      <el-table
          :data="base.filter(data => !search || data.act.toLowerCase().includes(search.toLowerCase()))"
          class="midBack"
          stripe
          border>
        <el-table-column
            label="Date"
            prop="date"
            width="100px">
        </el-table-column>
        <el-table-column
            label="No"
            prop="no">
        </el-table-column>
        <el-table-column
            label="City"
            prop="city">
        </el-table-column>
        <el-table-column
            label="Place"
            prop="act">
        </el-table-column>
        <el-table-column
            align="right">
          <template slot="header" slot-scope="scope">
            <el-input
                v-model="search"
                size="mini"
                placeholder="输入关键字搜索"/>
          </template>
          <template slot-scope="scope">
            <el-button
                size="mini"
                @click="handleEdit(scope.$index, scope.row)">Edit
            </el-button>
            <el-button
                size="mini"
                type="danger"
                @click="handleDelete(scope.$index, scope.row)">Delete
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>


    <!--    <el-row :gutter="0">-->
    <!--      <el-col :span="24">-->
    <!--        <div v-if="sta===true" class="dazhanshi">-->
    <!--          <div class="rgt">-->
    <!--            <button @click="confirm">确认</button>-->
    <!--          </div>-->
    <!--          <div class="zhanshi">-->
    <!--            <label>编号</label>-->
    <!--            <label>地点</label>-->
    <!--            <label>确诊日期</label>-->
    <!--            <label>活动时间</label>-->
    <!--            <label>活动地点</label>-->
    <!--            <div v-for="(item,index1) in dd">-->
    <!--              <div>-->
    <!--                <input type="text" v-for="(it,index2) in item" :value=it @input="dd[index1][index2]=$event.target.value"-->
    <!--                       class="inp">-->
    <!--                <div class="adt" @click="dlt(index1)"></div>-->
    <!--                <br>-->
    <!--                <br>-->
    <!--                &lt;!&ndash;          <label class="xiaozhanshi" v-for="it in item">{{ it }}</label>&ndash;&gt;-->
    <!--              </div>-->
    <!--            </div>-->

    <!--            <div class="middle middlemi">-->
    <!--              <button @click="add">增加数据</button>-->
    <!--            </div>-->

    <!--          </div>-->


    <!--        </div>-->
    <!--      </el-col>-->
    <!--      <el-col :offset="2" :span="11">-->
    <!--        <el-card></el-card>-->
    <!--      </el-col>-->
    <!--    </el-row>-->
  </div>
</template>

<script>
import {postUrl} from "@/components/api/data";

export default {
  name: "AddWeb",
  data() {
    return {
      search: '',
      form: {
        url: ''
      },
      form2: {
        url: '',
        XPath:''
      },
      content: [],
      hd: [],
      dd: [],
      base: [],
      sta: false,

    }
  },
  methods: {
    onSubmit() {
      postUrl(this.form).then(res => {
        console.log(res.data)
        this.content = res.data.content
        this.hd = res.data.hd
        this.base = res.data.base
        this.sta = true
        this.$message({
          message: '提交成功',
          type: 'success'
        });
      })
    },
    handleEdit(index, row) {
      console.log(index, row);
      this.$prompt('请写出修改内容', '修改', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      }).then(({value}) => {
        this.$message({
          type: 'success',
          message: '修改已完成:' + value
        });
        row.act = value
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消输入'
        });
      });
    },
    handleDelete(index, row) {
      console.log(index, row);
      this.$confirm('此操作将删除该行, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message({
          type: 'success',
          message: '删除成功!',
        });
        this.deleteData(index, row)
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });
    },
    add() {
      this.dd.push(['', '', '', '', ''])
    },
    deleteData(index, row) {
      this.base.splice(index, 1)
    },
    dlt(index) {
      this.dd.splice(index, 1)
    },
    confirm() {
      let that = this
      // this.$refs.myConfirm.show('确认将数据提交？')
      this.axios({
        method: 'get',
        url: '/confirm',
        params: {
          dd: that.dd,
        }
      }).then(function (response) {
        console.log('获取数据response:' + response)
        console.log(response.data.status)
        that.sta = true
        that.dd.splice(0)
      }).catch(function (error) {
        console.log(error)
      })
    },
  }
}
</script>

<style scoped>
.titl {
  text-align: center;
  padding: 20px;
  margin-bottom: 50px;
}

.elpu {
  width: 80%;
  padding-left: 50px;
  margin-top: 50px;
}

.dazhanshi {

  width: 880px;
  padding: 15px;
  margin: 40px auto 0;
  font-size: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, .4);
}

.zhanshi {

  margin-right: 4px;
}

.zhanshi label {
  display: inline-block;
  font-size: 18px;
  width: 157.6px;
  height: 20px;
  margin-bottom: 10px;
}

.middle button {
  /* height: 35px;
   width: 45px; */
}

.middlemi button {
  width: 65px;
}

.middle {
  text-align: center;
  margin-top: 8px;
}

.sta {
  margin-top: 20px;
  margin-left: 30px;
}

.rgt {
}

.rgt button {
  float: right;
  margin-right: 10px;
  width: 45px;
  height: 29px;
}

.middle button {
  /* height: 35px;
   width: 45px; */
}

.middlemi button {
  width: 65px;
}

.inp {
  width: 150px;
  margin-right: 7.6px;
}

.dazhanshi {

  width: 880px;
  padding: 15px;
  margin: 40px auto 0;
  font-size: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, .4);
}

.zhanshi {

  margin-right: 4px;
}

.zhanshi label {
  display: inline-block;
  font-size: 18px;
  width: 157.6px;
  height: 20px;
  margin-bottom: 10px;
}

.adt {
  display: inline-block;
  height: 10px;
  width: 10px;
  background-image: url("../../../assets/img/dlt.png");
  background-size: 100% 100%;
}

.adt:hover {
  cursor: pointer;
}

.panel-header {
  border-bottom: solid 1px transparent;
  padding: 8px 15px;
  font-size: 14px;
  font-weight: 700;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  border-color: #50BFFF;
  background-color: #4662D9;
  color: #fff
}

.midBack {
  border-left: 50px;
  border-right: 100px;
  width: 1000px;
  margin: 100px;
}

/*面板标题*/
</style>