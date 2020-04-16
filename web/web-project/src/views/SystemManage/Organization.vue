<template>
  <el-row>
    <el-col :span="24">
      <el-form :inline="true">
        <el-form-item>
          <el-radio-group v-model="layoutValue" fill="#082F4C" size="small" @change="changeSettings">
            <el-radio-button v-for="item in layoutSettings" :key="item.label" :label="item.label"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-radio-group v-model="orientValue" fill="#082F4C" size="small" @change="changeSettings">
            <el-radio-button v-for="item in orientSettings" :key="item.label" :label="item.label"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-radio-group v-model="positionValue" fill="#082F4C" size="small" @change="changeSettings">
            <el-radio-button v-for="item in positionSettings" :key="item.label" :label="item.label"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-radio-group v-model="roamValue" fill="#082F4C" size="small" @change="changeSettings">
            <el-radio-button v-for="item in roamSettings" :key="item.label" :label="item.label"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-radio-group v-model="DepthValue" fill="#082F4C" size="small" @change="changeSettings">
            <el-radio-button v-for="item in DepthSettings" :key="item.label" :label="item.label"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="曲度：" style="">
          <div style="width: 100px;">
            <el-slider v-model="sliderValue" :max="1" :min="0" :step="0.1" @input="changeSettings"></el-slider>
          </div>
        </el-form-item>
        <el-form-item>
          <el-radio-group v-model="modeValue" fill="#082F4C" size="small">
            <el-radio-button v-for="item in modeSettings" :key="item.label" :label="item.label"></el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <div class="chartContainer">
        <ve-tree :data="chartData" :settings="chartSettings" :extend="chartExtend" :events="events" height="600px"></ve-tree>
      </div>
      <el-drawer title="我是标题" :visible.sync="drawer" :with-header="false">
        <div style="padding: 20px;">
          <h3>{{ drawerTitle }}</h3>
          <el-form :model="organizationForm" label-width="80px" :rules="rules" ref="ruleForm">
            <el-form-item label="id">
              <el-input v-model="organizationForm.id" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="节点名称" prop="name">
              <el-input v-model="organizationForm.name"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="save('ruleForm')">保存</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-drawer>
    </el-col>
  </el-row>
</template>

