<template>
  <el-container style="height: 100%;">
    <div class="login-img-bg">
      <div class="login-mask-bg"></div>
      <div class="login-form-box">
        <div class="login-form-mask"></div>
        <div class="login-form">
          <el-form ref="form" :model="loginForm">
            <el-form-item>
              <el-input placeholder="请输入工号" v-model="userName">
                <i slot="prefix" class="el-input__icon el-icon-s-custom"></i>
              </el-input>
            </el-form-item>
            <el-form-item>
              <el-input placeholder="请输入密码" v-model="userName">
                <i slot="prefix" class="el-input__icon el-icon-lock"></i>
              </el-input>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
  </el-container>
</template>

<script>
  export default {
    name: "login",
    data(){
      return{
        loginForm:{
          userName:""
        },
      }
    }
  }
</script>

<style scoped>
  .login-img-bg{
    position: relative;
    width: 100%;
    height: 100%;
    background: url("../assets/imgs/loginBg.jpg") no-repeat;
    background-size:cover;
    -webkit-background-size: cover;
    -o-background-size: cover;
    background-position: center 0;
    display: flex;
    align-items:center;
  }
  .login-mask-bg{
    position: absolute;
    width: 100%;
    height: 100%;
    background: #082F4C;
    opacity: 0.52;
  }
  .login-form-box{
    position: relative;
    width: 400px;
    height: 400px;
    margin: 0 auto;
  }
  .login-form-mask{
    position: absolute;
    width: 100%;
    height: 100%;
    background: #fff;
    border-radius:8px;
    opacity: 0.33;
  }
  .login-form{
    width: 100%;
    height: 100%;
    padding: 40px;
  }
</style>
