<template>
  <el-row style="height: 100%;background: #fff;">
    <el-col :span="24">
      <TreeChart :json="treeData"/>
    </el-col>
  </el-row>
</template>

<script>
  import TreeChart from 'vue-tree-chart'
  export default {
    name: "Organization",
    components: {
      TreeChart
    },
    data(){
      return {
        treeData: {
          id: 0,
          name: "XXX科技有限公司",
          children: [
            {id: 2,name: "产品研发部",
              children: [
                {id: 5,name: "研发-前端"},
                {id: 6,name: "研发-后端"},
                {id: 9,name: "UI设计"},
                {id: 10,name: "产品经理"}
              ]
            },
            {id: 3,name: "销售部",
              children: [
                {id: 7,name: "销售一部"},
                {id: 8,name: "销售二部"}
              ]
            },
            {id: 4,name: "财务部"},
            {id: 9,name: "HR人事"}
          ]
        },
        showBox: false,
				tranLeft: 0, // 向左偏移
				tranTop: 0,  // 向右偏移
        selectedId:"", //选中节点的id
        selectedLabel:"" //选中节点的label
      };
    },
    methods: {
      renderContent (h, data) {
        return data.label
      },
      onNodeClick(e, data) {
        this.tranLeft = (e.pageX - 240) + 'px'
				this.tranTop = (e.pageY - 60) + 'px'
        if(this.selectedId == data.id && this.showBox){
          this.showBox = false
        }else{
          this.showBox = true
        }
        this.selectedId = data.id
        this.selectedLabel = data.label
      },
      addNode(){
        var treeData = this.treeData
        this.showBox = false
        this.$prompt('请输入子节点名称', '给'+this.selectedLabel+'添加子节点', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
        }).then(({ value }) => {
          this.$message({
            type: 'success',
            message: '已成功为' + this.selectedLabel + '添加子节点：' + value
          });
        }).catch(action => {
          console.log(action)
          this.$message({
            type: 'info',
            message: '取消添加'
          });
        });
      },
      editNode(){
        this.showBox = false
        this.$prompt('请输入子节点名称', '修改'+this.selectedLabel+'的名称', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
        }).then(({ value }) => {
          this.$message({
            type: 'success',
            message: '已将' + this.selectedLabel + '修改为：' + value
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消修改'
          });
        });
      },
      delNode(){
        this.showBox = false
        this.$confirm('此操作将永久删除该节点, 是否继续?', '删除'+this.selectedLabel+'节点', {
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
    }
  }
</script>

<style scoped>
  .org-tree-node-label {
    white-space: nowrap;
  }
  .show-parent {
    position: absolute;
    box-shadow: 0 0 2px #8c939d;
    z-index: 1;
  }
  .show-parent li{
    padding: 10px;
    color: #082F4C;
    background-color: #ffffff;
    cursor: pointer;
  }
  .show-parent li:hover{
    color: #ffffff;
    background-color: #082F4C;
  }
</style>
