<template>
    <div>
        <div class="show-foot">
               <div class="sf-l">
                   <div class="hf">耗费成本</div>
                   <div class="all-money">{{this.$store.state.sbnumber.cost}}<span>元</span></div>
               </div>
                <div class="sf-r">
                   <div class="machine">设备在线情况</div>
                   <div class="tj"><span>12</span>&nbsp;/&nbsp;<span>23</span></div>
               </div>
        </div>

    </div>
</template>
<script>
import store from '../../store/index'
export default {
    data(){
        return {
            
            
        }
    }
}
</script>
<style lang="less" scoped>
 @bgca:#3D4048FF;
 @bgcc:#1E222BFF;
 @bgct:#7E7F84;
.show-foot{
            position: relative;
            height:64px;
            background:@bgca;
            opacity:1;
            border-radius:4px;
            background-color:@bgcc;
            .sf-l{
                position: absolute;
                left:0;
                top:0;
                width: 196px;
                height: 64px;
                border-radius: 4px;
                background-color: @bgct;
                .hf{
                    position: absolute;
                    top:8px;
                    left: 13px;
                    height:11px;
                    font-size:8px;
                    font-weight:400;
                    line-height:11px;
                    color:rgba(255,255,255,1);
                    opacity:1;
                }
                .all-money{
                    position: absolute;
                    left:16px;
                    top:28px;
                    height:23px;
                    font-size: 23px;
                    color:rgba(255,255,255,1);
                    span{
                        font-size: 12px;
                        margin-left: 5px;
                        }
                }

            }
            .sf-r{
                position: absolute;
                right: 0;
                top:0;
                width:141px;
                height: 64px;
                border-radius: 4px;
                background-color:@bgct;
                .machine{
                    position: absolute;
                    top:8px;
                    left: 12px;
                    height:11px;
                    font-size:8px;
                    font-weight:400;
                    line-height:11px;
                    color:rgba(255,255,255,1);
                }
                .tj{
                    position: absolute;
                    left: 13px;
                    top: 28px;
                    font-size: 23px;
                    font-weight: 500;
                    color: #fff;
                    letter-spacing: 5px;
                }
            }
        }
</style>