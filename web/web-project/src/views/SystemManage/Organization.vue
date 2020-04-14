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
          <el-radio-group v-model="roamValue" fill="#082F4C" size="small" @change="changeSettings">
            <el-radio-button v-for="item in roamSettings" :key="item.label" :label="item.label"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-radio-group v-model="DepthValue" fill="#082F4C" size="small" @change="changeSettings">
            <el-radio-button v-for="item in DepthSettings" :key="item.label" :label="item.label"></el-radio-button>
          </el-radio-group>
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
  const treeData = {
    name: '好护士药业有限责任公司',
    value: 1,
    children: [
      {
        name: 'a',
        value: 1,
        children: [
          {
            name: 'a-a',
            value: 2
          },
          {
            name: 'a-b',
            value: 2
          }
        ]
      },
      {
        name: 'b',
        value: 1,
        children: [
          {
            name: 'b-a',
            value: 2
          },
          {
            name: 'b-b',
            value: 2
          }
        ]
      },
      {
        name: 'c',
        value: 3,
        children: [
          {
            name: 'c-a',
            value: 4
          },
          {
            name: 'c-b',
            value: 2
          }
        ]
      },
      {
        name: 'd',
        value: 3,
        children: [
          {
            name: 'd-a',
            value: 4
          },
          {
            name: 'd-b',
            value: 2
          }
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
        orientValue:'水平',
        orientSettings: [
          {label:'水平'},
          {label:'垂直'}
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
        chartSettings: {
          seriesMap:{
            tree:{
              orient: 'LR',
              lineStyle:{
                curveness:0.5,
                width: 1.5,
                color: "#B9B9B9"
              },
              roam:false,
              layout:"orthogonal",
              initialTreeDepth:-1,
              edgeShape: 'curve',
              symbolSize: 8,
              label:{
                position: 'bottom',
              },
              itemStyle:{
                color:"#228AD5",
                borderColor:"#082F4C"
              }
            }
          },
        },
        chartExtend: {
          tooltip: {

          },

        },
        chartData: {
          columns: ['name', 'value'],
          rows: [{
            name: 'tree',
            value: [treeData]
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
        if(a === "垂直"){
          this.chartSettings.seriesMap.tree.orient="TB"
        }else if(a === "水平"){
          this.chartSettings.seriesMap.tree.orient="LR"
        }else if(a === "关闭"){
          this.chartSettings.seriesMap.tree.roam=false
        }else if(a === "缩放"){
          this.chartSettings.seriesMap.tree.roam="scale"
        }else if(a === "平移"){
          this.chartSettings.seriesMap.tree.roam="move"
        }else if(a === "缩放和平移"){
          this.chartSettings.seriesMap.tree.roam=true
        }else if(a === "正交布局"){
          this.chartSettings.seriesMap.tree.layout="orthogonal"
        }else if(a === "径向布局"){
          this.chartSettings.seriesMap.tree.layout="radial"
        }else if(a === "展示全部"){
          this.chartSettings.seriesMap.tree.initialTreeDepth=-1
        }else if(a === "1层"){
          this.chartSettings.seriesMap.tree.initialTreeDepth=0
        }else if(a === "2层"){
          this.chartSettings.seriesMap.tree.initialTreeDepth=1
        }else if(a === "3层"){
          this.chartSettings.seriesMap.tree.initialTreeDepth=2
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
