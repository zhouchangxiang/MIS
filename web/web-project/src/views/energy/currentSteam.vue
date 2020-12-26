<template>
  <el-row>
    <el-col :span="24">
      <el-row>
          <el-col :span="6">
                <div class="platformContainer asidetree" style="height:850px;">
                    <el-tree 
                      :data="treedata"
                      show-checkbox
                      node-key="id"
                      ref="tree"
                      default-expand-all
                      :props="defaultProps">
                    </el-tree>
                </div>
              </el-col>
              <el-col :span="18">
                 <div class="Timepick" style="height:66px;">
                   <el-form>
                   <el-form-item label="开始时间">
                      <el-date-picker
                        v-model="valuedatetime1"
                        type="datetime"
                        placeholder="选择日期时间"
                        default-time="valuedatetime1">
                      </el-date-picker>
                  </el-form-item>
                  <el-form-item label="结束时间">
                       <el-date-picker
                        v-model="valuedatetime2"
                        type="datetime"
                        placeholder="选择日期时间"
                        default-time="valuedatetime2">
                      </el-date-picker>
                  </el-form-item>
                   </el-form>
                   <el-radio-group v-model="radio1">
                      <el-radio-button label="汽"></el-radio-button>
                   </el-radio-group>
                   <el-tooltip  effect="dark" content="数据查询" placement="top-start">
                      <el-button type="primary" icon="el-icon-search" @click='searchData'>点击查询数据</el-button>
                  </el-tooltip>
                   <el-tooltip  effect="dark" content="数据导出" placement="top-start">
                      <el-button type="primary" icon="el-icon-position" @click='outExcel'>数据导出</el-button>
                  </el-tooltip>
              </div>
              <div class="platformContainer mainechart" style="position:relative;">
                   <div id="main" style="width:100%; height:750px;" v-loading="loading">数据图表</div>
              </div>
            </el-col>

      </el-row>
    </el-col>
  </el-row>
</template>

