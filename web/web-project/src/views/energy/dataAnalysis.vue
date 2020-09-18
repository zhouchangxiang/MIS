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
    name: "dataAnalysis",
    data(){
      return {
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        treedata:[{
          id: 1,
          label:this.$route.query.areaName,
          children: []
        }],
        valuedatetime1:moment().format('YYYY-MM-DD 00:00:00'),
        valuedatetime2:moment().format('YYYY-MM-DD 06:00:00'),
        radio1:'汽',
        loading:false,
        dateset:[],
        TagCode:'S_Area_GLF_45_3_502',
        websoc:null,
        selftime:2,
        isout:false,
        value2:'',
        dates:[],
        myChart:null,
        dataline1:[],
        maxvalue:10,
        date1:moment().format('YYYY-MM-DD'),
        date2:moment().format('YYYY-MM-DD'),
        time1:'00:00:00',
        time2:moment().format('HH:mm:ss'),
        averagevalue1:0,
        dataIndex:0,
        comparetime:'00:00:04',
      }
    },
    created(){
      this.initTree()
    },
    methods:{
      initTree(){
        var params={
          AreaName:this.$route.query.areaName,
          EnergyClass:'汽'
        }
          this.axios.get('/api/selectTagByAreamName',{params:params}).then((res) => {
            var arr=res.data
            if(this.$route.query.areaName!=='整厂区'){
              this.treedata[0].children=arr.map((value, index) => {
                return {id:value.TagClassValue,label:value.FEFportIP,ParentTagCode:value.DeviceNum}
            })
            }else{
              this.treedata=arr.map((value, index) => {
                return {id:value.ID,label:value.AreaName,children:[{
                 id:value.TagClassValue,label:value.FEFportIP,ParentTagCode:value.DeviceNum
                }]}
            })
            }
          })
      },
      searchData(){
        var arr=this.$refs.tree.getCheckedNodes()
        if(arr.length===0){
          this.$message({
              message: '请先选择要实时展示的tag点',
              type: 'warning'
        });
          return;
        }
        var j=0
        for(var i=0;i<arr.length;i++){
           if(arr[i].hasOwnProperty('ParentTagCode')){  //判断子节点
              j++
              if(j>1){
                this.$message({
                  message: '请选择单个tag点',
                  type: 'error'
              });
              return;
              }else{
                this.TagCode=arr[i].id
                this.dateset=[]
                this.dateset.push(arr[i].label)
              }
          }}
        var params={
          StartTime:moment(this.valuedatetime1).format('YYYY-MM-DD HH:mm:ss'),
          EndTime:moment(this.valuedatetime2).format('YYYY-MM-DD HH:mm:ss'),
          TagClassValue:this.TagCode,
          EnergyClass:'汽'
        }
        this.axios.get('/api/selectIncrementStreamTableByTag',{params:params}).then((res) => {
         this.dates = res.data.map(function (item) {
                return item.CollectionDate.slice(11, 19)
              })
        this.dataline1 = res.data.map(function (item) {
                  return +item.IncremenValue;
               });
        this.yvaluemax=Math.max.apply(Math, this.dataline1).toFixed(0)//初始y轴坐标值
        this.yvaluemin=Math.min.apply(Math, this.dataline1).toFixed(0)//初始y轴坐标值
        this.drawLine(this.dataline1,this.dateset,this.yvaluemax,this.yvaluemin);
        })
      },
    drawLine(dataline1,dateset,yvaluemax,yvaluemin){
        if(this.myChart){
          this.myChart.dispose()
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
