<template>
  <div>
    <el-menu
        :default-active="$route.path"
        class="el-menu-vertical-demo"
        background-color="#112f50"
        text-color="#fff"
        active-text-color="#ffd04b"
        router
        :collapse="isCollapse"
    >
      <el-menu-item>
        <span slot="title">疫情溯源分析系统</span>
      </el-menu-item>
      <el-menu-item :index="'/index'"><i class="el-icon-menu"></i>处理中心</el-menu-item>
      <el-menu-item :index="'/main'"><i class="el-icon-location"></i>地图总览</el-menu-item>
      <el-menu-item :index="'/city/huhehaoteshi'"><i class="el-icon-location"></i>具体城市</el-menu-item>
      <!--        <el-menu-item :index="'/main'" style="text-align: center"><i class="el-icon-location"></i>-->
      <!--          <el-cascader-panel :options="options" ></el-cascader-panel>-->
      <!--        </el-menu-item>-->
      <el-menu-item :index="'/message'">
        <i class="el-icon-document"></i>信息反馈处理
      </el-menu-item>
<!--      <el-menu-item :index="'/sql'">-->
<!--        <i class="el-icon-search"></i>数据库查询-->
<!--      </el-menu-item>-->
      <el-menu-item :index="'/add-web'">
        <i class="el-icon-setting"></i>流调网址添加
      </el-menu-item>
      <el-menu-item :index="'/bulletin'">
        <i class="el-icon-info"></i>公告发布
      </el-menu-item>
      <el-menu-item :index="'/admin'" v-show="show">
        <i class="el-icon-setting"></i>管理员管理
      </el-menu-item>
      <el-menu-item :index="'/rizhi'" v-show="show">
        <i class="el-icon-news"></i>管理员操作日志
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: "newLeft",
  data() {
    return {
      isCollapse: false,
      level: '',
      show: false,
    }
  },
  mounted() {
    this.level = sessionStorage.getItem('level')
    if (this.level === 'atAdmin'){
      this.show = true
    }
  }
}
</script>

<style lang="less" scoped>
.el-menu {
  border-right: 0;

  /deep/ .is-active {
    background: #1e78bf !important;
    color: #fff !important;
  }
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}

/deep/ .el-menu-item {
  width: 200px !important;
}
</style>