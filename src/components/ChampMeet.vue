<template>
  <div class="main-frame">
    <el-form class="input-form" :inline="true">
      <el-form-item>
        <el-button @click="saveUma">{{ $t("message.saveUma") }}</el-button>
      </el-form-item>
      <el-form-item>
        <el-select v-model="umaToLoad" :placeholder="$t('message.umaToLoad')">
          <el-option v-for="(_, key) in savedUmas" :label="key" :value="key" :key="key"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button @click="loadUma">{{ $t("message.loadUma") }}</el-button>
      </el-form-item>
      <el-form-item>
        <el-popconfirm :confirm-button-text="$t('message.yes')" :cancel-button-text="$t('message.no')"
          :title="$t('message.deleteOrNot')" trigger="click" @confirm="removeUma">
          <el-button slot="reference">{{ $t("message.delete") }}</el-button>
        </el-popconfirm>
      </el-form-item>
      <el-form-item>
        <el-popconfirm :confirm-button-text="$t('message.yes')" :cancel-button-text="$t('message.no')"
          :title="$t('message.resetOrNot')" trigger="click" @confirm="resetUma">
          <el-button slot="reference">{{ $t("message.reset") }}</el-button>
        </el-popconfirm>
      </el-form-item>
      <el-form-item>
        <el-button @click="exportUma">{{ $t("message.exportUma") }}</el-button>
        <el-dropdown @command="importUma">
          <el-button>
            {{ $t("message.importUma")
            }}<i class="el-icon-arrow-down el-icon--right"></i>
          </el-button>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="tool">{{
              $t("message.importUmaFromTool")
            }}</el-dropdown-item>
            <el-tooltip content="race_horse_data / trained_chara">
              <el-dropdown-item command="game">{{
                $t("message.importUmaFromGame")
              }}</el-dropdown-item>
            </el-tooltip>
          </el-dropdown-menu>
        </el-dropdown>
      </el-form-item>

      <!-- Kua -->
      <el-form-item>
        <el-button @click="generateKuaWeights"> 大奶 </el-button>
        <el-input v-model="kua.baseSkillName" class="input-status"></el-input>
        <el-input v-model="kua.baseSkillPt" class="input-status"></el-input>
      </el-form-item>
      <el-dialog :visible.sync="kua.showKuaWeights" style="text-align: left">
        <p><el-button @click="copyKuaWeights">Copy</el-button></p>
        <p>
          {{ kuaWeightsOutputLine1 }}<br />
          {{ kuaWeightsOutputLine2 }}<br />
          {{ kuaWeightsOutputLine3 }}<br />
        </p>
      </el-dialog>
      <!-- Kua -->

      <br />
      <el-form-item :label="$t('message.speed')">
        <el-input v-model="umaStatus.speed" class="input-status"></el-input>
      </el-form-item>
      <el-form-item :label="$t('message.stamina')">
        <el-input v-model="umaStatus.stamina" class="input-status"></el-input>
      </el-form-item>
      <el-form-item :label="$t('message.power')">
        <el-input v-model="umaStatus.power" class="input-status"></el-input>
      </el-form-item>
      <el-form-item :label="$t('message.guts')">
        <el-input v-model="umaStatus.guts" class="input-status"></el-input>
      </el-form-item>
      <el-form-item :label="$t('message.wisdom')">
        <el-input v-model="umaStatus.wisdom" class="input-status"></el-input>
      </el-form-item>
      <br />
      <el-form-item :label="$t('message.style')">
        <el-select v-model="umaStatus.style" style="width: 100px">
          <el-option :label="$t('message.runningStyle1')" value="1"></el-option>
          <el-option :label="$t('message.runningStyle2')" value="2"></el-option>
          <el-option :label="$t('message.runningStyle3')" value="3"></el-option>
          <el-option :label="$t('message.runningStyle4')" value="4"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item :label="$t('message.distanceFit')">
        <el-select v-model="umaStatus.distanceFit" style="width: 70px">
          <el-option v-for="rank in fitRanks" :label="rank" :value="rank" :key="rank"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item :label="$t('message.surfaceFit')">
        <el-select v-model="umaStatus.surfaceFit" style="width: 70px">
          <el-option v-for="rank in fitRanks" :label="rank" :value="rank" :key="rank"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item :label="$t('message.styleFit')">
        <el-select v-model="umaStatus.styleFit" style="width: 70px">
          <el-option v-for="rank in fitRanks" :label="rank" :value="rank" :key="rank"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item :label="$t('message.mood')">
        <el-select v-model="umaStatus.condition" @change="initCondition" style="width: 130px">
          <el-option :label="$t('message.mood0')" value="0"></el-option>
          <el-option :label="$t('message.mood1')" value="1"></el-option>
          <el-option :label="$t('message.mood2')" value="2"></el-option>
          <el-option :label="$t('message.mood3')" value="3"></el-option>
          <el-option :label="$t('message.mood4')" value="4"></el-option>
          <el-option :label="$t('message.random')" value="5"></el-option>
        </el-select>
      </el-form-item>
      <br />
      <el-form-item :label="$t('message.course')">
        <el-select v-model="track.location" @change="locationChanged" style="width: 120px">
          <el-option v-for="(_, trackId) in this.trackData" :label="$t(`course.${trackId}`)" :value="trackId"
            :key="trackId"></el-option>
        </el-select>
        <el-select v-model="track.course" @change="courseChanged" style="width: 170px">
          <el-option v-for="(obj, key) in courseList" :label="`${$t('surface.' + obj.surface)}${obj.distance
            }m${courseNameSuffix(obj.name)}`" :value="key" :key="key">
          </el-option>
        </el-select>
        <span style="color: white">{{ track.course }}</span>
      </el-form-item>
      <el-form-item :label="$t('message.surfaceCondition')">
        <el-select v-model="track.surfaceCondition" style="width: 90px">
          <el-option :label="$t('message.surfaceCondition1')" value="1"></el-option>
          <el-option :label="$t('message.surfaceCondition2')" value="2"></el-option>
          <el-option :label="$t('message.surfaceCondition3')" value="3"></el-option>
          <el-option :label="$t('message.surfaceCondition4')" value="4"></el-option>
        </el-select>
      </el-form-item>
      <br />

      <el-form-item :label="$t('message.uniqueSkill')">
        <el-select v-model="selectedUnique" filterable :filter-method="filterUniqueSkills"
          @change="clearUniqueSkillFilter">
          <el-option v-for="skill in this.filteredUniqueSkillData" :label="skill.name" :value="skill.id"
            :key="skill.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="Lv">
        <el-input-number :max="6" :min="0" v-model="uniqueLevel"></el-input-number>
        &emsp;{{ $t("message.uniqueLv0Hint") }}
      </el-form-item>
      <br />

      <el-form-item :label="$t('message.evoSkill')">
        <div v-if="availableSkills.evo.length === 0">
          {{ $t("message.evoHint") }}
        </div>
        <el-checkbox-group v-model="hasEvoSkills">
          <el-tooltip v-for="skill in availableSkills.evo" :key="skill.name" :content="skill.tooltip"
            :disabled="!('tooltip' in skill)" :open-delay="500">
            <el-checkbox-button :label="skill.id">
              <SkillLabel :name="skill.name" :have="skill.have" />
            </el-checkbox-button>
          </el-tooltip>
        </el-checkbox-group>
      </el-form-item>
      <br />
      <!-- 添加按钮/开关 -->
      <el-form-item label="显示超前技能">
        <el-switch v-model="showPreemptiveSkill" active-text="显示" inactive-text="隐藏" />
      </el-form-item>
      <el-collapse v-model="skillGroups">
        <el-collapse-item v-for="menu in skillMenu" :title="menu.title" :name="menu.type" :key="menu.title">
          <div v-for="rarity in raritySections" :key="menu.type + rarity">
            <el-collapse v-if="
              rarity === 'inherit' &&
              ['speed', 'composite'].includes(menu.type)
            ">
              <el-collapse-item :title="menu.title + '：' + $t(rarityString[rarity])">
                <el-checkbox-group v-model="hasSkills[menu.type][rarity]">
                  <el-tooltip v-for="skill in availableSkills[menu.type][rarity]" :key="skill.name"
                    :content="skill.tooltip" :disabled="!('tooltip' in skill)" :open-delay="500">
                    <el-checkbox-button :label="skill.id">
                      <SkillLabel :name="skill.name" :have="skill.have" />
                    </el-checkbox-button>
                  </el-tooltip>
                </el-checkbox-group>
              </el-collapse-item>
            </el-collapse>

            <div v-if="
              rarity !== 'inherit' ||
              !['speed', 'composite'].includes(menu.type)
            ">
              <h3 v-if="availableSkills[menu.type][rarity].length > 0">
                {{ $t(rarityString[rarity]) }}
              </h3>
              <el-checkbox-group v-model="hasSkills[menu.type][rarity]">
                <el-tooltip v-for="skill in availableSkills[menu.type][rarity]" :key="skill.name"
                  :content="skill.tooltip" :disabled="!('tooltip' in skill)" :open-delay="500">
                  <el-checkbox-button v-if="skill.have || showPreemptiveSkill" :label="skill.id">
                    <SkillLabel :name="skill.name" :have="skill.have" />
                  </el-checkbox-button>
                </el-tooltip>
              </el-checkbox-group>
            </div>
          </div>
        </el-collapse-item>
      </el-collapse>
      <br />
      <ExecuteBlock ref="executeBlock" :exec-function="this.exec" />
    </el-form>
    <el-divider />
    <div class="p-6 space-y-6">
      <h3 class="text-xl font-semibold text-gray-800">{{ $t("message.emulationResult") }}</h3>
      <div class="overflow-x-auto">
        <table class="table-auto w-full border border-gray-300 text-sm text-center">
          <thead class="bg-gray-100">
            <tr>
              <th class="px-4 py-2"></th>
              <th class="px-4 py-2">{{ $t("message.realTime") }}</th>
              <th class="px-4 py-2">{{ $t("message.StandardDeviation") }}</th>
              <th class="px-4 py-2">{{ $t("message.best") }}</th>
              <th class="px-4 py-2">{{ $t("message.worst") }}</th>
              <th class="px-4 py-2">{{ $t("message.timeInGame") }}</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr>
              <th class="px-4 py-2 font-medium">{{ $t("message.avg") }}</th>
              <td class="px-4 py-2">{{ formatTime(avgRaceTime, 3) }}</td>
              <td class="px-4 py-2">{{ timeStandardDeviation.toFixed(3) }}</td>
              <td class="px-4 py-2">{{ formatTime(bestTime, 3) }}</td>
              <td class="px-4 py-2">{{ formatTime(worstTime, 3) }}</td>
              <td class="px-4 py-2">{{ formatTime(toDisplayTime(avgRaceTime), 1) }}</td>
            </tr>
            <tr>
              <th class="px-4 py-2 font-medium">{{ $t("message.MaxSpurt") }}</th>
              <td class="px-4 py-2">{{ formatTime(avgRaceTimeMaxSpurt, 3) }}</td>
              <td class="px-4 py-2">{{ timeStandardDeviationMaxSpurt.toFixed(3) }}</td>
              <td class="px-4 py-2">{{ formatTime(bestTimeMaxSpurt, 3) }}</td>
              <td class="px-4 py-2">{{ formatTime(worstTimeMaxSpurt, 3) }}</td>
              <td class="px-4 py-2">{{ formatTime(toDisplayTime(avgRaceTimeMaxSpurt), 1) }}</td>
            </tr>
            <tr>
              <th class="px-4 py-2 font-medium">{{ $t("message.NotMaxSpurt") }}</th>
              <td class="px-4 py-2">{{ formatTime(avgRaceTimeNotMaxSpurt, 3) }}</td>
              <td class="px-4 py-2">{{ timeStandardDeviationNotMaxSpurt.toFixed(3) }}</td>
              <td class="px-4 py-2">{{ formatTime(bestTimeNotMaxSpurt, 3) }}</td>
              <td class="px-4 py-2">{{ formatTime(worstTimeNotMaxSpurt, 3) }}</td>
              <td class="px-4 py-2">{{ formatTime(toDisplayTime(avgRaceTimeNotMaxSpurt), 1) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h3 class="text-xl font-semibold text-gray-800">{{ $t("message.spurtAverage") }}</h3>
      <div class="overflow-x-auto">
        <table class="table-auto w-full border border-gray-300 text-sm text-center">
          <thead class="bg-gray-100">
            <tr>
              <th class="px-4 py-2">{{ $t("message.maxSpurtRate") }}</th>
              <th class="px-4 py-2">{{ $t("message.maxSpurtSPLeft") }}</th>
              <th class="px-4 py-2">{{ $t("message.nonMaxSpurtSPLack") }}</th>
            </tr>
          </thead>
          <tbody>
            <tr class="bg-white">
              <td class="px-4 py-2">{{ maxSpurtRate }}%</td>
              <td class="px-4 py-2">{{ maxSpurtSPLeft }}</td>
              <td class="px-4 py-2">{{ nonMaxSpurtSPLack }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
      <h3 class="text-xl font-semibold text-gray-800">
        {{ $t("message.latestRaceTime") }} ({{ formatTime(latestRaceTime, 3) }})
      </h3>
      <chart-hint />
      <race-graph :chart-data="chartData" :options="chartOptions" />
    </div>
    <course-info :track="track" />
    <calculated-values />

    <el-divider />
    <release-note />
    <h3>注意事項</h3>
    <ol>
      <li>{{ $t("message.remark1") }}</li>
      <li>{{ $t("message.remark2") }}</li>
      <li>{{ $t("message.remark3") }}</li>
      <li>{{ $t("message.remark4") }}</li>
      <li>{{ $t("message.remark5") }}</li>
      <li>{{ $t("message.remark6") }}</li>
      <li>{{ $t("message.remark7") }}</li>
      <li>{{ $t("message.remark8") }}</li>
      <li>
        <a href="https://twitter.com/urakagi">{{ $t("message.contact") }}</a>
      </li>
    </ol>
  </div>
</template>

<script>
import MixinRaceCore from "@/components/MixinRaceCore";
import CourseInfo from "@/components/CourseInfo";
import ReleaseNote from "@/components/ReleaseNote";
import CalculatedValues from "@/components/CalculatedValues";
import ChartHint from "./ChartHint";
import ExecuteBlock from "./ExecuteBlock";
import SkillLabel from './SkillLabel';
export default {
  name: "ChampMeet",
  components: {
    ExecuteBlock,
    ChartHint,
    CalculatedValues,
    ReleaseNote,
    CourseInfo,
    SkillLabel,
  },
  mixins: [MixinRaceCore],
  data() {
    return {
      emulatorType: "cm",
      showPreemptiveSkill: false,
    };
  },
  computed: {
    distanceType() {
      return this.trackDetail.distanceType;
    },
    surfaceType() {
      return this.trackDetail.surface;
    },
  },
  mounted() {
    const sc = localStorage.getItem("selectedCourse");
    if (sc) {
      const j = JSON.parse(sc);
      this.track.location = j.location;
      this.locationChanged(this.track.location);
      this.track.course = j.course;
    } else {
      this.track.location = Object.keys(this.trackData)[0];
      this.locationChanged(this.track.location);
      this.track.course = Object.keys(this.courseList)[0];
    }
  },
};
</script>
