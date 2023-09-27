<template>
  <el-row class="tac">
    <el-col>
      <el-menu
          :router="true"
          default-active="1"
          :default-openeds=this.defopen
          class="el-menu-vertical-demo"
          open="1"
          @open="handleOpen"
          @close="handleClose">
        <el-menu-item :index="'/index'" style="text-align: center"><i class="el-icon-menu"></i>处理中心</el-menu-item>
        <el-menu-item :index="'/main'" style="text-align: center"><i class="el-icon-location"></i>地图总览</el-menu-item>
        <!--        <el-menu-item :index="'/main'" style="text-align: center"><i class="el-icon-location"></i>-->
        <!--          <el-cascader-panel :options="options" ></el-cascader-panel>-->
        <!--        </el-menu-item>-->
        <el-submenu index="1" class="juti">
          <template slot="title">
            <i class="el-icon-location"></i>
            <span>具体城市</span>
          </template>
          <el-menu-item-group>
            <template slot="title">城市预览</template>
            <p></p>
            <div v-for="(item,index) in left">
              <!--              <el-row>-->
              <!--                <el-col :span="8" v-for="(item,index) in left">-->
              <div class="nei">
                <router-link :to="'/city/'+city_name[index]" @click.native="flash()">
                  <div :class="city_name[index]">
<!--                    <p>{{ item[0][0] }}</p>-->
                    <i>{{ item[0] }}</i>
                  </div>
                </router-link>
              </div>
              <!--                </el-col>-->
              <!--              </el-row>-->
            </div>
          </el-menu-item-group>
        </el-submenu>
        <el-menu-item :index="'/message'" style="text-align: center">
          <i class="el-icon-setting"></i>信息处理
        </el-menu-item>
        <el-menu-item :index="'/add-web'" style="text-align: center">
          <i class="el-icon-setting"></i>流调网址添加
        </el-menu-item>
      </el-menu>
    </el-col>
  </el-row>
</template>

<script>
import {getLeft} from "@/components/api/data";
import {pinyin} from "pinyin-pro";

export default {
  name: "Left",
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
      this.defopen.push('1')
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
      this.defopen.pop()
    },
    // flash() {
    //   this.$router.go(0)
    // },
  },
  data() {
    return {
      left: [],
      dd: [],
      city_name: [],
      defopen:['1'],
    }
  },
  mounted() {
    getLeft().then(res => {
      console.log("zheshileft:", res.data.target)
      this.left = res.data.target
      for (let i of this.left) {
        this.city_name.push(pinyin(i[0], {toneType: 'none'}).replace(/\s*/g, ""))
      }
      console.log(this.city_name)
    })
  }
}
</script>

<style lang="less" scoped>

.el-menu h3 {
  padding: 0px;
  text-align: center;
  color: cornflowerblue;
  font-size: 18px;
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  min-height: 400px;

}

.el-submenu {
  padding: 0px;
}

.juti {
  text-align: center;
}

.nei {
  float: left;
  width: 50%;
  height: 50px;
  text-align: center;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}

.nei i {
  font-size: 14px;
}

.tac {
  margin-top: 10px;
}
</style>