<script>
  const tree1Data = {
    name: '好护士药业有限责任公司',
    value: 1,
    children: [
      {name: '生产部',value: 1,children: [
        {name: '配料',value: 2},
        {name: '压片',value: 2},
        {name: '包衣',value: 2,children: [
          {name: '老张',value: 2},
          {name: '老李',value: 2},
          {name: '老王',value: 2},
          {name: '老赵',value: 2}
        ]},
        {name: '内包装',value: 2,children: [
          {name: '老周',value: 2},
          {name: '老吴',value: 2}
        ]},
        {name: '外包装',value: 2}
      ]},
      {name: '质检部',value: 1,children: [
          {name: '原料检验',value: 2},
          {name: '辅料检验',value: 2},
          {name: '包材检验',value: 2},
          {name: '半成品检验',value: 2},
          {name: '成品检验',value: 2}
        ]
      },
      {name: '物流部',value: 1,children: [
          {name: '物流主管',value: 2},
          {name: '中药仓',value: 2},
          {name: '车队',value: 2},
          {name: '拣货',value: 2},
          {name: '扫描',value: 2},
          {name: '市场',value: 2},
          {name: '退货',value: 2},
          {name: '送货',value: 2},
        ]
      },
      {name: '设备部',value: 3,children: [
          {name: '部长',value: 4},
          {name: '经理',value: 2},
          {name: '维修工',value: 2}
        ]
      }
    ]
  }
  const tree2Data = {
    name: '好护士药业有限责任公司',
    value: 1,
    children: [
      {name: '提取二车间',value: 1,children: [
          {name: '提取段',value: 2},
        ]
      },
      {name: '综合车间',value: 1,children: [
          {name: '煎煮段',value: 2},
          {name: '浓缩段',value: 2},
          {name: '提取段',value: 2},
        ]
      },
      {name: '新建综合制剂楼',value: 1,children: [
          {name: '收粉段',value: 2},
        ]
      }
    ]
  }
  export default {
    name: "Organization",
    data(){
      var self = this
      this.events = {
        click:function(e){
          self.clickTree(e)
        }
      }
      return {
        orientValue:'向右',
        orientSettings: [
          {label:'向右'},
          {label:'向下'},
          {label:'向左'},
          {label:'向上'},
        ],
        positionValue:'标签靠右',
        positionSettings: [
          {label:'标签靠右'},
          {label:'靠下'},
          {label:'靠左'},
          {label:'靠上'},
        ],
        roamValue:'关闭',
        roamSettings: [
          {label:'关闭'},
          {label:'缩放'},
          {label:'平移'},
          {label:'缩放和平移'},
        ],
        layoutValue:'正交布局',
        layoutSettings: [
          {label:'正交布局'},
          {label:'径向布局'}
        ],
        DepthValue:'展示全部',
        DepthSettings: [
          {label:'展示全部'},
          {label:'3层'},
          {label:'2层'},
          {label:'1层'}
        ],
        modeValue:'查看模式',
        modeSettings: [
          {label:'查看模式'},
          {label:'添加子节点'},
          {label:'修改'},
          {label:'删除'},
        ],
        sliderValue:0.5,
        chartSettings: {
          seriesMap:{
            tree1: {
              top: '5%',
              left: '5%',
              bottom: '5%',
              right: '50%',
              orient: 'LR',
              lineStyle:{
                curveness:0.5,
                width: 1.5,
                color: "#B9B9B9"
              },
              roam:false,
              layout:"orthogonal",
              initialTreeDepth:-1,
              symbolSize: 8,
              label:{
                position: 'right',
              },
              itemStyle:{
                color:"#228AD5",
                borderColor:"#082F4C"
              }
            },
            tree2: {
              top: '5%',
              left: '55%',
              bottom: '5%',
              right: '5%',
              orient: 'LR',
              lineStyle:{
                curveness:0.5,
                width: 1.5,
                color: "#B9B9B9"
              },
              roam:false,
              layout:"orthogonal",
              initialTreeDepth:-1,
              symbolSize: 8,
              label:{
                position: 'right',
              },
              itemStyle:{
                color:"#228AD5",
                borderColor:"#082F4C"
              }
            },
          },
        },
        chartExtend: {
          tooltip: {

          },

        },
        chartData: {
          columns: ['name', 'value'],
          rows: [{
            name: 'tree1',
            value: [tree1Data]
          },
          {
            name:"tree2",
            value: [tree2Data]
          }]
        },
        drawer:false,
        drawerTitle:"",
        organizationForm:{
          id:"",
          name:""
        },
        rules:{
          name:[
            {required: true, message: '请输入节点名称', trigger: 'blur'}
          ],
        },
      }
    },
    methods: {
      changeSettings(a){
        this.chartSettings.seriesMap.tree1.lineStyle.curveness = this.sliderValue
        this.chartSettings.seriesMap.tree2.lineStyle.curveness = this.sliderValue
        if(a === "向下"){
          this.chartSettings.seriesMap.tree1.orient="TB"
          this.chartSettings.seriesMap.tree2.orient="TB"
        }else if(a === "向右"){
          this.chartSettings.seriesMap.tree1.orient="LR"
          this.chartSettings.seriesMap.tree2.orient="LR"
        }else if(a === "向左"){
          this.chartSettings.seriesMap.tree1.orient="RL"
          this.chartSettings.seriesMap.tree2.orient="RL"
        }else if(a === "向上"){
          this.chartSettings.seriesMap.tree1.orient="BT"
          this.chartSettings.seriesMap.tree2.orient="BT"
        }else if(a === "关闭"){
          this.chartSettings.seriesMap.tree1.roam=false
          this.chartSettings.seriesMap.tree2.roam=false
        }else if(a === "缩放"){
          this.chartSettings.seriesMap.tree1.roam="scale"
          this.chartSettings.seriesMap.tree2.roam="scale"
        }else if(a === "平移"){
          this.chartSettings.seriesMap.tree1.roam="move"
          this.chartSettings.seriesMap.tree2.roam="move"
        }else if(a === "缩放和平移"){
          this.chartSettings.seriesMap.tree1.roam=true
          this.chartSettings.seriesMap.tree2.roam=true
        }else if(a === "正交布局"){
          this.chartSettings.seriesMap.tree1.layout="orthogonal"
          this.chartSettings.seriesMap.tree2.layout="orthogonal"
        }else if(a === "径向布局"){
          this.chartSettings.seriesMap.tree1.layout="radial"
          this.chartSettings.seriesMap.tree2.layout="radial"
        }else if(a === "展示全部"){
          this.chartSettings.seriesMap.tree1.initialTreeDepth=-1
          this.chartSettings.seriesMap.tree2.initialTreeDepth=-1
        }else if(a === "1层"){
          this.chartSettings.seriesMap.tree1.initialTreeDepth=0
          this.chartSettings.seriesMap.tree2.initialTreeDepth=0
        }else if(a === "2层"){
          this.chartSettings.seriesMap.tree1.initialTreeDepth=1
          this.chartSettings.seriesMap.tree2.initialTreeDepth=1
        }else if(a === "3层"){
          this.chartSettings.seriesMap.tree1.initialTreeDepth=2
          this.chartSettings.seriesMap.tree2.initialTreeDepth=2
        }else if(a === "标签靠右"){
          this.chartSettings.seriesMap.tree1.label.position="right"
          this.chartSettings.seriesMap.tree2.label.position="right"
        }else if(a === "靠下"){
          this.chartSettings.seriesMap.tree1.label.position="bottom"
          this.chartSettings.seriesMap.tree2.label.position="bottom"
        }else if(a === "靠左"){
          this.chartSettings.seriesMap.tree1.label.position="left"
          this.chartSettings.seriesMap.tree2.label.position="left"
        }else if(a === "靠上"){
          this.chartSettings.seriesMap.tree1.label.position="top"
          this.chartSettings.seriesMap.tree2.label.position="top"
        }
      },
      clickTree(e){
        console.log(e)
        this.drawerTitle = this.modeValue
        if(this.modeValue === "添加子节点"){
          this.drawer = true
          this.organizationForm = {
            id:"",
            name:""
          }
        }else if(this.modeValue === "修改"){
          this.drawer = true
          this.organizationForm = {
            id:e.data.id,
            name:e.data.name
          }
        }else if(this.modeValue === "删除"){
          this.$confirm('此操作将永久删除该节点, 是否继续?', '删除节点'+e.data.name, {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            this.$message({
              type: 'success',
              message: '删除成功!'
            });
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消删除'
            });
          });
        }
      },
      save(formName){
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.$message({
              type: 'success',
              message: "保存成功"
            });
            this.drawer = false
          } else {
            return false;
          }
        });
      }
    }
  }
</script>

<style scoped>
  .chartContainer{
    padding: 15px;
    background: #fff;
    border-radius: 4px;
    clear: both;
    overflow: inherit;
  }
</style>
