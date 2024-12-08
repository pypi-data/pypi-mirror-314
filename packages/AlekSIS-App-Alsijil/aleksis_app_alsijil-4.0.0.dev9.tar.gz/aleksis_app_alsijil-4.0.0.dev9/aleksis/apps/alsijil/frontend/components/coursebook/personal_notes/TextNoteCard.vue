<template>
  <v-card
    outlined
    dense
    rounded="lg"
    class="mb-2"
    v-bind="$attrs"
    v-on="$listeners"
  >
    <v-card-title class="text-subtitle-2 pb-1 font-weight-medium">
      {{ $t("alsijil.personal_notes.card.title") }}
    </v-card-title>
    <v-card-text>{{ note.note || "–" }}</v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "TextNoteCard",
  props: {
    note: {
      type: Object,
      required: true,
    },
  },
};
</script>
