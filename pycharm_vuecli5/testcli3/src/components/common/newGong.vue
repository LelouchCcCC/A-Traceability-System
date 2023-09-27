<template>
  <div class="layout">
    <div class="menu">
      <Menu></Menu>
    </div>
    <div class="content">
      <Content></Content>
    </div>
  </div>
</template>

<script>
import Menu from './Menu'
import Content from './Content'
export default {
  name: "newGong",
  components:{
    Menu,
    Content,

  }
}

</script>

<style lang="less" scoped>
.layout{
  .menu{
    //width:200px;
    background-color: #112f50;
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
  }
  .content{
    padding-left: 200px;
  }
}
</style>