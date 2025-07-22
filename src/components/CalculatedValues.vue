<template>
  <div>

    <!-- 总状态 + 修正值 -->
    <div class="p-4 space-y-2rounded shadow-sm">
      <!-- 总素质 -->
      <div class="flex items-center flex-wrap gap-2">
        <span class="font-semibold text-gray-700">{{ $t("message.totalStatus") }}：</span>
        <span class="px-3 py-1 rounded bg-gray-500 text-white text-xs font-semibold">
          {{ typeof totalStatus === 'number' && !isNaN(totalStatus)
            ? totalStatus.toFixed(1) : '-' }}
        </span>
      </div>

      <!-- 补正后各项属性 -->
      <div class="flex items-center flex-wrap gap-2">
        <span class="font-semibold text-gray-700">{{ $t("message.corrected") }}：</span>
        <span class="box px-3 py-1 rounded-lg speed text-white text-xs font-semibold">
          {{ $t("message.speed") }} {{ typeof $parent.modifiedSpeed === 'number' && !isNaN($parent.modifiedSpeed) ?
            $parent.modifiedSpeed.toFixed(1) : '-' }}
        </span>
        <span class="box px-3 py-1 rounded-lg stamina text-white text-xs font-semibold">
          {{ $t("message.stamina") }} {{ typeof $parent.modifiedStamina === 'number' && !isNaN($parent.modifiedStamina)
            ? $parent.modifiedStamina.toFixed(1) : '-' }}
        </span>
        <span class="box px-3 py-1 rounded-lg power text-white text-xs font-semibold">
          {{ $t("message.power") }} {{ typeof $parent.modifiedPower === 'number' && !isNaN($parent.modifiedPower) ?
            $parent.modifiedPower.toFixed(1) : '-' }}
        </span>
        <span class="box px-3 py-1 rounded-lg guts text-white text-xs font-semibold">
          {{ $t("message.guts") }} {{ typeof $parent.modifiedGuts === 'number' && !isNaN($parent.modifiedGuts) ?
            $parent.modifiedGuts.toFixed(1) : '-' }}
        </span>
        <span class="box px-3 py-1 rounded-lg wisdom text-white text-xs font-semibold">
          {{ $t("message.wisdom") }} {{ typeof $parent.modifiedWisdom === 'number' && !isNaN($parent.modifiedWisdom) ?
            $parent.modifiedWisdom.toFixed(1) : '-' }}
        </span>
      </div>
    </div>

    <!-- 起始HP与等效耐力 -->
    <div class="flex items-center flex-wrap gap-2">
      <span class="font-semibold text-gray-700">{{ $t("message.startHP") }}：</span>
      <span class="box corner px-2 py-1 rounded bg-cyan-600 text-white text-xs font-semibold">
        {{ formatNumber($parent.spMax, 1, defaultValue = 0) }}
      </span>

      <span class="font-semibold text-gray-700">{{ $t("message.rareHP") }}≒</span>
      <span class="box corner px-2 py-1 rounded bg-emerald-600 text-white text-xs font-semibold">
        {{ formatNumber(getEqualStamina(550), 1, defaultValue = 0) }} {{ $t("message.stamina") }}
      </span>

      <span class="font-semibold text-gray-700">{{ $t("message.normalHP") }}≒</span>
      <span class="box corner px-2 py-1 rounded bg-emerald-400 text-white text-xs font-semibold">
        {{ formatNumber(getEqualStamina(150), 1, defaultValue = 0) }} {{ $t("message.stamina") }}
      </span>

      <span class="font-semibold text-gray-700">{{ $t("message.spurtCoeff") }}：</span>
      <span class="box corner px-2 py-1 rounded bg-indigo-600 text-white text-xs font-semibold">
        {{ formatNumber($parent.spurtSpCoef, 3, defaultValue = 0) }}
      </span>
    </div>

    <!-- 技能与气质 -->
    <div class="flex items-center flex-wrap gap-2">
      <span class="font-semibold text-gray-700">{{ $t("message.skillActivateRate") }}：</span>
      <span class="box corner px-2 py-1 rounded bg-orange-500 text-white text-xs font-semibold">
        {{ formatNumber($parent.skillActivateRate, 1) }}％
      </span>

      <span class="font-semibold text-gray-700"> {{ $t("message.temperamentRate") }}：</span>
      <span class="box corner px-2 py-1 rounded bg-red-500 text-white text-xs font-semibold">
        {{ formatNumber($parent.temptationRate, 1, defaultValue = 0) }}％
      </span>
    </div>

    <!-- v0 / a0 -->
    <div class="flex items-center flex-wrap gap-2">
      <span class="font-semibold text-gray-700">{{ $t("message.v0") }}：</span>
      <span class="box corner px-2 py-1 rounded bg-lime-600 text-white text-xs font-semibold">
        {{ formatNumber($parent.v0, 2) }}
      </span>

      <span class="font-semibold text-gray-700">{{ $t("message.a0") }}：</span>
      <span class="box corner px-2 py-1 rounded bg-lime-400 text-white text-xs font-semibold">
        {{ formatNumber($parent.a0, 3) }}
      </span>
    </div>





    <!-- 各阶段速度/加速度 表格 -->
    <div class="max-w-md mx-0 my-4 overflow-auto">
      <table class="table-auto border border-gray-300 text-center text-xs">
        <thead class="bg-gray-100">
          <tr>
            <th class="border px-6 py-3">{{ $t("chart.phase") }}</th>
            <th class="border px-6 py-3">{{ $t("chart.targetSpeed") }}</th>
            <th class="border px-6 py-3">{{ $t("chart.acceleration") }}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="border px-6 py-3">{{ $t("chart.start") }}</td>
            <td class="border px-6 py-3">{{ $parent.v1.toFixed(2) }}</td>
            <td class="border px-6 py-3">{{ $parent.a1.toFixed(3) }}</td>
          </tr>
          <tr>
            <td class="border px-6 py-3">{{ $t("chart.opening") }}</td>
            <td class="border px-6 py-3">{{ $parent.v1.toFixed(2) }}</td>
            <td class="border px-6 py-3">{{ $parent.a1.toFixed(3) }}</td>
          </tr>
          <tr>
            <td class="border px-6 py-3">{{ $t("chart.mid") }}</td>
            <td class="border px-6 py-3">{{ $parent.v2.toFixed(2) }}</td>
            <td class="border px-6 py-3">{{ $parent.a2.toFixed(3) }}</td>
          </tr>
          <tr>
            <td class="border px-6 py-3">{{ $t("chart.final") }}</td>
            <td class="border px-6 py-3">{{ $parent.v3.toFixed(2) }}</td>
            <td class="border px-6 py-3">{{ $parent.a3.toFixed(3) }}</td>
          </tr>
          <tr>
            <td class="border px-6 py-3">{{ $t("message.maxSpurtSpeed") }}</td>
            <td class="border px-6 py-3">{{ $parent.maxSpurtSpeed.toFixed(2) }}</td>
            <td class="border px-6 py-3">—</td>
          </tr>
        </tbody>
      </table>
    </div>




    <!-- 逃げ or 大逃げ限定 -->
    <div v-if="$parent.runningStyle == 1 || $parent.runningStyle == 10">
      <span class="font-semibold">{{ $t("message.leadCompetitionSpeed") }}：</span>
      {{ $parent.systematicSkills.leadCompetition.targetSpeed.toFixed(3) }}
      ／
      <span class="font-semibold">{{ $t("message.leadCompetitionDuration") }}：</span>
      {{ $parent.systematicSkills.leadCompetition.duration.toFixed(1) }}
      ／
      <span class="font-semibold">{{ $t("message.leadCompetitionAdvantage") }}：</span>
      {{
        (
          ($parent.systematicSkills.leadCompetition.duration *
            $parent.systematicSkills.leadCompetition.targetSpeed) / 2.5
        ).toFixed(2)
      }}
      ／
      <span class="font-semibold">{{ $t("message.leadCompetitionHP") }}：</span>
      {{ $parent.leadCompetitionUsage.toFixed(1) }}
    </div>
  </div>
