<!--主页的内容写在这个地方-->
<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
// import MainTarBar from "@/components/content/maintarbar/MainTarBar";


export default {
  name: 'App',
  data() {
    return {
      back_data_ct: {},
    }
  },
  methods: {},
  mounted() {
    document.title="疫情溯源流调系统"
  }

}
</script>

<style  scoped>
@import "./assets/css/base.css";
@import "./assets/style/common.less";
html, body, #app {
  height: 100%;
  width: 100%;
  position: absolute;
  top: 0;
  left: 0;
  /* background:rgba(38, 24, 49,.6); */
}

</style>
