<template>
  <div class="login">
  <div class="login-header">
    <h5>好护士能管系统</h5>
    <p>欢迎使用</p>
  </div>
  <div class="login-body">
    <p>密码登陆</p>
    <div class="login-box">
     <van-form @submit="onSubmit">
        <van-field
          label-width='261px'
          v-model="username"
          label='用户名'
          placeholder="输入登录账号"
          :rules="[{ required: true, message: '请填写用户名' }]"
        />
        <van-field
          label-width='261px'
          v-model="password"
          label="密码"
          type="password"
          placeholder="输入登录密码"
          :rules="[{ required: true, message: '请填写密码' }]"
        />
        <div style="margin: 16px;">
          <van-button round block type="info" native-type="submit">
            提交
          </van-button>
          </div>
    </van-form>

    </div>
  </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
        username:'',
        password:''
    }
  },
  methods:{
    onSubmit(values) {
      console.log('submit', values);
    },
  }
}
</script>
<style scoped>
p{
    margin:0;
    padding:0;
}
  .login{
  width:375px;
  height:667px;
  background:rgba(30,34,43,1);
  opacity:1;
  }
  .login-header{
    width:100%;
    height:141px;

  }
  .login-header p{
    position:absolute;
    top:90px;
    left:156px;
    width:64px;
    height:22px;
    line-height:22px;
    font-size:16px;
    font-family:PingFang SC;
    font-weight:400;
    color:rgba(255,255,255,1);

  }
  h5{
    position:absolute;
    left:125px;
    top:46px;
    font-size:18px;
    font-family:PingFang SC;
    font-weight:500;
    line-height:25px;
    color:rgba(255,255,255,1);
    opacity:1;
  }
  .login-body{
    position:relative;
    width:375px;
    height:526px;
    background:rgba(126,127,132,1);
    box-shadow:0px -2px 4px rgba(206,199,199,0.16);
    opacity:1;
    border-radius: 30px 30px 0 0;
  }
  .login-body p{
    position:absolute;
    left:152px;
    width:72px;
    height:25px;
    top: 30px;
    font-size:18px;
    font-family:PingFang SC;
    font-weight:500;
    line-height:25px;
    color:rgba(255,255,255,1);
    opacity:1;
  }
  .login-box{
    position:absolute;
    top:90px;
    left:50%;
    transform: translateX(-50%);
  }
  .van-button--info{
    background-color:rgba(0,250,231,1);
    opacity:1;
    border-radius:8px;
    border-color: #CEC7C7;
  }
</style>
