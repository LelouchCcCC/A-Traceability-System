<template>
  <div class="header">
    <div class="open">
      <span class="iconfont icon-a-communicate_textbox_icon_rightindent"></span>
      <span class="iconfont icon-a-communicate_textbox_icon_leftindent"></span>
    </div>
    <div class="right">
      <ul>
        <li>
          {{ nowDate }}
        </li>
        <li>|</li>
        <li>
          <el-dropdown>
  <span class="el-dropdown-link" type="primary">
    语言
    <i class="el-icon-arrow-down el-icon--right"></i>
  </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>中文</el-dropdown-item>
              <el-dropdown-item>English</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </li>
        <li>|</li>
        <li>欢迎使用该系统，{{ user }}</li>
        <li>|</li>
        <li class="dianyuan" @click="logOut"><span class="iconfont icon-dianyuan" ></span></li>
      </ul>
    </div>
  </div>
</template>

<script>

export default {
  name: "Header",
  created() {
    this.currentTime()
  },
  data() {
    return {
      nowDate: '',
      user: '',
      level: '',
    }
  },
  mounted:function (){
    this.user = sessionStorage.getItem('user')
    this.level = sessionStorage.getItem('level')
  },
  methods: {

    //获取当前时间

    getDate() {
      let date = new Date();
      let year = date.getFullYear(); // 年
      let month = date.getMonth() + 1; // 月
      let day = date.getDate(); // 日
      let week = date.getDay(); // 星期
      let weekArr = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
      let hour = date.getHours(); // 时
      hour = hour < 10 ? "0" + hour : hour; // 如果只有一位，则前面补零
      let minute = date.getMinutes(); // 分
      minute = minute < 10 ? "0" + minute : minute; // 如果只有一位，则前面补零
      let second = date.getSeconds(); // 秒
      second = second < 10 ? "0" + second : second; // 如果只有一位，则前面补零
      this.nowDate = `${year}年${month}月${day}日 ${hour}:${minute}:${second}`;
    },

    //定时器调取当前时间

    currentTime() {
      setInterval(() => {
        this.getDate()
      }, 1000)
    },
    logOut(){
      this.$store.commit('clearToken')
      this.$router.push('/login')
    },

  }
}

</script>

<style lang="less" scoped>
.header {
  display: flex;
  height: 50px;
  background-color: #1e78bf;
  color: white;
  line-height: 50px;

  .open {
    flex: 1;

    .iconfont {
      font-size: 20px;
      cursor: pointer;
    }
  }
}

.right {
  float: right;
  //background-color: pink;
  margin-right: 50px;
  width: 500px;
  height: 100%;
}

li {
  margin: 0 4px;
}

.el-dropdown-link {
  cursor: pointer;
  //color: #409EFF;
  color: white;
}

.el-icon-arrow-down {
  font-size: 12px;
}

.el-dropdown {
    vertical-align: top;
}

.dianyuan:hover{
  cursor: pointer;

}
</style>