import Vue from "vue";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import App from "./App.vue";
import VueRouter from "vue-router";
import "tailwindcss/tailwind.css";
import i18n from "./i18n";
import routes from "@/routes";
import PluginUtils from "@/components/plugins/PluginUtils";
Vue.config.productionTip = false;
Vue.use(ElementUI);

Vue.use(require("vue-script2"));
Vue.use(VueRouter);
Vue.use(PluginUtils);
const router = new VueRouter({ routes });

new Vue({
  i18n,
  router,
  render: (h) => h(App),
}).$mount("#app");
