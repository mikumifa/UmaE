import ChampMeet from "@/components/ChampMeet.vue";
import TeamRace from "@/components/TeamRace.vue";

const routes = [
  { path: "/", redirect: "/champions-meeting" },
  { path: "/champions-meeting", component: ChampMeet },
  { path: "/team-race", component: TeamRace },
];

export default routes;
