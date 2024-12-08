<template>
  <div v-bind="$attrs" v-on="$listeners">
    <v-card outlined dense rounded="lg" class="mb-2">
      <v-card-title class="text-subtitle-2 pb-1 font-weight-medium">
        {{ $t("alsijil.coursebook.summary.topic.label") }}
      </v-card-title>
      <v-card-text>{{ documentation.topic || "–" }}</v-card-text>
    </v-card>
    <v-card outlined dense rounded="lg" class="mb-2">
      <v-card-title class="text-subtitle-2 pb-1 font-weight-medium">
        {{ $t("alsijil.coursebook.summary.homework.label") }}
      </v-card-title>
      <v-card-text>
        {{
          documentation.homework ||
          $t("alsijil.coursebook.summary.homework.empty_yet")
        }}
      </v-card-text>
    </v-card>
    <v-card outlined dense rounded="lg">
      <v-card-title class="text-subtitle-2 pb-1 font-weight-medium">
        {{ $t("alsijil.coursebook.summary.group_note.label") }}
      </v-card-title>
      <v-card-text>
        {{
          documentation.groupNote ||
          $t("alsijil.coursebook.summary.group_note.empty")
        }}
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "DocumentationFullDetails",
  props: {
    documentation: {
      type: Object,
      required: true,
    },
  },
};
</script>
