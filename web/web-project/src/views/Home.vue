<template>
  <div class="home-container">
    <el-row :gutter="15">
      <el-col :span="17">
        <div class="home-card">
          <div class="home-card-head">
            <span><i class="el-icon-time el-icon--left" style="color: #FB3A06;"></i>能耗预览</span>
            <el-select class="card-head-select" v-model="energyValue" placeholder="请选择">
              <el-option v-for="item in energyOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </div>
          <div class="home-card-body" style="height: 462px;">
            <el-row :gutter="10">
              <el-col :span="8">
                <ul class="card-body-ul">
                  <li><span class="text-size-large text-color-info">本日耗电量</span><span class="text-size-mini text-color-info-shallow">（截止12：00）</span></li>
                  <li class="text-size-big text-color-warning">1256.25kwh</li>
                  <li><span class="text-size-mini text-color-info-shallow">对比</span>
                    <el-date-picker v-model="CompareDate" align="right" type="date" placeholder="选择日期" :picker-options="pickerOptions" size="mini" style="width: 130px"></el-date-picker>
                  </li>
                  <li><span class="text-size-small text-color-primary">1256.25kwh</span><span class="text-size-mini text-color-danger" style="float: right;">+9.5%<i class="el-icon-top"></i></span></li>
                </ul>
              </el-col>
              <el-col :span="8">
                <ul class="card-body-ul">
                  <li><span class="text-size-large text-color-info">本月耗电量</span></li>
                  <li class="text-size-big text-color-warning">1256.25kwh</li>
                  <li style="margin-top: 15px;">
                    <span class="text-size-mini text-color-info-shallow">上月同期</span>
                    <span class="text-size-mini text-color-info">4543.56 kwh</span>
                  </li>
                  <li>
                    <span class="text-size-mini text-color-info-shallow">上月同期</span>
                    <span class="text-size-mini text-color-success">+9.5%<i class="el-icon-bottom"></i></span>
                  </li>
                </ul>
              </el-col>
              <el-col :span="8">
                <ul class="card-body-ul">
                  <li>
                    <span class="text-size-large text-color-info">年累计耗电量</span>
                    <span class="text-size-mini text-color-warning">kwh</span>
                  </li>
                  <li class="text-size-big text-color-warning">1256.25kwh</li>
                  <li style="margin-top: 15px;">
                    <span class="text-size-mini text-color-info-shallow">上年同期</span>
                    <span class="text-size-mini text-color-info">4543.56 kwh</span>
                    <span style="float: right;" class="text-size-mini text-color-danger">+9.5%<i class="el-icon-top"></i></span>
                  </li>
                </ul>
              </el-col>
            </el-row>
          </div>
        </div>
        <el-row :gutter="15">
          <el-col :span="10">
            <div class="home-card-head">
              <span><i class="el-icon-guide el-icon--left" style="color: #228AD5;"></i>区域时段能耗</span>
              <el-select class="card-head-select" v-model="energyValue" placeholder="请选择">
                <el-option v-for="item in energyOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </div>
            <div class="home-card-body" style="height:280px;">

            </div>
          </el-col>
          <el-col :span="7">
            <div class="home-card-head">
              <span><i class="el-icon-odometer el-icon--left" style="color: #FB3A06;"></i>电能负荷率</span>
            </div>
            <div class="home-card-body" style="height:280px;">

            </div>
          </el-col>
          <el-col :span="7">
            <div class="home-card-head">
              <span><i class="el-icon-s-order el-icon--left" style="color: #15CC48;"></i>在线情况检测</span>
            </div>
            <div class="home-card-body" style="height:280px;">

            </div>
          </el-col>
        </el-row>
      </el-col>
      <el-col :span="7">
        <div class="home-card">
          <div class="home-card-head">
            <span><i class="el-icon-bell el-icon--left" style="color: #FB3A06;"></i>实时预警</span>
          </div>
          <div class="home-card-body" style="height: 300px;">

          </div>
        </div>
        <div class="home-card">
          <div class="home-card-head">
            <span><i class="el-icon-bell el-icon--left" style="color: #228AD5;"></i>单位批次能耗</span>
          </div>
          <div class="home-card-body" style="height: 300px;">

          </div>
        </div>
        <div class="home-card-body" style="height: 130px;">

        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  export default {
    name: "Home",
    data(){
        return{
          energyOptions: [{
            value: '选项1',
            label: '电能'
          }, {
            value: '选项2',
            label: '水能'
          }, {
            value: '选项3',
            label: '汽能'
          }],
          energyValue:'电能', //默认下拉
          pickerOptions: {
            disabledDate(time) {
              return time.getTime() > (Date.now() - 3600 * 1000 * 24);
            },
            shortcuts: [{
              text: '昨天',
              onClick(picker) {
                const date = new Date();
                date.setTime(date.getTime() - 3600 * 1000 * 24);
                picker.$emit('pick', date);
              }
            }, {
              text: '一周前',
              onClick(picker) {
                const date = new Date();
                date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
                picker.$emit('pick', date);
              }
            }]
          },
          CompareDate:Date.now() - 3600 * 1000 * 24, //默认对比日期
        }
    },
    mounted(){
      this.axios.get('http://127.0.0.1:5000/CUID',{
        params: {
            tableName: "AreaTable",
            limit : 100000000,
              offset : 0
        }
      }).then(function (response) {
          console.log(response);
      }).catch(function (error) {
          console.log(error);
      });
    }
  }
</script>
<style>
  .home-card{
    width: 100%;
    margin-bottom:10px;
  }
  .home-card-head{
    background: #082F4C;
    color: #fff;
    font-size: 18px;
    height: 48px;
    line-height: 48px;
    padding: 0 10px;
    border-radius:4px;
    margin-bottom: 10px;
  }
  .card-head-select{
    float: right;
    width: 85px;
  }
  .card-head-select .el-input__inner{
    background-color: #082F4C;
    border:none;
    color:#fff;
  }
  .card-head-select .el-select__caret{
    line-height: 48px;
  }
  .home-card-body{
    background: #fff;
    border-radius:4px;
    padding:10px;
  }
  .card-body-ul li{
    margin-bottom: 10px;
  }
  .text-size-big{
    font-size: 24px;
  }
  .text-size-large{
    font-size: 21px;
  }
  .text-size-small{
    font-size: 18px;
  }
  .text-size-mini{
    font-size: 16px;
  }
  .text-color-info{
    color: rgba(8,47,76,1);
  }
  .text-color-info-shallow{
    color: rgba(8,47,76,0.58);
  }
  .text-color-primary{
    color: #228AD5;
  }
  .text-color-warning{
    color: #FB8A06;
  }
  .text-color-success{
    color: #15CC48;
  }
  .text-color-danger{
    color: #FB3A06;
  }
</style>
