<template>
  <v-card>
    <v-skeleton-loader
      v-if="$apollo.queries.statistics.loading"
      type="card-heading"
    />
    <v-card-title v-else-if="compact">
      {{ $t("alsijil.coursebook.statistics.person_compact.title") }}
      <v-spacer />
      <base-button
        :icon="true"
        icon-text="mdi-open-in-new"
        i18n-key=""
        :to="{
          name: 'alsijil.coursebook_statistics',
          params: {
            personId: person.id,
            mode: MODE.PARTICIPATIONS,
          },
        }"
      />
    </v-card-title>
    <v-card-title v-else>
      {{ $t("alsijil.coursebook.statistics.title_plural") }}
    </v-card-title>

    <v-card-text
      v-if="!$apollo.queries.statistics.loading && statistics == null"
    >
      <message-box type="error">
        <div>{{ $t("generic_messages.error") }}</div>
        <small>
          {{ $t("error_code", { errorCode }) }}
        </small>
      </message-box>
    </v-card-text>
    <v-card-text v-else>
      <div class="grid">
        <statistics-absences-card
          style="grid-area: absences"
          :absence-reasons="statistics.absenceReasons"
          :loading="$apollo.queries.statistics.loading"
        />
        <statistics-tardiness-card
          style="grid-area: tardinesses"
          :tardiness-sum="statistics.tardinessSum"
          :tardiness-count="statistics.tardinessCount"
          :loading="$apollo.queries.statistics.loading"
        />
        <statistics-extra-marks-card
          style="grid-area: extra_marks"
          :extra-marks="statistics.extraMarks"
          :loading="$apollo.queries.statistics.loading"
        />
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import personOverviewCardMixin from "aleksis.core/mixins/personOverviewCardMixin.js";
import BaseButton from "aleksis.core/components/generic/buttons/BaseButton.vue";
import MessageBox from "aleksis.core/components/generic/MessageBox.vue";
import StatisticsAbsencesCard from "./StatisticsAbsencesCard.vue";
import StatisticsTardinessCard from "./StatisticsTardinessCard.vue";
import StatisticsExtraMarksCard from "./StatisticsExtraMarksCard.vue";

import { statisticsByPerson } from "./statistics.graphql";
import errorCodes from "../../../errorCodes";
import { MODE } from "./modes";

export default {
  name: "StatisticsForPersonCard",
  mixins: [personOverviewCardMixin],
  components: {
    BaseButton,
    MessageBox,
    StatisticsAbsencesCard,
    StatisticsTardinessCard,
    StatisticsExtraMarksCard,
  },
  props: {
    compact: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
  data() {
    return {
      statistics: {
        absenceReasons: [],
        tardinessSum: 0,
        tardinessCount: 0,
        extraMarks: [],
      },
      errorCode: errorCodes.statisticsEmpty,
    };
  },
  apollo: {
    statistics: {
      query: statisticsByPerson,
      variables() {
        return {
          person: this.person.id,
        };
      },
    },
  },
  computed: {
    MODE() {
      return MODE;
    },
    gridTemplateAreas() {
      return this.compact
        ? `"absences extra_marks" "tardinesses tardinesses"`
        : `"absences" "tardinesses" "extra_marks"`;
    },
    gridTemplateColumnsNum() {
      return this.compact ? 2 : 1;
    },
  },
};
</script>

<style scoped>
.grid {
  display: grid;
  max-width: 100%;
  grid-template-columns: repeat(v-bind(gridTemplateColumnsNum), minmax(0, 1fr));
  grid-template-areas: v-bind(gridTemplateAreas);
  gap: 0.5em;
}
</style>
