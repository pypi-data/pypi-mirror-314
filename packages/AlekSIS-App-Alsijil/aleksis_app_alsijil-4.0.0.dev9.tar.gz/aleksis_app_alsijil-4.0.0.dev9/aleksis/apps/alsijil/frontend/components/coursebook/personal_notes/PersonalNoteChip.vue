<script>
export default {
  name: "PersonalNoteChip",
  props: {
    note: {
      type: Object,
      required: true,
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
  <v-tooltip bottom>
    <template #activator="{ on, attrs }">
      <v-chip
        dense
        outlined
        v-bind="{ ...$attrs, ...attrs }"
        v-on="{ ...$listeners, ...on }"
      >
        <v-avatar left>
          <v-icon small>mdi-note-outline</v-icon>
        </v-avatar>
        <slot name="prepend" />
        <slot>
          <span class="text-truncate" style="max-width: 30ch">
            {{ note.note }}
          </span>
        </slot>
        <slot name="append" />
        <v-avatar right v-if="loading">
          <v-progress-circular indeterminate :size="16" :width="2" />
        </v-avatar>
      </v-chip>
    </template>
    <span v-text="note.note" />
  </v-tooltip>
</template>