<script>
import echarts from '@/assets/js/echarts.js'
var moment = require('moment');
  export default {
    name: "currentSteam",
    data(){
      return {
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        treedata:[],
        valuedatetime1:moment().format('YYYY-MM-DD 00:00:00'),
        valuedatetime2:moment().format('YYYY-MM-DD 06:00:00'),
        radio1:'汽',
        loading:false,
        dateset:[],
        TagCode:'S_Area_GLF_45_3_502',
        dates:[],
        myChart:null,
        dataline1:[]
      }
    },
    created(){
      this.initTree()
    },
    mounted(){
      this.firstRenderDesk()
    },
    destroyed(){
    if(this.myChart){
      this.myChart.dispose()
      this.myChart.clear()
    }
    },
    methods:{
      outExcel(){

          var start_time=moment(this.valuedatetime1).format('YYYY-MM-DD HH:mm:ss')
          var end_time=moment(this.valuedatetime2).format('YYYY-MM-DD HH:mm:ss')
          var tag=this.TagCode

        window.location.href = "/api/exports?start_time="+start_time+"&end_time="+end_time+"&tag="+tag
      },
      initTree(){
          this.axios.get('/api/tags').then((res) => {
           this.treedata=res.data.data
          })
      },
      searchData(){
        var arr=this.$refs.tree.getCheckedNodes(true)
        if(arr.length===0){
          this.$message({
              message: '请先选择要实时展示的tag点',
              type: 'warning'
        });
          return;
        }else if(arr.length>1){
          this.$message({
              message: '只能选择一个tag点',
              type: 'warning'
          });
          return;
        }else{
          this.TagCode=arr[0].id
        var params={
          start_time:moment(this.valuedatetime1).format('YYYY-MM-DD HH:mm:ss'),
          end_time:moment(this.valuedatetime2).format('YYYY-MM-DD HH:mm:ss'),
          tag:this.TagCode
        }
        this.axios.post('/api/flow',this.qs.stringify(params)).then((res) => {
         this.dates = res.data.data.map(function (item) {
                return item.time.slice(11, 19)
              })
        this.dataline1 = res.data.data.map(function (item) {
                  return +item.value;
               });
        this.yvaluemax=Math.max.apply(Math, this.dataline1).toFixed(0)//初始y轴坐标值
        this.yvaluemin=Math.min.apply(Math, this.dataline1).toFixed(0)//初始y轴坐标值
        this.drawLine(this.dataline1,this.dateset,this.yvaluemax,this.yvaluemin);
        })
        }
      },
      firstRenderDesk(){
        var params={
          start_time:moment(this.valuedatetime1).format('YYYY-MM-DD HH:mm:ss'),
          end_time:moment(this.valuedatetime2).format('YYYY-MM-DD HH:mm:ss'),
          tag:this.TagCode
        }
        this.axios.post('/api/flow',this.qs.stringify(params)).then((res) => {
         this.dates = res.data.data.map(function (item) {
                return item.time.slice(11, 19)
              })
        this.dataline1 = res.data.data.map(function (item) {
                  return +item.value;
               });
        this.yvaluemax=Math.max.apply(Math, this.dataline1).toFixed(0)//初始y轴坐标值
        this.yvaluemin=Math.min.apply(Math, this.dataline1).toFixed(0)//初始y轴坐标值
        this.drawLine(this.dataline1,this.dateset,this.yvaluemax,this.yvaluemin);
        })
      },
    drawLine(dataline1,dateset,yvaluemax,yvaluemin){
        if(this.myChart){
          this.myChart.dispose()
          this.myChart.clear()
        }
        this.myChart= echarts.init(document.getElementById('main'));
        var option = {
              legend: {
                  data:dateset,
                  inactiveColor: '#777',
                  textStyle: {
                      color: '#fff'
                  }
              },
              tooltip: {
                  trigger: 'axis',
                  axisPointer: {
                      animation: false,
                      type: 'cross',
                      lineStyle: {
                          color: '#376df4',
                          width: 2,
                          opacity: 1
                      }
                  }
              },
              toolbox: {
                      feature: {
                          dataZoom: {
                              yAxisIndex: false
                          },
                          brush: {
                              type: ['lineX', 'clear']
                          }
                      }
                  },
              brush: {
                      xAxisIndex: 'all',
                      brushLink: 'all',
                      outOfBrush: {
                      colorAlpha: 0.1
                  }
              },
              xAxis: {
              type: 'category',
              data:this.dates,
              axisLine: { lineStyle: { color: '#8392A5' } }
              },
              yAxis: [{
                type: 'value',
                name: dateset,
                min: yvaluemin,
                max: yvaluemax,
                position: 'left',
                axisLabel: {
                    formatter: '{value}',
                },
                axisLine: {
                    lineStyle: {
                        color: '#8392A5',
                    },
                },
              }],
              grid: {
                bottom: 80,
                top:80
              },
              animation: false,
              visualMap: {
                show: false,
                dimension: 1,
                pieces: [],  //pieces的值由动态数据决定
                outOfRange: {
                color: 'green'
              }
          },
          series: [
              {
                  name: dateset[0],
                  yAxisIndex:0, 
                  type: 'line',
                  data: dataline1,
                  smooth: true,
                  showSymbol: false,
                  lineStyle: {
                      width: 1,
                      color:'#8CBD47'
                  }
              },
              {
	        name: '平行于y轴的对比线',
            type: 'line',
            markLine: {
                name: 'cc',
                symbol:'none',//去掉箭头
                lineStyle:{
                        type:"solid",
                        color:"#FF4B5C",
                    }
            }
              }
          ]
      };
        this.myChart.setOption(option);
      }

    }
  }
</script>

<style scoped>
.staticbox .platformContainer{
  margin-bottom: 0px;
  padding:15px 0px;
}
.staticbox .cardContainer{
  padding-left:0px;
}
.Timepick{
  width: 100%;
  margin-bottom: 15px;
  padding-left: 12px;
  padding-top: 12px;
  border-radius: 4px;
}
.asidetree{
  overflow: auto;
  padding-left: 0px;
  padding-right: 0px;
  border-radius: 4px;
}
.mainechart{
  border-radius: 4px;
}
</style>
