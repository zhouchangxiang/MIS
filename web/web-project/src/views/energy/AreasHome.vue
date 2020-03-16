<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <el-col :span="8">
        <div class="platformContainer">
          <div class="iconBlock float-left" style="color: #FB8A06;">
            <i class="fa fa-flash fa-2x"></i>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="platformContainer">
          <div class="iconBlock float-left" style="color: #FB8A06;">
            <i class="fa fa-flash fa-2x"></i>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="platformContainer">
          <div class="iconBlock float-left" style="color: #FB8A06;">
            <i class="fa fa-flash fa-2x"></i>
          </div>
        </div>
      </el-col>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name: "AreasHome"
  }
</script>

<style scoped>
  .iconBlock{
    width: 60px;
    height: 60px;
    line-height: 60px;
    background: #082F4C;
    text-align: center;
  }
  .iconBlock i{
    border-radius: 4px;
    vertical-align: middle;
  }
</style>
