<template>
  <div>
    <h3 class="title">信息反馈</h3>
    <el-table
        :data="text"
        border
        style="width: 100%;"
    >
      <el-table-column
          fixed
          prop="date"
          label="日期"
          width="150">
      </el-table-column>

      <el-table-column
          prop="con"
          label="邮箱"
          width="200">
      </el-table-column>
      <el-table-column
          prop="email"
          label="内容"
          width="500">
      </el-table-column>
      <el-table-column
          fixed="right"
          label="操作"
          width="100">
        <template slot-scope="scope">
          <el-button @click="handleClick(scope.row)" type="text" size="small">回复</el-button>
          <el-button type="text" size="small">忽略</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
        :page-size="20"
        :pager-count="11"
        layout="prev, pager, next"
        :total="1000">
    </el-pagination>
  </div>

</template>

<script>
import {getFeed} from "@/components/api/data";
import {sendEmail} from "@/components/api/data";

export default {
  name: "Message",
  data() {
    return {
      text: [],
      length: 0,
      emaildata: {
        'receiver': '',
        'content': ''
      }


    }
  },
  methods: {
    handleClick(row) {
      console.log(row);
      this.emaildata.receiver = row.con;
      this.$prompt('请输入回复信息', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        // inputPattern: /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
        // inputErrorMessage: '邮箱格式不正确'
      }).then(({value}) => {

        this.emaildata.content = value;
        console.log(this.emaildata)
        sendEmail(this.emaildata).then(res => {
          if (res.data.status === 'success') {
            this.$message({
              type: 'success',
              message: '已成功回复信息:' + value
            });
          }

        })

      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消输入'
        });
      });
    }
  },
  mounted() {
    getFeed().then(res => {
      console.log(res.data)
      this.text = res.data.data
    })
  }
}
</script>

<style scoped>
.title {
  text-align: center;
  font-size: 30px;
  padding: 20px 0;
}
</style>