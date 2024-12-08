<template>
  <v-skeleton-loader v-if="loading" type="card" />
  <v-card v-else>
    <v-card-text class="d-flex flex-column" style="gap: 0.5em">
      <absence-reason-chip
        v-for="absenceReason in absenceReasons"
        :key="absenceReason.id"
        :absenceReason="absenceReason.absenceReason"
        :count="absenceReason.count"
      />
    </v-card-text>
  </v-card>
</template>

<script>
import AbsenceReasonChip from "aleksis.apps.kolego/components/AbsenceReasonChip.vue";

export default {
  name: "StatisticsAbsencesCard",
  components: {
    AbsenceReasonChip,
  },
  props: {
    absenceReasons: {
      type: Array,
      required: true,
    },
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
};
</script>
