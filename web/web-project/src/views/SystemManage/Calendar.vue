<template>
  <full-calendar :events="events" :config="config"></full-calendar>
</template>

<script>
  import 'fullcalendar/dist/fullcalendar.css'
  export default {
    name: "Calendar",
    data(){
      return {
        events:[
          {title:"event1",start:"2020-02-18"},
          {title:"event1",start:"2020-02-20",end:"2020-02-22"},
          {title:"event1",start:"2020-02-24"}
        ],
        config:{
          locale:'zh-cn',
          defaultView: "month",
          height:'auto',
          editable:true,
          /* 设置按钮文字 */
          buttonText:{
            today:'今天',
          }
        }
      }
    }
  }
</script>

<style scoped>

</style>
