<template>
  <v-skeleton-loader v-if="loading" type="card" />
  <v-card v-else>
    <v-card-text class="d-flex flex-column" style="gap: 0.5em">
      <counter-chip
        v-for="extraMark in extraMarks"
        :key="extraMark.id"
        :value="extraMark.extraMark.id"
        :color="extraMark.extraMark.colourBg"
        :text-color="extraMark.extraMark.colourFg"
        :count="extraMark.count"
      >
        {{ extraMark.extraMark.name }}
      </counter-chip>
    </v-card-text>
  </v-card>
</template>

<script>
import CounterChip from "aleksis.core/components/generic/chips/CounterChip.vue";

export default {
  name: "StatisticsExtraMarksCard",
  components: {
    CounterChip,
  },
  props: {
    extraMarks: {
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
