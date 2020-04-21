<template>
  <el-row>
    <el-col :span="24">
      <div class="card-head">
        <i v-if="showTypeValue === '看板视图'" class="el-icon-share" style="color: #FB3A06"></i>
        <i v-if="showTypeValue === '表格视图'" class="el-icon-s-grid" style="color: #FB3A06"></i>
        <span style="margin-left: 10px;" class="text-size-normol">组织结构</span>
        <el-select class="card-head-select" v-model="showTypeValue" placeholder="请选择">
          <el-option v-for="(item,index) in showType" :key="index" :value="item.value" v-html="item.label"></el-option>
        </el-select>
      </div>
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
        <ve-tree :data="chartData" :settings="chartSettings" :events="events" height="600px"></ve-tree>
      </div>
      <el-drawer :visible.sync="departmentDrawer" :with-header="false">
        <div style="padding: 20px;">
          <h3>{{ drawerTitle }}</h3>
          <el-form :model="departmentForm" label-width="80px" :rules="rules" ref="ruleForm">
            <el-form-item label="父节点">
              <el-input v-model="departmentForm.factory_name" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="部门名称" prop="department_name">
              <el-input v-model="departmentForm.department_name"></el-input>
            </el-form-item>
            <el-form-item label="部门编码" prop="department_code">
              <el-input v-model="departmentForm.department_code"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="departmentSave('ruleForm')">保存</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-drawer>
    </el-col>
  </el-row>
</template>

<script>
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
        showTypeValue:"看板视图",
        showType:[
          {label:"<i class='el-icon-share'></i>看板视图",value:"看板视图"},
          {label:"<i class='el-icon-s-grid'></i>表格视图",value:"表格视图"}
        ],
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
            tree: {
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
            }
          },
        },
        chartData: {
          columns: ['name', 'value'],
          rows: [
            {name:"tree",value: []}
          ]
        },
        departmentDrawer:false,
        drawerTitle:"",
        clicktype:"",
        departmentForm:{
          id:"",
          factory_name:"",
          department_name:"",
          department_code:""
        },
        delDepartmentCode:"",
        delDepartmentName:"",
        rules:{
          department_name:[
            {required: true, message: '请输入部门名称', trigger: 'blur'}
          ],
          department_code:[
            {required: true, message: '请输入部门编码', trigger: 'blur'}
          ]
        },
      }
    },
    created(){
      this.getTreeData()
    },
    methods: {
      getTreeData(){
        var that = this
        this.axios.get("/api/system_tree").then(res => {
          that.chartData.rows[0].value = [res.data]
        })
      },
      changeSettings(a){
        this.chartSettings.seriesMap.tree.lineStyle.curveness = this.sliderValue
        if(a === "向下"){
          this.chartSettings.seriesMap.tree.orient="TB"
        }else if(a === "向右"){
          this.chartSettings.seriesMap.tree.orient="LR"
        }else if(a === "向左"){
          this.chartSettings.seriesMap.tree.orient="RL"
        }else if(a === "向上"){
          this.chartSettings.seriesMap.tree.orient="BT"
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
        }else if(a === "标签靠右"){
          this.chartSettings.seriesMap.tree.label.position="right"
        }else if(a === "靠下"){
          this.chartSettings.seriesMap.tree.label.position="bottom"
        }else if(a === "靠左"){
          this.chartSettings.seriesMap.tree.label.position="left"
        }else if(a === "靠上"){
          this.chartSettings.seriesMap.tree.label.position="top"
        }
      },
      clickTree(e){
        console.log(e)
        var clickType = e.data.type
        this.drawerTitle = this.modeValue
        if(this.modeValue === "添加子节点"){
          if(clickType === "factory"){
            this.departmentDrawer = true
            this.departmentForm = {
              factory_name:e.data.name,
              department_name:"",
              department_code:""
            }
          }else if(clickType === "department"){

          }else if(clickType === "role"){

          }else if(clickType === "user"){

          }
        }else if(this.modeValue === "修改"){
          if(clickType === "factory"){

          }else if(clickType === "department"){
            this.departmentDrawer = true
            this.departmentForm = {
              id:e.data.id,
              department_name:e.data.name,
              department_code:e.data.value
            }
          }else if(clickType === "role"){

          }else if(clickType === "user"){

          }
        }else if(this.modeValue === "删除"){
          this.$confirm('此操作将永久删除'+ e.data.name +'节点, 是否继续?', '删除节点'+e.data.name, {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            var headers = {
              department_code:e.data.value
            }
            this.axios.delete("/api/system_tree/delete_department",{headers:headers}).then(res => {
              console.log(res.data)
              if(res.data.code === 10001){
                this.$message({
                  type: 'success',
                  message: res.data.msg
                });
                this.departmentDrawer = false
                this.getTreeData()
              }else{
                this.$message({
                  type: 'info',
                  message: "新增失败"
                });
              }
            })
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
      departmentSave(formName){
        this.$refs[formName].validate((valid) => {
          if (valid) {
            if(this.drawerTitle === "添加子节点"){
              this.axios.post("/api/system_tree/add_department",this.departmentForm).then(res => {
                if(res.data.code === 10000){
                  this.$message({
                    type: 'success',
                    message: res.data.msg
                  });
                  this.departmentDrawer = false
                  this.getTreeData()
                }else{
                  this.$message({
                    type: 'info',
                    message: "新增失败"
                  });
                }
              })
            }else if(this.drawerTitle === "修改"){
              console.log(this.departmentForm)
              this.axios.patch("/api/system_tree/update_department",this.departmentForm).then(res => {
                if(res.data.code === 10002){
                  this.$message({
                    type: 'success',
                    message: res.data.msg
                  });
                  this.departmentDrawer = false
                  this.getTreeData()
                }else{
                  this.$message({
                    type: 'info',
                    message: "修改失败"
                  });
                }
              })
            }
          } else {
            return false;
          }
        });
      }
    }
  }
</script>

<style scoped>
  .card-head{
    width: 100%;
    margin-bottom:10px;
    background: #082F4C;
    color: #fff;
    font-size: 18px;
    height: 48px;
    line-height: 48px;
    padding: 0 10px;
    border-radius:4px;
  }
  .card-head-select{
    float: right;
    width: 100px;
  }
  .chartContainer{
    padding: 15px;
    background: #fff;
    border-radius: 4px;
    clear: both;
    overflow: inherit;
  }
</style>