</template>



<script>
export default {
  name: "CalculatedValues",
  computed: {
    totalStatus() {
      return (
        parseInt(this.$parent.umaStatus.speed) +
        parseInt(this.$parent.umaStatus.stamina) +
        parseInt(this.$parent.umaStatus.power) +
        parseInt(this.$parent.umaStatus.guts) +
        parseInt(this.$parent.umaStatus.wisdom)
      );
    },
  },
  methods: {
    getEqualStamina(value) {
      return Math.floor(
        (this.$parent.spMax * value) /
        10000.0 /
        0.8 /
        this.$parent.styleSpCoef[this.$parent.runningStyle]
      );
    },
    formatNumber(value, digits = 1, defaultValue = '-') {
      if (typeof value === 'number' && !isNaN(value)) {
        return value.toFixed(digits) > 0 ? value.toFixed(digits) : 0;
      }
      return defaultValue; // 或者你想显示的默认值，比如 '0.0'
    }
  },
};
</script>

<style scoped>
.box {
  @apply inline-block px-2 py-1 m-0.5 mr-2 border border-gray-300 rounded-md text-sm;
}

.corner {
  @apply border-purple-300 text-purple-800;
}

.speed {
  display: inline-block;
  background: rgba(59, 130, 246, 0.2);
  /* Tailwind blue-500 */
}

.stamina {
  display: inline-block;
  background: rgba(34, 197, 94, 0.2);
  /* Tailwind green-500 */
}

.power {
  display: inline-block;
  background: rgba(239, 68, 68, 0.2);
  /* Tailwind red-500 */
}

.guts {
  display: inline-block;
  background: rgba(234, 179, 8, 0.2);
  /* Tailwind yellow-400 */
}

.wisdom {
  display: inline-block;
  background: rgba(168, 85, 247, 0.2);
  /* Tailwind purple-500 */
}
</style>