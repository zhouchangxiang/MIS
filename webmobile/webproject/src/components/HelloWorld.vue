<template>
  <div class="login">
  <div class="login-header">
    <h5>好护士能管系统</h5>
    <p>欢迎使用</p>
  </div>
  <div class="login-body">
    <p>密码登陆</p>
    <div class="login-box">
      <van-cell-group>
                    <van-field
                        v-model="username"
                        required
                        clearable
                        type="tel"
                        label="手机号"
                        label-width="53px"
                        left-icon="contact"
                        right-icon="question-o"
                        placeholder="输入登录账号"
                        @click-right-icon="$toast('请填写11位手机号码')"
                       
                    />
                    <van-field
                        v-model="password"
                        label="密码"
                        label-width="53px"
                        left-icon="closed-eye"
                        right-icon="question-o"
                        placeholder="输入登录密码"
                        required
                        clearable
                        @click-right-icon="$toast('请牢记你的输入密码,不要泄露')"
                   
                    />
                    </van-cell-group>
                <div class='submit'><van-button color="#00FAE7FF" size="large" @click="login">登录</van-button></div>
    </div>
  </div>
  </div>
</template>

<script>
import qs from 'qs'
export default {
  data () {
    return {
        username: "",
        password: ""
    }
  },
  methods:{
  
    login: function (e,username,password) {
        if(this.username == ''){
          this.$toast("用户名不能为空");
          return false;
        }
        if(this.password == ''){
          this.$toast("密码不能为空");
          return false;
        }else{
          let comment={worknumber:this.username,password:this.password}
          let str=qs.stringify(comment)
          console.log(str)
          this.$http.post('/api/v2/accounts/login',str).then((value) => {
            console.log(value)
          })
        }
  }
}
}
</script>
<style scoped>
  p,h5{
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
    top:101px;
    left:50%;
    width:261px;
    transform: translateX(-50%);
  }
  .van-cell{
    background-color: #7E7F84;
  }
  .submit{
    background-color: #7E7F84;
    padding-top: 33px;
  }
  .van-button{
    border-radius: 10px;
  }
  .van-button__text{
    width:32px;
    height:22px;
    font-size:16px;
    font-family:PingFang SC;
    font-weight:400;
    line-height:22px;
    color:rgba(30,34,43,1);
    opacity:1;
  }
</style>
