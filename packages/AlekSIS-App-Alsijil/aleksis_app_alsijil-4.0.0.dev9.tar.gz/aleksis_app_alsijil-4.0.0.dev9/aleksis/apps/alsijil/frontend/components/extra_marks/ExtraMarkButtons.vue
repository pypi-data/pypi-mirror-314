<script>
import { extraMarks } from "./extra_marks.graphql";

export default {
  name: "ExtraMarkButtons",
  data() {
    return {
      extraMarks: [],
    };
  },
  apollo: {
    extraMarks: {
      query: extraMarks,
      update: (data) => data.items,
      skip() {
        return this.customExtraMarks.length > 0;
      },
    },
  },
  props: {
    customExtraMarks: {
      type: Array,
      required: false,
      default: () => [],
    },
  },
  computed: {
    innerExtraMarks() {
      if (this.customExtraMarks.length > 0) {
        return this.customExtraMarks;
      } else {
        return this.extraMarks;
      }
    },
  },
  methods: {
    emit(value) {
      this.$emit("input", value);
      this.$emit("click", value);
    },
  },
};
</script>

<template>
  <div class="d-flex flex-wrap" style="gap: 0.5em">
    <v-skeleton-loader
      class="full-width d-flex flex-wrap child-flex-grow-1"
      style="gap: 0.5em"
      v-if="$apollo.queries.extraMarks.loading"
      type="button@4"
    />
    <template v-else>
      <v-btn
        v-for="extraMark in innerExtraMarks"
        :key="'extra-mark-' + extraMark.id"
        :color="extraMark.colourBg"
        :style="{ color: extraMark.colourFg }"
        class="flex-grow-1"
        depressed
        @click="emit(extraMark.id)"
      >
        {{ extraMark.name }}
      </v-btn>
    </template>
  </div>
</template>

<style>
.child-flex-grow-1 > * {
  flex-grow: 1;
}
</style>
