<script>
export default {
  name: "TardinessChip",
  props: {
    tardiness: {
      type: Number,
      required: false,
      default: 0,
    },
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  extends: "v-chip",
};
</script>

<template>
  <v-chip dense outlined v-bind="$attrs" v-on="$listeners">
    <v-avatar left>
      <v-icon small>mdi-clock-alert-outline</v-icon>
    </v-avatar>
    <slot name="prepend" />
    <slot>
      {{ $tc("alsijil.personal_notes.minutes_late", tardiness) }}
    </slot>
    <slot name="append" />
    <v-avatar right v-if="loading">
      <v-progress-circular indeterminate :size="16" :width="2" />
    </v-avatar>
  </v-chip>
</template>
