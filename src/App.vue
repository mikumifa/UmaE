<template>
  <div id="app">

    <ChampMeet></ChampMeet>
    <div>
      数据更新时间：
      <span class="font-mono text-gray-900">
        {{ this.buildTime }}
      </span>
    </div>
    <div class="text-gray-600 p-4">
      本项目是在
      <a href="https://twitter.com/urakagi" target="_blank" rel="noopener noreferrer"
        class="text-blue-600 hover:underline">
        @urakagi
      </a>
      的赛马娘模拟器基础上修改构建而成。
    </div>
  </div>
</template>

<script>
import ChampMeet from "@/components/ChampMeet.vue";
export default {
  name: "App",
  components: { ChampMeet },
  data() {
    return {
      navLink: ["/team-race", "/champions-meeting"],
      buildTime: ''
    };
  },
  created() {
    fetch('./build-time.txt')
      .then(res => res.text())
      .then(time => {
        this.buildTime = new Date(time).toLocaleString()
      })
      .catch(() => {
        this.buildTime = '未知'
      })
  },

};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
