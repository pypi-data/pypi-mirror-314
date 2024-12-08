<template>
  <c-r-u-d-list
    i18n-key="TODO"
    :headers="headers"
    :gql-query="gqlQuery"
    :gql-additional-query-args="gqlQueryArgs"
    :enable-create="false"
    :enable-edit="false"
    :elevated="false"
    :show-select="false"
    @items="items = $event"
  >
    <template
      v-for="(extraMark, index) in extraMarks"
      #[`extraMarks.${index}.count`]="{ item }"
    >
      <extra-mark-chip
        :key="extraMark.id"
        :extra-mark="extraMark"
        only-show-count
        dense
        :count="
          item.extraMarks.find((m) => extraMark.id === m.extraMark.id).count
        "
      />
    </template>

    <template
      v-for="(absenceReason, index) in absenceReasons"
      #[`absenceReasons.${index}.count`]="{ item }"
    >
      <absence-reason-chip
        :key="absenceReason.id"
        :absence-reason="absenceReason"
        only-show-count
        dense
        :count="
          item.absenceReasons.find(
            (m) => absenceReason.id === m.absenceReason.id,
          ).count
        "
      />
    </template>

    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #person.fullName="{ item }">
      <person-chip :person="item.person" />
    </template>

    <template #tardinessCount="{ item }">
      <v-chip dense outlined class="me-2">
        <v-icon left>mdi-chart-line-variant</v-icon>
        {{ $tc("alsijil.personal_notes.times_late", item.tardinessCount) }}
      </v-chip>
      <v-chip dense outlined v-if="item.tardinessSum">
        <v-icon left>mdi-sigma</v-icon>
        {{
          $tc("time.minutes_n", item.tardinessSum, { n: $n(item.tardinessSum) })
        }}
      </v-chip>
    </template>

    <template #actions="{ item }">
      <secondary-action-button
        i18n-key="alsijil.personal_notes.statistics.person_view_details"
        icon-text="mdi-open-in-new"
        :to="{
          name: 'alsijil.coursebook_statistics',
          params: {
            personId: item.person.id,
            mode: MODE.PARTICIPATIONS,
          },
        }"
      />
    </template>
  </c-r-u-d-list>
</template>

<script>
import groupOverviewTabMixin from "aleksis.core/mixins/groupOverviewTabMixin.js";
import CRUDList from "aleksis.core/components/generic/CRUDList.vue";
import PersonChip from "aleksis.core/components/person/PersonChip.vue";
import SecondaryActionButton from "aleksis.core/components/generic/buttons/SecondaryActionButton.vue";

import AbsenceReasonChip from "aleksis.apps.kolego/components/AbsenceReasonChip.vue";
import ExtraMarkChip from "aleksis.apps.alsijil/components/extra_marks/ExtraMarkChip.vue";

import { statisticsByGroup } from "./statistics.graphql";
import { absenceReasons } from "../queries/absenceReasons.graphql";
import { extraMarks } from "../../extra_marks/extra_marks.graphql";
import { MODE } from "./modes";

export default {
  name: "StatisticsForGroupTab",
  mixins: [groupOverviewTabMixin],
  components: {
    AbsenceReasonChip,
    CRUDList,
    ExtraMarkChip,
    PersonChip,
    SecondaryActionButton,
  },
  data() {
    return {
      gqlQuery: statisticsByGroup,
      items: [],
      absenceReasons: [],
      extraMarks: [],
    };
  },
  computed: {
    MODE() {
      return MODE;
    },
    headers() {
      // TODO: i18n
      return [
        {
          text: this.$t("person.name"),
          value: "person.fullName",
        },
        ...this.absenceReasons.map((reason, index) => {
          return {
            text: reason.name,
            value: `absenceReasons.${index}.count`,
            align: "center",
          };
        }),
        ...this.extraMarks.map((mark, index) => {
          return {
            text: mark.name,
            value: `extraMarks.${index}.count`,
            align: "center",
          };
        }),
        {
          text: this.$t("alsijil.personal_notes.tardiness_plural"),
          value: "tardinessCount",
          align: "center",
        },
        {
          value: "actions",
          sortable: false,
        },
      ];
    },
    absenceReasonsFirstHeader() {
      return this.absenceReasons.length > 0
        ? this.absenceReasons[0].shortName + ".header"
        : null;
    },
    extraMarksFirstHeader() {
      return this.extraMarks.length > 0
        ? this.extraMarks[0].shortName + ".header"
        : null;
    },
    gqlQueryArgs() {
      const term = this.schoolTerm ? { term: this.schoolTerm.id } : {};
      return {
        group: this.group.id,
        ...term,
      };
    },
  },
  apollo: {
    absenceReasons: {
      query: absenceReasons,
      update: (data) => data.items,
    },
    extraMarks: {
      query: extraMarks,
      update: (data) => data.items,
    },
  },
};
</script>
