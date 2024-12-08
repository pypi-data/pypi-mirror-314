<script>
import CounterChip from "aleksis.core/components/generic/chips/CounterChip.vue";

export default {
  name: "ExtraMarkChip",
  components: { CounterChip },
  props: {
    extraMark: {
      type: Object,
      required: true,
    },
    short: {
      type: Boolean,
      required: false,
      default: false,
    },
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  extends: CounterChip,
  computed: {
    text() {
      return this.short ? this.extraMark.shortName : this.extraMark.name;
    },
  },
};
</script>

<template>
  <counter-chip
    :color="extraMark.colourBg"
    :text-color="extraMark.colourFg"
    :value="extraMark.id"
    :count="count"
    :only-show-count="onlyShowCount"
    :outlined="false"
    v-bind="$attrs"
    v-on="$listeners"
  >
    <slot name="prepend" />
    {{ text }}
    <slot name="append" />
    <v-avatar right v-if="loading">
      <v-progress-circular indeterminate :size="16" :width="2" />
    </v-avatar>
  </counter-chip>
</template>
