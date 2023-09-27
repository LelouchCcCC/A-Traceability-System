<template>
  <div>
<!--    顶部-->
    <Header></Header>
<!--    内容-->
    <router-view></router-view>
  </div>
</template>

<script>
import Header from './Header'
export default {
  name: "Content",
  components:{
    Header
  }
}
</script>

<style scoped>

</style>