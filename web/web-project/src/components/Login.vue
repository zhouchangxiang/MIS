<template>
  <el-container style="height: 100%;">
    <div class="login-img-bg">
      <div class="login-mask-bg"></div>
      <div class="login-form-box">
        <div class="login-form-title">辽宁好护士能耗管理系统</div>
        <div class="login-form-mask"></div>
        <div class="login-form">
          <el-form ref="ruleForm" :model="loginForm" :rules="rules" style="width: 100%;">
            <el-form-item prop="WorkNumber">
              <el-input placeholder="请输入工号" v-model="loginForm.WorkNumber">
                <i slot="prefix" class="el-input__icon el-icon-s-custom"></i>
              </el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input placeholder="请输入密码" v-model="loginForm.password" show-password>
                <i slot="prefix" class="el-input__icon el-icon-lock"></i>
              </el-input>
            </el-form-item>
            <el-form-item>
              <el-checkbox v-model="loginForm.rememb" class="remembCheckbox">记住密码</el-checkbox>
            </el-form-item>
          </el-form>
        </div>
        <div class="login-form-submit" @click="submitForm('ruleForm')">登录</div>
      </div>
    </div>
  </el-container>
</template>

<script>
  export default {
    name: "login",
    data(){
      return{
        color:"#082F4C",
        loginForm:{
          WorkNumber:"",
          password:"",
          rememb:false
        },
        rules:{
          WorkNumber:[
            {required: true, message: '请输入工号', trigger: 'blur'}
          ],
          password:[
            {required: true, message: '请输入密码', trigger: 'blur'}
          ]
        }
      }
    },
    methods:{
      submitForm(formName){
        let params = {
          WorkNumber:this.loginForm.WorkNumber,
          password:this.loginForm.password
        };
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.axios.post('/api/account/userloginauthentication',{
              WorkNumber:this.loginForm.WorkNumber,
              password:this.loginForm.password
            }).then(res =>{
              console.log(res)
              if(res.data == "OK"){
                this.$message({
                  message: "登录成功",
                  type: 'success'
                });
                var that = this;
                setTimeout(function(){
                  that.$router.push("/")
                },1000)
                sessionStorage.setItem('WorkNumber',this.loginForm.WorkNumber)
                this.$store.dispatch('setUser',this.loginForm.WorkNumber);
              }else{
                this.$message({
                  type: 'info',
                  message: res.data
                });
              }
            },res =>{
              console.log("请求错误")
            })
          }
        })
      },
      setCookie(){

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
    height: 360px;
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
    display: flex;
    align-items: center;
  }
  .login-form-title{
    position: relative;
    top: 20px;
    height: 40px;
    line-height: 40px;
    display: table;
    padding: 0 40px;
    background: #082F4C;
    color: #fff;
    border-radius:8px;
    margin: 0 auto;
    z-index: 1;
  }
  .login-form-submit{
    position: relative;
    bottom: 30px;
    width: 60px;
    height: 60px;
    line-height: 60px;
    text-align: center;
    display: table;
    background: #082F4C;
    color: #fff;
    border-radius:50%;
    margin: 0 auto;
    cursor: pointer;
    z-index: 1;
  }
</style>
