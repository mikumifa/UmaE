<template>
  <div class="max-w-96 my-4 rounded-2xl shadow-md p-6">

    <div class="flex items-center flex-wrap gap-2">
      <span class="font-semibold text-gray-700">{{ $t("chart.slope") }}：</span>
      <span v-for="slope in slopes" :key="slope"
        :class="['box px-2 py-1 rounded  text-xs font-semibold', slopeClass(slope)]">
        {{ slope }}
      </span>
    </div>

    <div class="flex items-center flex-wrap gap-2">
      <span class="font-semibold text-gray-700">{{ $t("chart.corner") }}：</span>
      <span v-for="corner in corners" :key="corner"
        class="box corner px-2 py-1 rounded bg-blue-500 text-xs font-semibold">
        {{ corner }}
      </span>
    </div>

    <div class="flex items-center flex-wrap gap-2">
      <span class="font-semibold text-gray-700">{{ $t("chart.straight") }}：</span>
      <span v-for="straight in straights" :key="straight"
        class="box straight px-2 py-1 rounded bg-green-500 text-xs font-semibold">
        {{ straight }}
      </span>
    </div>

    <div class="flex items-center flex-wrap gap-2 text-gray-600">
      <span class="font-semibold text-gray-700">
        {{
          $t("chart.phaseSeparators",
            [
              (trackDetail.distance / 6).toFixed(0),
              (trackDetail.distance * 2 / 3).toFixed(0)
            ])
        }}
      </span>
    </div>

    <div class="flex items-center flex-wrap gap-4 text-gray-600">
      <span class="font-semibold text-gray-700">
        {{ $t("message.displayStatusCheck") }}：
        <span class="box straight px-2 py-1 rounded bg-green-500 text-xs font-semibold">{{ displayStatusCheck
        }}</span>
      </span>
      <span class="font-semibold text-gray-700">
        {{ $t("message.minTime") }}：
        <span class="box straight px-2 py-1 rounded bg-green-500  text-xs font-semibold">
          {{ formatTime($parent.trackDetail.finishTimeMin, 1) }}
        </span>
      </span>
      <span class="font-semibold text-gray-700">
        ／{{ $t("message.maxTime") }}：
        <span class="box straight px-2 py-1 rounded bg-green-500 text-xs font-semibold">
          {{ formatTime($parent.trackDetail.finishTimeMax, 1) }}
        </span>
      </span>
    </div>

  </div>
</template>


<script>
import MixinCourseData from "./data/MixinCourseData"

export default {
  name: "CourseInfo",
  props: ['track'],
  mixins: [MixinCourseData],
  computed: {
    trackDetail() {
      if (!this.track.location) {
        return {
          distance: 0, surface: 1, turn: 1, distanceType: 1,
          courseSetStatus: [], corners: [], straights: [], slopes: [],
        }
      }
      return this.trackData[this.track.location].courses[this.track.course]
    },
    corners() {
      const ret = []
      for (const c of this.trackDetail.corners) {
        ret.push(`${c.start}m～${c.start + c.length}m`)
      }
      return ret
    },
    straights() {
      const ret = []
      for (const c of this.trackDetail.straights) {
        ret.push(`${c.start}m～${c.end}m`)
      }
      return ret
    },
    slopes() {
      const ret = []
      for (const slope of this.trackDetail.slopes) {
        const s = slope.slope > 0 ? `↑${slope.slope * 0.0001}` : `↓${-slope.slope * 0.0001}`
        ret.push(`${slope.start}m～${slope.start + slope.length}m (${s})`)
      }
      return ret
    },
    displayStatusCheck() {
      const STATUS = ['', this.$t("message.speed"), this.$t("message.stamina"), this.$t("message.power"), this.$t("message.guts"), this.$t("message.wisdom")]
      const check = this.$parent.trackDetail.courseSetStatus
      switch (check.length) {
        case 0:
          return this.$t("message.none")
        case 1:
          return STATUS[check[0]]
        case 2:
        default:
          return STATUS[check[0]] + '、' + STATUS[check[1]]
      }
    },
  },
  methods: {
    slopeClass(slope) {
      return slope.indexOf('↑') > 0 ? 'up-slope' : 'down-slope'
    },
  }
}
</script>

<style scoped>
.box {
  @apply inline-block px-2 py-1 m-0.5 mr-2 border border-gray-300 rounded-md text-sm;
}

.corner {
  @apply bg-purple-100 border-purple-300 text-purple-800;
}

.straight {
  display: inline-block;
  background: rgba(210, 235, 255, 0.2);
}

.up-slope {
  display: inline-block;
  background: rgba(240, 235, 105, 0.2);
}

.down-slope {
  display: inline-block;
  background: rgba(125, 255, 190, 0.2);
}
</style>
