<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="8">
        <my-card class="mycd" color="red">
          <template #header>
            <div class="card-header">
              <i class="el-icon-tickets"></i>
              <span>admin1</span>
            </div>
          </template>
          <el-card class="box-card">
            <div v-for="o in da1" class="text item">
              {{ o }}
            </div>
          </el-card>
        </my-card>
      </el-col>
      <el-col :span="8">
        <my-card class="mycd" color="red">
          <template #header>
            <div class="card-header">
              <i class="el-icon-tickets"></i>
              <span>admin2</span>
            </div>
          </template>
          <el-card class="box-card">
            <div v-for="o in da2" class="text item">
              {{ o }}
            </div>
          </el-card>
        </my-card>
      </el-col>
      <el-col :span="8">
        <my-card class="mycd" color="red">
          <template #header>
            <div class="card-header">
              <i class="el-icon-tickets"></i>
              <span>admin3</span>
            </div>
          </template>
          <el-card class="box-card">
            <div v-for="o in da3" class="text item">
              {{ o }}
            </div>
          </el-card>
        </my-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "riZhi",
  data(){
    return{
      da1:['admin1_2023_02_18.txt','admin1_2023_03_14.txt','admin1_2023_03_15.txt','admin1_2023_03_16.txt','admin1_2023_03_17.txt'],
      da2:['admin2_2023_03_01.txt','admin2_2023_03_02.txt','admin2_2023_03_03.txt','admin2_2023_03_04.txt','admin2_2023_03_05.txt','admin2_2023_03_06.txt'],
      da3:['admin3_2023_04_10.txt','admin3_2023_04_11.txt','admin3_2023_04_12.txt','admin3_2023_04_13.txt'],
    }
  }
}
</script>

<style scoped>
 .text {
    font-size: 14px;
   text-decoration: underline;
  }
 .text:hover{
   cursor: pointer;
 }

  .item {
    padding: 18px 0;
  }
</style>