import ChampMeet from "@/components/ChampMeet.vue";

const routes = [
  { path: "/", redirect: "/champions-meeting" },
  { path: "/champions-meeting", component: ChampMeet },
];

export default routes;
