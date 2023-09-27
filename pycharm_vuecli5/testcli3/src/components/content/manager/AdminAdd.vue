<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="12">
        <my-card class="mycd" color="red">
          <template #header>
            <div class="card-header">
              <i class="el-icon-tickets"></i>
              <span>添加管理员</span>
            </div>
          </template>
          <el-form ref="form" :model="form" label-width="120px" :rules="rules">
            <el-form-item label="管理员账号" prop="username">
              <el-input v-model="form.username"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input v-model="form.password" show-password></el-input>
            </el-form-item>
            <el-form-item label="请再次输入密码" prop="password2">
              <el-input v-model="form.password2" show-password></el-input>
            </el-form-item>
            <div class="butt">
              <el-button type="primary" @click="useSubmit">提交</el-button>
              <!--        <el-button class="shou" @click="register">注册</el-button>-->
            </div>
          </el-form>
        </my-card>
      </el-col>
      <el-col :span="12">
        <my-card class="mycd" color="red">
          <template #header>
            <div class="card-header">
              <i class="el-icon-tickets"></i>
              <span>已有管理员</span>
            </div>
          </template>
          <el-table :data="da">
            <el-table-column
                label="账号"
                prop="name"
                width="100px">
            </el-table-column>
            <el-table-column
                label="密码"
                prop="password"
            width="100px">
            </el-table-column>
            <el-table-column
                align="right">
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
        </my-card>
      </el-col>
    </el-row>

  </div>
</template>

<script>
import {submit} from "@/components/api/data";
import {submit2} from "@/components/api/data";

export default {
  name: "AdminAdd",
  data() {
    const validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== this.form.password) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    };
    return {
      da: [],
      form: {
        username: '',
        password: '',
        password2: '',
      },
      rules: {
        username: [
          {required: true, message: "请输入用户名", trigger: "blur"},
          {max: 10, message: "不能大于10个字符", trigger: "blur"},
        ],
        password: [
          {required: true, message: "请输入密码", trigger: "blur"},
          {max: 10, message: "不能大于10个字符", trigger: "blur"},
          // { validator: validatePass2, trigger: 'blur', required: true }
        ],
        password2: [
          {required: true, message: "请输入密码", trigger: "blur"},
          {max: 10, message: "不能大于10个字符", trigger: "blur"},
          {validator: validatePass2, trigger: 'blur'}
        ],
      },
    }
  },
  methods: {
    useSubmit() {
      submit(this.form).then(res => {
        if (res.data.code === '20000') {
          this.$message({
            message: res.data.message,
            type: 'success'
          });
        } else {
          this.$message({
            message: res.data.message,
            type: 'failure'
          });
        }
      })
    }
  },
  mounted() {
    submit2().then((res) => {
      this.da = res.data.np
      console.log(this.da)
    })
  }
}
</script>

<style scoped>
.mycd {
  width: 500px;
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

.butt {
  margin-top: 10px;
  text-align: center;
}

</style>