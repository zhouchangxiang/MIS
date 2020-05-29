<template>
   <div class="mainbox">
       <div class="top">
           <div class='head-name'>辽宁好护士能源管理系统</div>
           <span @click="logout"></span>
       </div>
       <router-view/>
       <div class="foot">
           <van-tabbar v-model="active" :fixed="false" inactive-color="#fff">
                <van-tabbar-item icon="wap-home" to="/home">首页</van-tabbar-item>
                <van-tabbar-item icon="location" to="/region" >区域</van-tabbar-item>
                <van-tabbar-item icon="graphic" to="/efficiency">能效</van-tabbar-item>
                <van-tabbar-item icon="ascending" to="/report">报告</van-tabbar-item>
           </van-tabbar>
       </div>
   </div>
</template>
<script>
export default {
    data(){
        return {
            msg:'123',
            active:0
        }
    },
    methods:{
        logout(){
            localStorage.removeItem('token')
            this.$router.push('/login')
        }
    }
}
</script>
<style lang="less" scoped>
    @bgca:#3D4048FF;
    @bgcc:#1E222BFF;
    .mainbox{
        position: relative;
        width:375px;
        height:667px;
        background:#eee;
        opacity:1;
    }
    .top{
        position: relative;
        height:89px;
        width:375px;
        background-color:#999;
        .head-name{
            position: absolute;
            top:46px;
            left:90px;
            height:25px;
            font-size:16px;
            font-family:PingFang SC;
            font-weight:500;
            line-height:25px;
            color:rgba(255,255,255,1);
            opacity:1;
        }
        span{
           position: absolute;
           width: 20px;
           height: 20px;
           top:48px;
           left:318px;
           border: 1px solid #ccc;
           background-image: url('../../assets/png/delete_fill.png');
           background-color:skyblue;
           background-size: contain;
        }
    }
    .foot{
        position: fixed;
        bottom: 0;
        width:375px;
        height:64px;
        background:#666;
        box-shadow:0px -2px 4px rgba(255,255,255,0.16);
        opacity:1;
    }
    .van-tabbar{
        height: 64px;
        background-color: #999;
        &.van-tabbar--fixed{
            height: 64px;
        }
    }
</style>
