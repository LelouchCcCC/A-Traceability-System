<template>
  <el-container>
    <el-header>
      <Nav/>
    </el-header>
    <el-row :gutter="0">
      <el-col :span="4">
        <el-aside width="200px">
          <Left/>
        </el-aside>
      </el-col>
      <el-col :span="19">
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-col>
    </el-row>
  </el-container>
</template>

<script>
import Nav from "@/components/common/Nav";
import Left from "@/components/common/Left";
export default {
  name: "GongTong",
    components: {
    Nav,
    Left,
  },
}
</script>

<style scoped>

.el-aside {
  height: 100vh;
}

.el-header {
  padding: 0;
}
.el-card /deep/ .el-card__header {
  padding: 0;
}

.el-card__body, .el-main {
    padding: 0px;
}
</style>