<template>
  <div>
    <my-card class="mycd">
      <template #header>
        <div class="card-header">
          <i class="el-icon-tickets"></i>
          <span>系统公告发布</span>
        </div>
      </template>

      <el-form ref="form" :model="form" label-width="120px">
        <el-form-item label="通告标题">
          <el-input v-model="form.name" ></el-input>
        </el-form-item>
        <el-form-item label="通告链接">
          <el-input v-model="form.url" ></el-input>
        </el-form-item>
        <el-form-item label="通告摘要">
          <el-input v-model="form.abstract" ></el-input>
        </el-form-item>
        <el-form-item label="时间选择">
          <el-col :span="11">
            <el-date-picker
                v-model="form.value3"
                type="datetime"
                placeholder="选择日期时间"
                default-time="12:00:00"
                style="width: 100%;">
            </el-date-picker>
          </el-col>
          <el-col class="line" :span="2">-</el-col>
          <el-col :span="11">
            <el-date-picker
                v-model="form.value4"
                type="datetime"
                placeholder="选择日期时间"
                default-time="12:00:00"
                style="width: 100%;">
            </el-date-picker>
          </el-col>
        </el-form-item>
        <el-form-item label="立即发布">
          <el-switch v-model="form.delivery"></el-switch>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">发布</el-button>
        </el-form-item>
      </el-form>
    </my-card>
  </div>
</template>

<script>
import {onBack} from "@/components/api/data";

export default {
  name: "Bulletin",
  data() {
    return {
      form: {
        name: '11月15日广州市新冠肺炎疫情情况',
        region: '',
        date1: '',
        url: 'https://www.gz.gov.cn/zt/qlyfdyyqfkyz/qktb/yqtb/content/post_8669398.html',
        abstract: '新增158例本土确诊病例和6138例本土无症状感染者情况',
        date2: '',
        delivery: false,
        type: [],
        resource: '',
        value3: '',
        value4: '',
        desc: ''
      }

    }
  },
  methods: {
    onSubmit() {
      this.$alert('确定提交吗？', '提示', {}).then((res) => {
        onBack(this.form).then((respond) => {
          this.$message({
            type: 'success',
            message: '成功提交'
          })
        })

      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消输入'
        });
      });
      console.log('submit!');
    },

  }
}
</script>

<style scoped>
.mycd {
  width: 1100px;
  margin-left: 50px;
  text-align: center;
}

.card-header {
  display: table-cell;
  text-align: center;
  vertical-align: middle;
}

/deep/ .my-card-header {
  text-align: center;
}

.card-header span {
  vertical-align: middle;
}

</style>