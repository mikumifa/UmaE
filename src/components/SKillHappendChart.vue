<template>
    <div class="flex justify-start max-w-96 my-4 rounded-2xl shadow-md p-6">
        <!-- 图表区域 -->
        <div class="h-[600px] w-full max-h-[600px] mr-16" ref="chartRef"></div>
        <!-- 表单+表格区域 -->
        <div class="h-[600px]  max-h-[600px]">
            <div>
                <!-- 输入区 -->
                <div class="flex gap-2 items-center mb-2">
                    <label
                        class="m-2 font-semibold text-gray-700 whitespace-nowrap overflow-hidden text-ellipsis block">{{
                            $t("message.from") }}</label>
                    <input v-model.number="skillFrom" type="number" class="border px-2 py-1 w-20 text-xs" />
                    <label
                        class="m-2 font-semibold text-gray-700 whitespace-nowrap overflow-hidden text-ellipsis block">{{
                            $t("message.to") }}</label>
                    <input v-model.number="skillTo" type="number" class="border px-2 py-1 w-20 text-xs" />
                </div>

                <!-- Element Plus 表格 -->
                <el-table :data="skillRates" style="width: 100%" max-height="540px" :empty-text="$t('message.noData')"
                    size="small">
                    <el-table-column width="100px" show-overflow-tooltip sortable prop="name"
                        :label="$t('message.skillName')" />
                    <el-table-column sortable prop="rate" :label="$t('message.skillRate')" />
                </el-table>
            </div>
        </div>
    </div>

</template>

<script>
import * as echarts from 'echarts';

export default {
    name: 'SkillHappendChart',
    data() {
        return {
            chart: null,
            skillFrom: null,
            skillTo: null,
            skillRates: [],
            skillChartOptions: null
        }
    },
    mounted() {
        this.initChart();
        this.updateSkillRates()
    },

    watch: {
        '$parent.$parent.skillChartOptions': {
            // eslint-disable-next-line no-unused-vars
            handler(newVal, _) {
                console.log('skillChartOptions changed:', newVal);
                this.updateSkillRates();
            },
            deep: true
        },
        skillFrom: {
            handler: 'updateSkillRates',
            deep: true
        }, skillTo: {
            handler: 'updateSkillRates',
            deep: true
        }
    },
    methods: {
        updateSkillRates() {
            const from = this.skillFrom != null ? this.skillFrom : 0;
            const to = this.skillTo != null ? this.skillTo : 9999;
            this.getSkillsRate(from, to);
            this.skillChartOptions = this.$parent.$parent.skillChartOptions;
            this.skillPosDatasets = this.$parent.$parent.skillPosDatasets;
            this.chart.setOption(this.$parent.$parent.skillChartOptions);
        },
        getSkillsRate(from, to) {
            const releaseSkills = this.$parent.$parent.ReleaseSkills;
            const maxEpoch = this.$parent.$parent.maxEpoch
            const fromInt = Math.round(from);
            const toInt = Math.round(to);
            const skillEpochMap = new Map();
            for (const skill of releaseSkills) {
                const roundedX = Math.round(skill.pos);
                if (roundedX < fromInt || roundedX > toInt) continue;

                const name = skill.data.name;
                const epoch = skill.epoch;

                if (!skillEpochMap.has(name)) {
                    skillEpochMap.set(name, new Set());
                }
                skillEpochMap.get(name).add(epoch);
            }
            const skillRateMap = [];
            const sortedEntries = Array.from(skillEpochMap.entries()).sort(([a], [b]) => a.localeCompare(b));
            for (const [name, epochs] of sortedEntries) {
                skillRateMap.push({
                    name: name,
                    rate: Number((epochs.size / maxEpoch).toFixed(4))
                });
            }
            this.skillRates = skillRateMap;
        },
        initChart() {
            this.chart = echarts.init(this.$refs.chartRef);
            this.chart.setOption(this.$parent.$parent.skillChartOptions);
            window.addEventListener('resize', () => {
                this.chart.resize();
            });
            this.chart.on('dataZoom', () => {
                const zoom = this.chart.getOption().dataZoom?.[0];
                this.skillFrom = zoom?.startValue ?? 0;
                this.skillTo = zoom?.endValue ?? this.$parent.$parent.courseLength;
            });
        }
    },

}
</script>
